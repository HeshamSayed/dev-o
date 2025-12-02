#!/usr/bin/env python3
"""Test aiohttp SSE directly."""

import asyncio
import aiohttp
import json

async def test_sse_aiohttp():
    """Test SSE with aiohttp directly."""

    url = "http://34.136.165.200:8000/generate/sse"
    payload = {
        "prompt": "Write hello world in Python",
        "think": True
    }

    print(f"Testing with aiohttp")
    print(f"Payload: {json.dumps(payload)}")
    print("=" * 60)

    timeout = aiohttp.ClientTimeout(total=10, connect=5, sock_read=None)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, json=payload) as response:
            print(f"Status: {response.status}")
            print("\nFirst events:")
            print("-" * 40)

            buffer = b""
            event_count = 0
            thinking_count = 0

            async for chunk in response.content.iter_any():
                buffer += chunk

                # Process complete lines
                while b'\n' in buffer:
                    line, buffer = buffer.split(b'\n', 1)
                    line_str = line.decode('utf-8').strip()

                    if line_str and event_count < 20:
                        print(f"{event_count+1}: {line_str[:80]}")

                        if 'thinking' in line_str:
                            thinking_count += 1

                    event_count += 1
                    if event_count >= 20:
                        break

                if event_count >= 20:
                    break

            print(f"\nFound {thinking_count} thinking-related lines in first {event_count} lines")

if __name__ == "__main__":
    asyncio.run(test_sse_aiohttp())