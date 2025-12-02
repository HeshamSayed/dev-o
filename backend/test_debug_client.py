#!/usr/bin/env python3
"""Debug external AI client SSE parsing."""

import json
import logging
import asyncio
from typing import Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class ExternalAIConfig:
    """External AI service configuration."""
    base_url: str = "http://34.136.165.200:8000"
    api_key: str = "sk-test-123456"
    model: str = "deepseek-coder-optimized"
    default_max_tokens: int = 4096
    default_system_prompt: str = "You are DEV-O, an expert AI coding assistant."
    timeout: int = 120


class DebugExternalAIClient:
    """Debug client for External AI API with SSE streaming support."""

    def __init__(self, config: Optional[ExternalAIConfig] = None):
        self.config = config or ExternalAIConfig()
        self.executor = ThreadPoolExecutor(max_workers=2)

    def _stream_request(self, payload: Dict, headers: Dict) -> requests.Response:
        """Make a streaming request using requests library."""
        return requests.post(
            f"{self.config.base_url}/generate/sse",
            json=payload,
            headers=headers,
            stream=True,
            timeout=(5, None)
        )

    async def generate_stream(
        self,
        prompt: str,
        thinking_mode: bool = False,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate a response with streaming via SSE."""

        payload = {
            "prompt": prompt,
            "think": thinking_mode,
        }

        headers = {
            "Content-Type": "application/json"
        }

        logger.info(f"Sending request with thinking_mode={thinking_mode}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")

        try:
            # Run the blocking request in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self.executor,
                self._stream_request,
                payload,
                headers
            )

            response.raise_for_status()

            line_count = 0
            # Process SSE stream
            for line in response.iter_lines():
                line_count += 1
                if not line:
                    logger.debug(f"Line {line_count}: [empty line]")
                    continue

                line_str = line.decode('utf-8').strip()
                logger.debug(f"Line {line_count}: {line_str[:100]}")

                # SSE format: "data: {json}"
                if line_str.startswith('data: '):
                    data_str = line_str[6:]  # Remove "data: " prefix

                    # Skip SSE comments, empty lines, and [DONE] marker
                    if not data_str or data_str.startswith(':') or data_str == '[DONE]':
                        logger.debug(f"  -> Skipping: {data_str}")
                        continue

                    try:
                        data = json.loads(data_str)
                        logger.debug(f"  -> Parsed: {data}")

                        # Handle different event types
                        event_type = data.get("type")

                        if event_type == "thinking_start":
                            logger.info("*** FOUND thinking_start event ***")
                            yield {"type": "thinking_start"}
                        elif event_type == "thinking":
                            content = data.get("content", "")
                            logger.info(f"*** FOUND thinking event: {content[:30]}... ***")
                            yield {"type": "thinking", "content": content}
                        elif event_type == "thinking_end":
                            logger.info("*** FOUND thinking_end event ***")
                            yield {"type": "thinking_end"}
                        elif event_type == "content" or "content" in data:
                            # Normal content streaming
                            yield {"type": "content", "content": data.get("content", "")}

                        # Check for completion
                        if data.get("done") or data.get("finished"):
                            logger.info("Stream complete")
                            break

                        # Allow other async tasks to run
                        await asyncio.sleep(0)

                        if line_count > 100:
                            logger.info("Stopping after 100 lines")
                            break

                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse: {data_str[:100]}, error: {e}")
                        continue

            response.close()

        except Exception as e:
            logger.error(f"Error: {e}")
            raise


async def test_debug_client():
    """Test the debug client."""

    client = DebugExternalAIClient()

    print("\n" + "=" * 60)
    print("Testing Debug External AI Client with thinking mode...")
    print("=" * 60 + "\n")

    thinking_events = 0
    content_events = 0
    total_events = 0

    async for chunk in client.generate_stream(
        prompt="Write hello world in Python",
        thinking_mode=True
    ):
        total_events += 1

        if chunk.get('type') == 'thinking':
            thinking_events += 1
        elif chunk.get('type') == 'content':
            content_events += 1

    print("\n" + "=" * 60)
    print(f"Total events: {total_events}")
    print(f"Thinking events: {thinking_events}")
    print(f"Content events: {content_events}")


if __name__ == "__main__":
    asyncio.run(test_debug_client())