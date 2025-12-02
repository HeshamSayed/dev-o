"""
Simple External AI Client using requests for SSE streaming.

Uses asyncio.to_thread for simplicity.
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass
import requests

logger = logging.getLogger(__name__)


@dataclass
class ExternalAIConfig:
    """External AI service configuration."""
    base_url: str = "http://34.136.165.200:8000"
    api_key: str = "sk-test-123456"
    model: str = "deepseek-coder-optimized"

    # DeepSeek Coder specific parameters
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    num_ctx: int = 8192
    default_max_tokens: int = 4096
    default_system_prompt: str = "You are DEV-O, an expert AI coding assistant. Provide clear, efficient, and well-documented code with best practices."
    timeout: int = 120


class ExternalAIClient:
    """Simple client for External AI API with SSE streaming support."""

    def __init__(self, config: Optional[ExternalAIConfig] = None):
        self.config = config or ExternalAIConfig()

    def _make_sse_request(self, payload: Dict, headers: Dict) -> list:
        """Make SSE request and collect all events."""
        events = []
        try:
            response = requests.post(
                f"{self.config.base_url}/generate/sse",
                json=payload,
                headers=headers,
                stream=True,
                timeout=(5, None)
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8').strip()
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        if data_str and data_str != '[DONE]' and not data_str.startswith(':'):
                            try:
                                data = json.loads(data_str)
                                events.append(data)
                            except json.JSONDecodeError:
                                pass

            response.close()
        except Exception as e:
            logger.error(f"SSE request error: {e}")
            raise

        return events

    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict]] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        repeat_penalty: Optional[float] = None,
        num_ctx: Optional[int] = None,
        thinking_mode: bool = False,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Generate a response with streaming via SSE.

        Note: This implementation collects all events first for simplicity.
        """
        # Add tools to prompt if provided
        full_prompt = prompt
        if tools:
            full_prompt = self._add_tools_to_prompt(full_prompt, tools)

        # Build request payload
        payload = {
            "prompt": full_prompt,
            "think": thinking_mode,
        }

        # Add model
        payload["model"] = self.config.model
        payload["temperature"] = temperature

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        else:
            payload["max_tokens"] = self.config.default_max_tokens

        # Add system prompt
        if system:
            payload["system"] = system
        elif self.config.default_system_prompt:
            payload["system"] = self.config.default_system_prompt

        # Only add optional params if explicitly set
        if top_p is not None:
            payload["top_p"] = top_p
        if top_k is not None:
            payload["top_k"] = top_k
        if repeat_penalty is not None:
            payload["repeat_penalty"] = repeat_penalty
        if num_ctx is not None:
            payload["num_ctx"] = num_ctx

        headers = {
            "Content-Type": "application/json"
        }

        # Debug logging
        logger.info(f"Sending SSE request with thinking_mode={thinking_mode}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            # Run blocking request in thread
            if hasattr(asyncio, 'to_thread'):
                # Python 3.9+
                events = await asyncio.to_thread(
                    self._make_sse_request, payload, headers
                )
            else:
                # Python 3.8
                loop = asyncio.get_event_loop()
                events = await loop.run_in_executor(
                    None, self._make_sse_request, payload, headers
                )

            # Process and yield events
            for data in events:
                event_type = data.get("type")

                if event_type == "thinking_start":
                    logger.info("Received thinking_start event")
                    yield {"type": "thinking_start"}
                elif event_type == "thinking":
                    content = data.get("content", "")
                    logger.debug(f"Received thinking content: {content[:30] if content else ''}...")
                    yield {"type": "thinking", "content": content}
                elif event_type == "thinking_end":
                    logger.info("Received thinking_end event")
                    yield {"type": "thinking_end"}
                elif event_type == "content":
                    yield {"type": "content", "content": data.get("content", "")}
                elif "content" in data and not event_type:
                    yield {"type": "content", "content": data.get("content", "")}

                # Check for completion
                if data.get("done") or data.get("finished"):
                    logger.info("Stream complete")
                    break

        except Exception as e:
            logger.error(f"External AI error: {e}")
            raise

    def _add_tools_to_prompt(
        self,
        prompt: str,
        tools: List[Dict]
    ) -> str:
        """Add tool definitions to the prompt."""
        tools_section = """## Available Tools

You have access to the following tools. To use a tool, respond with a JSON block in this exact format:
```tool_call
{
    "tool": "tool_name",
    "arguments": {
        "arg1": "value1",
        "arg2": "value2"
    },
    "reasoning": "Brief explanation of why you're using this tool"
}
```

Available tools:

"""
        for tool in tools:
            tools_section += f"### {tool['name']}\n"
            tools_section += f"{tool['description']}\n"
            if tool.get('parameters'):
                tools_section += "Parameters:\n"
                for param_name, param_info in tool['parameters'].get('properties', {}).items():
                    required = param_name in tool['parameters'].get('required', [])
                    req_str = " (required)" if required else " (optional)"
                    tools_section += f"  - {param_name}{req_str}: {param_info.get('description', '')}\n"
            tools_section += "\n"

        tools_section += """
After using a tool, wait for the result before continuing.
If you need to use multiple tools, use them one at a time.
When you have completed the task, respond normally without a tool_call block.

---

"""
        return tools_section + prompt

    def parse_thinking(self, text: str) -> tuple[str, str]:
        """
        Extract thinking from response.

        Returns (thinking, clean_text)
        """
        import re
        thinking = ""
        # Extract thinking (R1 format)
        thinking_match = re.search(r"<think>(.*?)</think>", text, re.DOTALL)
        if thinking_match:
            thinking = thinking_match.group(1).strip()
            text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

        return thinking, text.strip()

    async def check_health(self) -> bool:
        """Check if external AI service is running and accessible."""
        try:
            headers = {"Content-Type": "application/json"}

            payload = {
                "prompt": "Hi",
                "model": self.config.model,
                "system": "You are a helpful assistant.",
                "temperature": 0.7,
                "max_tokens": 10
            }

            if hasattr(asyncio, 'to_thread'):
                response = await asyncio.to_thread(
                    lambda: requests.post(
                        f"{self.config.base_url}/generate/sse",
                        json=payload,
                        headers=headers,
                        timeout=5
                    )
                )
            else:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(
                        f"{self.config.base_url}/generate/sse",
                        json=payload,
                        headers=headers,
                        timeout=5
                    )
                )
            return response.status_code == 200

        except Exception as e:
            logger.error(f"External AI health check failed: {e}")
            return False