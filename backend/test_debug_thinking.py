#!/usr/bin/env python3
"""Debug test for thinking mode."""

import asyncio
import json
import httpx

async def test_thinking_debug():
    """Debug test to see raw SSE data."""

    print("Testing raw SSE response...")
    print("="*60)

    payload = {
        "prompt": "Write hello world in Python",
        "think": True,  # Note: capital T
        "model": "deepseek-coder-optimized",
        "temperature": 0.7,
        "max_tokens": 500
    }

    headers = {
        "Content-Type": "application/json"
    }

    print(f"Payload: {json.dumps(payload, indent=2)}")
    print("\nRaw SSE Events:")
    print("-"*40)

    async with httpx.AsyncClient(timeout=30) as client:
        async with client.stream(
            'POST',
            "http://34.136.165.200:8000/generate/sse",
            json=payload,
            headers=headers
        ) as response:
            response.raise_for_status()

            event_count = 0
            async for line in response.aiter_lines():
                if line.startswith('data: '):
                    event_count += 1
                    data_str = line[6:]

                    if event_count <= 10:  # Show first 10 events
                        print(f"Event {event_count}: {data_str[:100]}")

                    if data_str and data_str != '[DONE]':
                        try:
                            data = json.loads(data_str)
                            event_type = data.get("type")

                            if event_type and event_count <= 10:
                                print(f"  -> Type: {event_type}, Has content: {'content' in data}")
                        except:
                            pass

                    if event_count > 50:  # Stop after 50 events
                        break

    print(f"\nTotal events received: {event_count}")

if __name__ == "__main__":
    asyncio.run(test_thinking_debug())