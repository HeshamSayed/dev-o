#!/usr/bin/env python3
"""Test simple external AI client."""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.external_ai_client_simple import ExternalAIClient

async def test_client():
    """Test the simple external AI client."""

    client = ExternalAIClient()

    print("Testing Simple External AI Client with thinking mode...")
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

            if chunk.get('type') == 'thinking_start':
                print("\n*** THINKING START ***")
            elif chunk.get('type') == 'thinking':
                thinking_events += 1
                if thinking_events <= 5:
                    print(f"Thinking {thinking_events}: {chunk.get('content', '')}")
            elif chunk.get('type') == 'thinking_end':
                print("*** THINKING END ***\n")
            elif chunk.get('type') == 'content':
                content_events += 1
                if content_events <= 5:
                    print(f"Content {content_events}: {chunk.get('content', '')}")

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