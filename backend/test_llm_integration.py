#!/usr/bin/env python
"""
Test LLM Integration with External AI

Run this inside the Django environment to test the external AI service.
"""

import os
import sys
import django
import asyncio

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devo.settings.base')
django.setup()

from apps.llm.services.llm_service import LLMService
from django.conf import settings


async def test_external_ai():
    """Test the external AI integration."""
    print("=" * 60)
    print("Testing DeepSeek Coder Integration")
    print("=" * 60)

    # Check configuration
    print("\nConfiguration:")
    print(f"  USE_EXTERNAL_AI: {settings.DEVO_SETTINGS.get('USE_EXTERNAL_AI', False)}")
    print(f"  EXTERNAL_AI_BASE_URL: {settings.DEVO_SETTINGS.get('EXTERNAL_AI_BASE_URL', 'Not set')}")
    print(f"  EXTERNAL_AI_MODEL: {settings.DEVO_SETTINGS.get('EXTERNAL_AI_MODEL', 'Not set')}")
    print(f"  DEFAULT_LLM_MODEL: {settings.DEVO_SETTINGS.get('DEFAULT_LLM_MODEL', 'Not set')}")
    print(f"\nDeepSeek Parameters:")
    print(f"  Temperature: {settings.DEVO_SETTINGS.get('DEEPSEEK_TEMPERATURE', 'Not set')}")
    print(f"  Top-p: {settings.DEVO_SETTINGS.get('DEEPSEEK_TOP_P', 'Not set')}")
    print(f"  Top-k: {settings.DEVO_SETTINGS.get('DEEPSEEK_TOP_K', 'Not set')}")
    print(f"  Repeat Penalty: {settings.DEVO_SETTINGS.get('DEEPSEEK_REPEAT_PENALTY', 'Not set')}")
    print(f"  Context Size: {settings.DEVO_SETTINGS.get('DEEPSEEK_NUM_CTX', 'Not set')}")
    print(f"  Max Tokens: {settings.DEVO_SETTINGS.get('DEEPSEEK_MAX_TOKENS', 'Not set')}")

    # Create LLM service
    llm = LLMService()

    print(f"\nClient Type: {llm.client.__class__.__name__}")
    print(f"Client Module: {llm.client.__class__.__module__}")

    try:
        # Test 1: Health Check
        print("\n" + "-" * 60)
        print("Test 1: Health Check")
        print("-" * 60)
        is_healthy = await llm.check_health()
        print(f"Result: {'✓ HEALTHY' if is_healthy else '✗ UNHEALTHY'}")

        if not is_healthy:
            print("\nExternal AI service is not responding.")
            print("Please verify:")
            print("  - Service is running at the configured URL")
            print("  - API key is correct")
            print("  - Network connectivity")
            await llm.close()
            return

        # Test 2: Simple Generation
        print("\n" + "-" * 60)
        print("Test 2: Simple Text Generation")
        print("-" * 60)
        prompt = "Say 'Hello from external AI!' and nothing else."
        print(f"Prompt: {prompt}")
        print("\nGenerating response...")

        response = await llm.generate(
            prompt=prompt,
            temperature=0.7
        )

        print(f"\nResponse:")
        print(f"  Content: {response.content}")
        print(f"  Thinking: {response.thinking[:100] if response.thinking else 'None'}")
        print(f"  Tool calls: {len(response.tool_calls)}")
        print(f"  Is final: {response.is_final}")

        # Test 3: Streaming
        print("\n" + "-" * 60)
        print("Test 3: Streaming Generation")
        print("-" * 60)
        prompt = "Count from 1 to 3"
        print(f"Prompt: {prompt}")
        print("\nStreaming response: ", end="", flush=True)

        full_response = ""
        async for chunk in llm.generate_stream(prompt=prompt):
            print(chunk, end="", flush=True)
            full_response += chunk

        print(f"\n\nFull response length: {len(full_response)} characters")

        # Test 4: Code Generation (DeepSeek Coder specific)
        print("\n" + "-" * 60)
        print("Test 4: Code Generation (DeepSeek Coder)")
        print("-" * 60)
        code_prompt = "Write a Python function to calculate fibonacci numbers"
        print(f"Prompt: {code_prompt}")
        print("\nGenerating code...")

        response = await llm.generate(
            prompt=code_prompt,
            system="You are DeepSeek Coder, an expert programming assistant. Provide clear, efficient code.",
            temperature=0.7,
            max_tokens=500
        )

        print(f"\nResponse:")
        print(f"  {response.content[:500]}...")
        print(f"  Is final: {response.is_final}")

        print("\n" + "=" * 60)
        print("✓ All Tests PASSED!")
        print("=" * 60)
        print("\nThe DeepSeek Coder API is working correctly with DEV-O!")
        print("\nNext steps:")
        print("  1. Agents (Alex, Sarah, Marcus, Elena) will now use DeepSeek Coder")
        print("  2. Test the chat interface: /ws/projects/{id}/chat/")
        print("  3. Verify agent responses use DeepSeek for code generation")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await llm.close()


if __name__ == '__main__':
    asyncio.run(test_external_ai())
