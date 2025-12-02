#!/usr/bin/env python3
"""Test with minimal payload exactly like curl."""

import asyncio
import json
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_minimal():
    """Test with minimal payload."""

    url = "http://34.136.165.200:8000/generate/sse"

    # Exact same payload as curl
    payload = {
        "prompt": "Write hello world in Python",
        "think": True  # Try with capital T
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"Sending minimal payload: {json.dumps(payload)}")
    print("=" * 60)

    async with httpx.AsyncClient(timeout=30) as client:
        async with client.stream('POST', url, json=payload, headers=headers) as response:
            print(f"Status: {response.status_code}")

            event_count = 0
            thinking_count = 0

            async for line in response.aiter_lines():
                if line.startswith('data: '):
                    event_count += 1
                    data_str = line[6:]

                    if event_count <= 10:
                        print(f"Line {event_count}: {line[:80]}")

                    try:
                        if data_str and data_str != '[DONE]':
                            data = json.loads(data_str)
                            if data.get('type') == 'thinking':
                                thinking_count += 1
                    except:
                        pass

                    if event_count > 100:
                        break

            print(f"\nReceived {thinking_count} thinking events out of {event_count} total")

if __name__ == "__main__":
    asyncio.run(test_minimal())