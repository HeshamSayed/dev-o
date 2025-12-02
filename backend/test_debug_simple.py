#!/usr/bin/env python3
"""Debug test for simple external AI client."""

import asyncio
import sys
import os
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

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
        print("Creating generator...")
        generator = client.generate_stream(
            prompt="Write hello world in Python",
            thinking_mode=True
        )

        print("Starting iteration...")
        async for chunk in generator:
            total_events += 1
            print(f"Got chunk: {chunk}")

            if chunk.get('type') == 'thinking':
                thinking_events += 1
            elif chunk.get('type') == 'content':
                content_events += 1

            if total_events >= 50:
                break

    except Exception as e:
        print(f"Exception in test: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"Total events: {total_events}")
    print(f"Thinking events: {thinking_events}")
    print(f"Content events: {content_events}")

if __name__ == "__main__":
    print("Starting test...")
    asyncio.run(test_client())
    print("Test complete.")