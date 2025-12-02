"""
Fixed External AI Client using requests for SSE streaming.

Uses requests library with proper async iteration for reliable SSE streaming.
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass
import requests
import threading
import queue

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
    """Fixed client for External AI API with SSE streaming support."""

    def __init__(self, config: Optional[ExternalAIConfig] = None):
        self.config = config or ExternalAIConfig()

    def _stream_worker(self, payload: Dict, headers: Dict, event_queue: queue.Queue):
        """Worker thread that processes SSE stream."""
        try:
            response = requests.post(
                f"{self.config.base_url}/generate/sse",
                json=payload,
                headers=headers,
                stream=True,
                timeout=(5, None)  # 5 sec connect, no read timeout
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    event_queue.put(('data', line.decode('utf-8')))
                else:
                    event_queue.put(('data', ''))  # Empty line

            event_queue.put(('done', None))
            response.close()

        except Exception as e:
            event_queue.put(('error', str(e)))
            logger.error(f"Stream worker error: {e}")

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

        Yields event dictionaries with type and content.
        """
        # Add tools to prompt if provided
        full_prompt = prompt
        if tools:
            full_prompt = self._add_tools_to_prompt(full_prompt, tools)

        # Build request payload
        payload = {
            "prompt": full_prompt,
            "think": thinking_mode,  # Enable thinking mode
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

        # Create queue for thread communication
        event_queue = queue.Queue()

        # Start worker thread
        worker = threading.Thread(
            target=self._stream_worker,
            args=(payload, headers, event_queue),
            daemon=True
        )
        worker.start()

        # Process events from queue
        while True:
            # Non-blocking queue get with timeout
            try:
                event_type, data = await asyncio.get_event_loop().run_in_executor(
                    None, event_queue.get, True, 0.1
                )
            except queue.Empty:
                # Check if thread is still alive
                if not worker.is_alive():
                    break
                continue

            if event_type == 'error':
                logger.error(f"External AI request failed: {data}")
                raise Exception(data)

            elif event_type == 'done':
                break

            elif event_type == 'data':
                line_str = data.strip()

                # SSE format: "data: {json}"
                if line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove "data: " prefix

                    # Skip SSE comments, empty lines, and [DONE] marker
                    if not data_str or data_str.startswith(':') or data_str == '[DONE]':
                        continue

                    try:
                        data_json = json.loads(data_str)

                        # Handle different event types
                        event_type = data_json.get("type")

                        if event_type == "thinking_start":
                            logger.info("Received thinking_start event")
                            yield {"type": "thinking_start"}
                        elif event_type == "thinking":
                            content = data_json.get("content", "")
                            logger.debug(f"Received thinking content: {content[:30] if content else ''}...")
                            yield {"type": "thinking", "content": content}
                        elif event_type == "thinking_end":
                            logger.info("Received thinking_end event")
                            yield {"type": "thinking_end"}
                        elif event_type == "content":
                            # Normal content streaming
                            yield {"type": "content", "content": data_json.get("content", "")}
                        elif "content" in data_json and not event_type:
                            # Handle content without explicit type field
                            yield {"type": "content", "content": data_json.get("content", "")}

                        # Check for completion
                        if data_json.get("done") or data_json.get("finished"):
                            logger.info("Stream complete")
                            break

                    except json.JSONDecodeError as e:
                        if data_str != '[DONE]':
                            logger.warning(f"Failed to parse SSE data: {data_str[:100]}, error: {e}")
                        continue

        # Ensure thread cleanup
        worker.join(timeout=1)

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