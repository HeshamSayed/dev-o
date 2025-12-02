"""
External AI Client - Integrated from old DEV-O backend

Client for interacting with external AI service via HTTP API.
Supports DeepSeek Coder and other models via SSE streaming.
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass

import httpx
import aiohttp

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
    """
    Client for External AI API with SSE streaming support.

    Supports:
    - Streaming and non-streaming generation via SSE
    - Tool/function calling (via prompt engineering)
    - DeepSeek R1 thinking extraction
    """

    def __init__(self, config: Optional[ExternalAIConfig] = None):
        self.config = config or ExternalAIConfig()

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

        # Build request payload matching DeepSeek API format
        payload = {
            "prompt": full_prompt,
            "think": thinking_mode,  # Add thinking mode parameter EARLY in payload
        }

        # Add model parameter
        payload["model"] = self.config.model

        payload["temperature"] = temperature

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        else:
            payload["max_tokens"] = self.config.default_max_tokens

        # Only add these if explicitly set
        if top_p is not None:
            payload["top_p"] = top_p
        if top_k is not None:
            payload["top_k"] = top_k
        if repeat_penalty is not None:
            payload["repeat_penalty"] = repeat_penalty
        if num_ctx is not None:
            payload["num_ctx"] = num_ctx

        # Add system prompt if provided, otherwise use default
        if system:
            payload["system"] = system
        elif self.config.default_system_prompt:
            payload["system"] = self.config.default_system_prompt

        headers = {
            "Content-Type": "application/json"
        }

        # Debug logging
        logger.info(f"Sending SSE request with thinking_mode={thinking_mode}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            # Use aiohttp for better SSE stream handling
            timeout = aiohttp.ClientTimeout(
                total=None,  # No total timeout for SSE
                connect=10,
                sock_connect=10,
                sock_read=None  # No read timeout for streaming
            )

            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    f"{self.config.base_url}/generate/sse",
                    json=payload,
                    headers=headers
                ) as response:
                    response.raise_for_status()

                    # Parse SSE stream line by line
                    buffer = b""
                    async for chunk in response.content.iter_any():
                        buffer += chunk

                        # Process complete lines
                        while b'\n' in buffer:
                            line, buffer = buffer.split(b'\n', 1)
                            try:
                                line_str = line.decode('utf-8').strip()
                            except UnicodeDecodeError:
                                continue  # Skip non-UTF8 lines

                            # SSE format: "data: {json}"
                            if line_str.startswith('data: '):
                                data_str = line_str[6:]  # Remove "data: " prefix

                                # Skip SSE comments, empty lines, and [DONE] marker
                                if not data_str or data_str.startswith(':') or data_str == '[DONE]':
                                    continue

                                try:
                                    data = json.loads(data_str)

                                    # Handle different event types
                                    event_type = data.get("type")

                                    if event_type == "thinking_start":
                                        logger.info("Received thinking_start event")
                                        yield {"type": "thinking_start"}
                                    elif event_type == "thinking":
                                        content = data.get("content", "")
                                        logger.debug(f"Received thinking content: {content[:30]}...")
                                        yield {"type": "thinking", "content": content}
                                    elif event_type == "thinking_end":
                                        logger.info("Received thinking_end event")
                                        yield {"type": "thinking_end"}
                                    elif event_type == "content" or "content" in data:
                                        # Normal content streaming
                                        yield {"type": "content", "content": data.get("content", "")}

                                    # Check for completion
                                    if data.get("done") or data.get("finished"):
                                        logger.info("Stream complete")
                                        return  # Exit the generator

                                except json.JSONDecodeError as e:
                                    if data_str != '[DONE]':
                                        logger.warning(f"Failed to parse SSE data: {data_str[:100]}, error: {e}")
                                    continue

        except aiohttp.ClientResponseError as e:
            logger.error(f"External AI request failed: {e.status} - {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in external AI client: {e}")
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

            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(
                    f"{self.config.base_url}/generate/sse",
                    json=payload,
                    headers=headers
                )
                return response.status_code == 200

        except Exception as e:
            logger.error(f"External AI health check failed: {e}")
            return False
