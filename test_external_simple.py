#!/usr/bin/env python3
"""
Simple External AI Test (without Django)

Tests the external AI service directly using aiohttp.
"""

import asyncio
import json
import aiohttp


async def test_external_ai():
    """Test the external AI service."""
    print("=" * 60)
    print("Testing External AI Service")
    print("=" * 60)

    base_url = "http://41.33.142.254:8080"
    api_key = "sk-test-123456"

    async with aiohttp.ClientSession() as session:
        try:
            # Test streaming generation
            print("\nTesting streaming generation...")
            print("Prompt: 'Say hello in 5 words or less'")
            print("\nStreaming response: ", end="", flush=True)

            payload = {
                "prompt": "Say hello in 5 words or less",
                "stream": True,
                "format": "sse"
            }

            headers = {
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            }

            full_response = ""
            timeout = aiohttp.ClientTimeout(total=30)

            async with session.post(
                f"{base_url}/llm/api/generate",
                json=payload,
                headers=headers,
                timeout=timeout
            ) as response:
                if response.status != 200:
                    print(f"\n✗ ERROR: HTTP {response.status}")
                    text = await response.text()
                    print(f"Response: {text}")
                    return

                # Parse SSE stream
                buffer = b""
                async for chunk in response.content.iter_any():
                    buffer += chunk

                    # Process complete lines
                    while b'\n' in buffer:
                        line, buffer = buffer.split(b'\n', 1)
                        line_str = line.decode('utf-8').strip()

                        # SSE format: "data: {json}"
                        if line_str.startswith('data: '):
                            data_str = line_str[6:]  # Remove "data: " prefix

                            if not data_str or data_str.startswith(':'):
                                continue

                            try:
                                data = json.loads(data_str)

                                # Extract response content
                                if "response" in data:
                                    text_chunk = data["response"]
                                    print(text_chunk, end="", flush=True)
                                    full_response += text_chunk

                                # Check for completion
                                if data.get("done"):
                                    break

                            except json.JSONDecodeError as e:
                                print(f"\n✗ JSON parse error: {e}")
                                continue

            print("\n")
            print("=" * 60)
            print("✓ Test PASSED!")
            print("=" * 60)
            print(f"\nFull response: {full_response}")
            print(f"Response length: {len(full_response)} characters")
            print("\nThe external AI service is working correctly!")
            print("Model: phi3:mini")
            print("Endpoint: http://41.33.142.254:8080/llm/api/generate")

        except asyncio.TimeoutError:
            print("\n✗ ERROR: Request timed out")
            print("The service is responding but taking too long.")
            print("This may be normal for first requests as the model loads.")

        except aiohttp.ClientError as e:
            print(f"\n✗ ERROR: {e}")
            print("\nPlease check:")
            print("- Service URL: http://41.33.142.254:8080/llm/api/generate")
            print("- API Key: sk-test-123456")
            print("- Network connectivity")

        except Exception as e:
            print(f"\n✗ ERROR: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(test_external_ai())
