#!/usr/bin/env python3
"""
Test External AI Integration

Quick script to test the external AI service connection.
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devo.settings.base')
import django
django.setup()

from apps.llm.clients.external import ExternalAIClient, ExternalAIConfig


async def test_external_ai():
    """Test the external AI service."""
    print("=" * 60)
    print("Testing External AI Service")
    print("=" * 60)

    # Create client with configuration
    config = ExternalAIConfig(
        model='default',
        base_url='http://41.33.142.254:8080',
        api_key='sk-test-123456'
    )

    client = ExternalAIClient(config)

    try:
        # Test 1: Health check
        print("\n1. Testing health check...")
        is_healthy = await client.check_health()
        print(f"   Health check: {'✓ PASSED' if is_healthy else '✗ FAILED'}")

        if not is_healthy:
            print("\n   The external AI service appears to be unavailable.")
            print("   Please check:")
            print("   - The service is running at http://41.33.142.254:8080")
            print("   - The API key is correct: sk-test-123456")
            print("   - Network connectivity to the service")
            return

        # Test 2: Simple generation
        print("\n2. Testing simple generation...")
        prompt = "Say 'Hello, World!' and nothing else."
        print(f"   Prompt: {prompt}")

        response = await client.generate(
            prompt=prompt,
            temperature=0.7
        )

        print(f"   Response: {response[:100]}...")
        print("   ✓ Generation test PASSED")

        # Test 3: Streaming
        print("\n3. Testing streaming generation...")
        prompt = "Count from 1 to 5"
        print(f"   Prompt: {prompt}")
        print("   Streamed response: ", end="")

        full_response = ""
        async for chunk in client.generate_stream(prompt=prompt):
            print(chunk, end="", flush=True)
            full_response += chunk

        print()
        print("   ✓ Streaming test PASSED")

        # Test 4: Parse response
        print("\n4. Testing response parsing...")
        parsed = client.parse_response(full_response)
        print(f"   Content: {parsed.content[:100]}...")
        print(f"   Thinking: {parsed.thinking[:50] if parsed.thinking else 'None'}...")
        print(f"   Tool calls: {len(parsed.tool_calls)}")
        print("   ✓ Parsing test PASSED")

        print("\n" + "=" * 60)
        print("All tests PASSED! ✓")
        print("=" * 60)
        print("\nThe external AI service is working correctly.")
        print("Your application is now configured to use it.")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print("\nPlease check:")
        print("- Service URL: http://41.33.142.254:8080/llm/api/generate")
        print("- API Key: sk-test-123456")
        print("- Network connectivity")
        import traceback
        traceback.print_exc()

    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.run(test_external_ai())
