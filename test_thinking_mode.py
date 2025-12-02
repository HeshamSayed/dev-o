#!/usr/bin/env python3
"""Test script for thinking mode feature."""

import asyncio
import json
import httpx
import sys

# Configuration
API_URL = "http://34.136.165.200:8000"
ENDPOINT = "/generate/sse"

async def test_thinking_mode(thinking_enabled=True):
    """Test the thinking mode feature."""

    print(f"\n{'='*60}")
    print(f"Testing with thinking mode: {thinking_enabled}")
    print(f"{'='*60}\n")

    payload = {
        "prompt": "Write a simple Python function to calculate factorial",
        "think": thinking_enabled,
        "model": "deepseek-coder-optimized",
        "temperature": 0.7,
        "max_tokens": 500
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            async with client.stream(
                'POST',
                f"{API_URL}{ENDPOINT}",
                json=payload,
                headers=headers
            ) as response:
                response.raise_for_status()

                thinking_content = []
                response_content = []
                current_mode = None

                async for line in response.aiter_lines():
                    if line.startswith('data: '):
                        data_str = line[6:]

                        if not data_str or data_str == '[DONE]':
                            continue

                        try:
                            data = json.loads(data_str)
                            event_type = data.get('type')

                            if event_type == 'thinking_start':
                                current_mode = 'thinking'
                                print("🧠 [THINKING START]")

                            elif event_type == 'thinking':
                                content = data.get('content', '')
                                thinking_content.append(content)
                                print(f"{content}", end='', flush=True)

                            elif event_type == 'thinking_end':
                                current_mode = 'response'
                                print("\n🧠 [THINKING END]\n")

                            elif event_type == 'content' or 'content' in data:
                                if current_mode != 'response' and thinking_enabled:
                                    print("\n💬 [RESPONSE START]")
                                    current_mode = 'response'
                                content = data.get('content', '')
                                response_content.append(content)
                                print(f"{content}", end='', flush=True)

                            elif data.get('done'):
                                print("\n\n✅ [COMPLETE]")
                                break

                        except json.JSONDecodeError as e:
                            print(f"\n⚠️ Failed to parse: {data_str[:100]}...")

                print(f"\n{'='*60}")
                print("Summary:")
                if thinking_content:
                    print(f"  - Thinking: {len(''.join(thinking_content))} characters")
                print(f"  - Response: {len(''.join(response_content))} characters")
                print(f"{'='*60}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

async def main():
    """Run tests."""
    # Test with thinking mode enabled
    await test_thinking_mode(thinking_enabled=True)

    print("\n\n")

    # Test with thinking mode disabled
    await test_thinking_mode(thinking_enabled=False)

if __name__ == "__main__":
    print("Testing Thinking Mode Feature")
    print("==============================")
    asyncio.run(main())