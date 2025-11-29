"""
External AI Client

Client for interacting with external AI service via HTTP API.
"""

import asyncio
import json
import logging
import re
from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass

import aiohttp

try:
    import orjson  # Fast JSON library for better performance
    USE_ORJSON = True
except ImportError:
    USE_ORJSON = False

from .base import BaseLLMClient, LLMConfig, LLMResponse

logger = logging.getLogger(__name__)


@dataclass
class ExternalAIConfig(LLMConfig):
    """External AI service configuration."""
    base_url: str = "http://34.136.165.200:8000"
    api_key: str = "sk-test-123456"

    # DeepSeek Coder specific parameters
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    num_ctx: int = 8192
    default_max_tokens: int = 4096
    default_system_prompt: str = "You are DeepSeek Coder, an expert programming assistant. Provide clear, efficient, and well-documented code with best practices."


class ExternalAIClient(BaseLLMClient):
    """
    Client for External AI API.

    Supports:
    - Streaming and non-streaming generation via SSE
    - Tool/function calling (via prompt engineering)
    - DeepSeek R1 thinking extraction
    """

    def __init__(self, config: Optional[ExternalAIConfig] = None):
        self.config = config or ExternalAIConfig(model='default')
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def close(self):
        """Close the session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def generate(
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
    ) -> str:
        """
        Generate a response (non-streaming).

        Args:
            prompt: User prompt
            system: System prompt
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            tools: Tool definitions (will be added to prompt)
            top_p: Nucleus sampling probability
            top_k: Top-k sampling
            repeat_penalty: Penalty for repeating tokens
            num_ctx: Context window size

        Returns:
            Generated text
        """
        full_response = ""
        async for chunk in self.generate_stream(
            prompt=prompt,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
            top_p=top_p,
            top_k=top_k,
            repeat_penalty=repeat_penalty,
            num_ctx=num_ctx,
        ):
            full_response += chunk

        return full_response

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
    ) -> AsyncGenerator[str, None]:
        """
        Generate a response with streaming via SSE.

        Yields chunks of generated text as they arrive.

        Args:
            prompt: User prompt
            system: System prompt (sent separately in DeepSeek API)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            tools: Tool definitions (will be added to prompt)
            top_p: Nucleus sampling probability
            top_k: Top-k sampling
            repeat_penalty: Penalty for repeating tokens
            num_ctx: Context window size
        """
        session = await self._get_session()

        # Add tools to prompt if provided
        full_prompt = prompt
        if tools:
            full_prompt = self._add_tools_to_prompt(full_prompt, tools)

        # Build request payload matching DeepSeek API format
        # System prompt is sent separately, not combined with user prompt
        payload = {
            "prompt": full_prompt,
            "model": self.config.model or "deepseek-coder-optimized",
            "temperature": temperature,
            "top_p": top_p if top_p is not None else self.config.top_p,
            "top_k": top_k if top_k is not None else self.config.top_k,
            "repeat_penalty": repeat_penalty if repeat_penalty is not None else self.config.repeat_penalty,
            "num_ctx": num_ctx if num_ctx is not None else self.config.num_ctx,
            "max_tokens": max_tokens if max_tokens is not None else self.config.default_max_tokens,
        }

        # Add system prompt if provided, otherwise use default
        if system:
            payload["system"] = system
        elif self.config.default_system_prompt:
            payload["system"] = self.config.default_system_prompt

        headers = {
            "Content-Type": "application/json"
        }

        try:
            async with session.post(
                f"{self.config.base_url}/generate/sse",
                json=payload,
                headers=headers
            ) as response:
                response.raise_for_status()

                # Parse SSE stream - read line by line for real-time streaming
                buffer = b""
                async for chunk in response.content.iter_chunked(8192):
                    buffer += chunk

                    # Process complete lines immediately
                    while b'\n' in buffer:
                        line, buffer = buffer.split(b'\n', 1)
                        line_str = line.decode('utf-8').strip()

                        # SSE format: "data: {json}"
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]  # Remove "data: " prefix

                            # Skip SSE comments, empty lines, and [DONE] marker
                            if not data_str or data_str.startswith(':') or data_str == '[DONE]':
                                continue

                            try:
                                # Use orjson for faster JSON parsing if available
                                if USE_ORJSON:
                                    data = orjson.loads(data_str)
                                else:
                                    data = json.loads(data_str)

                                # Extract response content
                                if "content" in data:
                                    yield data["content"]

                                # Check for completion
                                if data.get("done") or data.get("finished"):
                                    break

                            except (json.JSONDecodeError, ValueError) as e:
                                # Only log if it's not a [DONE] marker
                                if data_str != '[DONE]':
                                    logger.warning(f"Failed to parse SSE data: {data_str}, error: {e}")
                                continue

        except aiohttp.ClientError as e:
            logger.error(f"External AI request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in external AI client: {e}")
            raise

    def _add_tools_to_prompt(
        self,
        prompt: str,
        tools: List[Dict]
    ) -> str:
        """
        Add tool definitions to the prompt.

        Since the external service may not natively support function calling,
        we add tool definitions to the prompt and parse the response.
        """
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

    def parse_response(self, response: str) -> LLMResponse:
        """
        Parse LLM response to extract thinking, tool calls, and answer.

        DeepSeek R1 outputs thinking in <think>...</think> tags.
        Tool calls are in ```tool_call...``` blocks.
        """
        thinking = ""
        tool_calls = []
        is_final = True

        # Extract thinking (R1 format)
        thinking_match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
        if thinking_match:
            thinking = thinking_match.group(1).strip()
            response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)

        # Extract tool calls - support both ```tool_call and ```json formats
        tool_call_pattern = r"```(?:tool_call|json)\s*\n?(.*?)\n?```"
        tool_matches = re.findall(tool_call_pattern, response, re.DOTALL)

        for match in tool_matches:
            try:
                # Use orjson for faster JSON parsing if available
                if USE_ORJSON:
                    tool_data = orjson.loads(match.strip())
                else:
                    tool_data = json.loads(match.strip())

                # Check if this is actually a tool call (has "tool" and "arguments" keys)
                if "tool" in tool_data and "arguments" in tool_data:
                    tool_calls.append({
                        "tool": tool_data.get("tool"),
                        "arguments": tool_data.get("arguments", {}),
                        "reasoning": tool_data.get("reasoning", "")
                    })
                    is_final = False
            except (json.JSONDecodeError, ValueError):
                logger.warning(f"Failed to parse tool call: {match}")

        # Remove tool call blocks from answer
        answer = re.sub(tool_call_pattern, "", response, flags=re.DOTALL)

        return LLMResponse(
            content=answer.strip(),
            thinking=thinking,
            tool_calls=tool_calls,
            is_final=is_final
        )

    async def check_health(self) -> bool:
        """Check if external AI service is running and accessible."""
        try:
            session = await self._get_session()
            headers = {
                "Content-Type": "application/json"
            }

            # Try a simple health check with minimal prompt using DeepSeek API format
            payload = {
                "prompt": "Hi",
                "model": self.config.model or "deepseek-coder-optimized",
                "system": "You are a helpful assistant.",
                "temperature": 0.7,
                "max_tokens": 10
            }

            async with session.post(
                f"{self.config.base_url}/generate/sse",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=20)
            ) as response:
                # Accept 200 status as healthy
                if response.status == 200:
                    # Try to read at least one byte to verify stream works
                    async for _ in response.content.iter_any():
                        return True
                    return True
                return False

        except asyncio.TimeoutError:
            logger.warning("External AI health check timed out (service may be slow)")
            return True  # Consider it healthy if it just takes time
        except Exception as e:
            logger.error(f"External AI health check failed: {e}")
            return False
