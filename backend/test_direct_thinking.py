#!/usr/bin/env python3
"""Direct test of thinking mode with external AI."""

import asyncio
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.external_ai_client import ExternalAIClient, ExternalAIConfig

async def test_thinking_mode():
    """Test thinking mode directly with external AI."""

    print("\n" + "="*60)
    print("Testing Thinking Mode with External AI Service")
    print("="*60 + "\n")

    # Initialize client
    config = ExternalAIConfig(
        base_url="http://34.136.165.200:8000"
    )
    client = ExternalAIClient(config)

    prompt = "Write a simple Python function to calculate the sum of two numbers"
    system = "You are a helpful AI assistant."

    print(f"Prompt: {prompt}")
    print(f"System: {system}")
    print("\n" + "-"*40 + "\n")

    print("Testing with thinking_mode=True:")
    thinking_events = []
    content_events = []
    in_thinking = False

    try:
        async for event in client.generate_stream(
            prompt=prompt,
            system=system,
            thinking_mode=True,
            max_tokens=500
        ):
            if event['type'] == 'thinking_start':
                print("🧠 [THINKING START]")
                in_thinking = True
            elif event['type'] == 'thinking':
                content = event.get('content', '')
                thinking_events.append(content)
                if len(''.join(thinking_events)) < 200:  # Only print first 200 chars
                    print(f"{content}", end='', flush=True)
            elif event['type'] == 'thinking_end':
                print("\n🧠 [THINKING END]\n")
                in_thinking = False
            elif event['type'] == 'content':
                content = event.get('content', '')
                content_events.append(content)
                print(f"{content}", end='', flush=True)

        print("\n\n" + "-"*40)
        print(f"Results:")
        print(f"  - Thinking events: {len(thinking_events)}")
        print(f"  - Content events: {len(content_events)}")
        print(f"  - Total thinking: {len(''.join(thinking_events))} chars")
        print(f"  - Total content: {len(''.join(content_events))} chars")

        if thinking_events:
            print("\n✅ Thinking mode is working!")
            print("\n🧠 Sample thinking (first 300 chars):")
            print(''.join(thinking_events)[:300] + "...")
        else:
            print("\n⚠️ No thinking events received. The external AI might not support thinking mode yet.")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_thinking_mode())