#!/usr/bin/env python3
"""Test WebSocket thinking mode functionality."""

import asyncio
import json
import websockets
import sys

async def test_thinking_mode():
    """Test thinking mode via WebSocket."""

    # You'll need to get a valid token first
    # For testing, we'll use a dummy token
    token = "your_test_token_here"
    ws_url = f"wss://api.dev-o.ai/ws/chat/?token={token}"

    print("Testing WebSocket Thinking Mode...")
    print("=" * 60)

    try:
        async with websockets.connect(ws_url, ssl=True) as websocket:
            print("✅ Connected to WebSocket")

            # Wait for connected message
            response = await websocket.recv()
            print(f"Received: {response}")

            # Send a test message with thinking mode enabled
            message = {
                "type": "chat_message",
                "message": "Write a simple Python function to calculate factorial",
                "thinking_mode": True
            }

            print(f"\n📤 Sending message with thinking_mode=True:")
            print(f"   Message: {message['message']}")

            await websocket.send(json.dumps(message))

            print("\n📥 Receiving responses:")
            thinking_content = []
            response_content = []

            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    data = json.loads(response)

                    if data['type'] == 'thinking_start':
                        print("🧠 [THINKING START]")
                    elif data['type'] == 'thinking':
                        thinking_content.append(data.get('content', ''))
                        print(f"🧠 {data.get('content', '')[:50]}...")
                    elif data['type'] == 'thinking_end':
                        print("🧠 [THINKING END]")
                    elif data['type'] == 'token':
                        response_content.append(data.get('content', ''))
                        # Don't print each token
                    elif data['type'] == 'done':
                        print("✅ [DONE]")
                        break
                    elif data['type'] == 'error':
                        print(f"❌ Error: {data.get('error')}")
                        break

                except asyncio.TimeoutError:
                    print("⏱️ Timeout waiting for response")
                    break

            print("\n" + "=" * 60)
            print("Summary:")
            print(f"  Thinking content: {len(''.join(thinking_content))} chars")
            print(f"  Response content: {len(''.join(response_content))} chars")

            if thinking_content:
                print(f"\n🧠 Thinking Preview:")
                print(''.join(thinking_content)[:200] + "...")

            if response_content:
                print(f"\n💬 Response Preview:")
                print(''.join(response_content)[:200] + "...")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("WebSocket Thinking Mode Test")
    print("Note: This requires a valid auth token to work properly")
    asyncio.run(test_thinking_mode())