#!/usr/bin/env python3
"""Test thinking mode integration in Django."""

import os
import sys
import django
import asyncio

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.ai_service import AIService
from services.external_ai_client import ExternalAIClient, ExternalAIConfig

async def test_thinking_mode():
    """Test thinking mode with AI service."""

    print("\n" + "="*60)
    print("Testing Thinking Mode Integration")
    print("="*60 + "\n")

    # Initialize AI service
    ai_service = AIService()

    # Test messages
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Write a simple hello world function in Python."}
    ]

    print("Testing with thinking_mode=True:")
    print("-" * 40)

    thinking_events = []
    content_events = []

    try:
        async for chunk in ai_service.stream_chat(messages, thinking_mode=True):
            if chunk['type'] == 'thinking_start':
                print("🧠 [THINKING START]")
            elif chunk['type'] == 'thinking':
                thinking_events.append(chunk.get('content', ''))
                print(f"🧠 THINKING: {chunk.get('content', '')[:50]}...")
            elif chunk['type'] == 'thinking_end':
                print("🧠 [THINKING END]")
            elif chunk['type'] == 'content':
                content_events.append(chunk.get('content', ''))
                # Don't print all content, just track it
            elif chunk['type'] == 'done':
                print("✅ [DONE]")
                break
            elif chunk['type'] == 'error':
                print(f"❌ ERROR: {chunk.get('error', 'Unknown error')}")
                break
    except Exception as e:
        print(f"❌ Exception: {e}")

    print(f"\nResults:")
    print(f"  - Thinking chunks: {len(thinking_events)}")
    print(f"  - Content chunks: {len(content_events)}")
    print(f"  - Total thinking length: {len(''.join(thinking_events))} chars")
    print(f"  - Total content length: {len(''.join(content_events))} chars")

    print("\n" + "="*60)
    print("Testing with thinking_mode=False:")
    print("-" * 40)

    content_events_no_thinking = []

    try:
        async for chunk in ai_service.stream_chat(messages, thinking_mode=False):
            if chunk['type'] == 'content':
                content_events_no_thinking.append(chunk.get('content', ''))
            elif chunk['type'] == 'done':
                print("✅ [DONE]")
                break
            elif chunk['type'] == 'error':
                print(f"❌ ERROR: {chunk.get('error', 'Unknown error')}")
                break
    except Exception as e:
        print(f"❌ Exception: {e}")

    print(f"\nResults (without thinking):")
    print(f"  - Content chunks: {len(content_events_no_thinking)}")
    print(f"  - Total content length: {len(''.join(content_events_no_thinking))} chars")

    # Test health check
    print("\n" + "="*60)
    print("Testing External AI Service Health Check:")
    print("-" * 40)

    client = ExternalAIClient()
    is_healthy = await client.check_health()
    print(f"Service health: {'✅ HEALTHY' if is_healthy else '❌ UNHEALTHY'}")

    print("\n" + "="*60)
    print("Test Complete!")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(test_thinking_mode())