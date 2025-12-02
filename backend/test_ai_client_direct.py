#!/usr/bin/env python3
"""Test external AI client directly."""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.external_ai_client import ExternalAIClient

async def test_client():
    """Test the external AI client directly."""

    client = ExternalAIClient()

    print("Testing External AI Client with thinking mode...")
    print("=" * 60)

    thinking_events = 0
    content_events = 0
    total_events = 0

    try:
        async for chunk in client.generate_stream(
            prompt="Write hello world in Python",
            thinking_mode=True
        ):
            total_events += 1

            if total_events <= 20:
                print(f"Event {total_events}: {chunk}")

            if chunk.get('type') == 'thinking':
                thinking_events += 1
            elif chunk.get('type') == 'content':
                content_events += 1

            if total_events >= 100:
                break

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"Total events: {total_events}")
    print(f"Thinking events: {thinking_events}")
    print(f"Content events: {content_events}")

if __name__ == "__main__":
    asyncio.run(test_client())