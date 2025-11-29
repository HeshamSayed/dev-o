"""
Ollama Client

Client for interacting with locally-running LLMs via Ollama.
Optimized for DeepSeek-R1 models.
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass

import aiohttp

from .base import BaseLLMClient, LLMConfig, LLMResponse

logger = logging.getLogger(__name__)


@dataclass
class OllamaConfig(LLMConfig):
    """Ollama-specific configuration."""
    base_url: str = "http://localhost:11434"
    num_ctx: int = 32768  # Context window size


class OllamaClient(BaseLLMClient):
    """
    Client for Ollama API.

    Supports:
    - Streaming and non-streaming generation
    - Tool/function calling (via prompt engineering)
    - DeepSeek R1 thinking extraction
    - Context window management
    """

    def __init__(self, config: Optional[OllamaConfig] = None):
        self.config = config or OllamaConfig(model='deepseek-r1:7b')
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            # Use separate timeouts: connect fast, but allow long read for streaming
            timeout = aiohttp.ClientTimeout(
                total=None,  # No total timeout for streaming
                connect=10,  # 10 seconds to connect
                sock_read=60  # 60 seconds between chunks
            )
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
    ) -> str:
        """
        Generate a response (non-streaming).

        Args:
            prompt: User prompt
            system: System prompt
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            tools: Tool definitions (will be added to prompt)

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
    ) -> AsyncGenerator[str, None]:
        """
        Generate a response with streaming.

        Yields chunks of generated text as they arrive.
        """
        logger.info(f"[Ollama] generate_stream called!")
        session = await self._get_session()
        logger.info(f"[Ollama] Session obtained!")

        # Build full prompt with tools if provided
        full_prompt = prompt
        if tools:
            full_prompt = self._add_tools_to_prompt(prompt, tools)

        # Build request payload
        payload = {
            "model": self.config.model,
            "prompt": full_prompt,
            "stream": True,
            "keep_alive": "10m",  # Keep model loaded for 10 minutes
            "options": {
                "temperature": temperature,
                "num_ctx": self.config.num_ctx,
                "num_predict": max_tokens or 512,  # Limit tokens for faster responses
            }
        }

        if system:
            payload["system"] = system

        try:
            logger.info(f"[Ollama] Calling API: {self.config.base_url}/api/generate with model {self.config.model}")
            logger.info(f"[Ollama] Payload: prompt_len={len(full_prompt)}, system_len={len(system) if system else 0}")

            async with session.post(
                f"{self.config.base_url}/api/generate",
                json=payload
            ) as response:
                logger.info(f"[Ollama] Response status: {response.status}")
                response.raise_for_status()

                chunk_count = 0
                logger.info(f"[Ollama] Starting to read response stream...")
                async for line in response.content:
                    if line:
                        try:
                            data = json.loads(line)
                            if "response" in data:
                                chunk_count += 1
                                if chunk_count == 1:
                                    logger.info(f"[Ollama] First chunk received!")
                                yield data["response"]
                            if data.get("done"):
                                logger.info(f"[Ollama] Streaming complete. Sent {chunk_count} chunks")
                                break
                        except json.JSONDecodeError as json_err:
                            logger.warning(f"[Ollama] JSON decode error: {json_err}")
                            continue

        except aiohttp.ClientError as e:
            logger.error(f"[Ollama] Request failed: {e}")
            raise
        except Exception as e:
            logger.exception(f"[Ollama] Unexpected error: {e}")
            raise

    def _add_tools_to_prompt(
        self,
        prompt: str,
        tools: List[Dict]
    ) -> str:
        """
        Add tool definitions to the prompt.

        Since Ollama doesn't natively support function calling,
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
                tool_data = json.loads(match.strip())

                # Check if this is actually a tool call (has "tool" and "arguments" keys)
                if "tool" in tool_data and "arguments" in tool_data:
                    tool_calls.append({
                        "tool": tool_data.get("tool"),
                        "arguments": tool_data.get("arguments", {}),
                        "reasoning": tool_data.get("reasoning", "")
                    })
                    is_final = False
            except json.JSONDecodeError:
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
        """Check if Ollama is running and accessible."""
        try:
            session = await self._get_session()
            async with session.get(f"{self.config.base_url}/api/tags") as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False

    async def list_models(self) -> List[str]:
        """List available models."""
        session = await self._get_session()
        async with session.get(f"{self.config.base_url}/api/tags") as response:
            response.raise_for_status()
            data = await response.json()
            return [model["name"] for model in data.get("models", [])]

    async def pull_model(self, model: str) -> AsyncGenerator[Dict, None]:
        """Pull a model with progress."""
        session = await self._get_session()

        async with session.post(
            f"{self.config.base_url}/api/pull",
            json={"name": model, "stream": True}
        ) as response:
            async for line in response.content:
                if line:
                    try:
                        data = json.loads(line)
                        yield data
                    except json.JSONDecodeError:
                        continue
