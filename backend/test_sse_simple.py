#!/usr/bin/env python3
"""Simple SSE test with requests."""

import requests
import json

def test_sse():
    """Test SSE with requests library."""

    url = "http://34.136.165.200:8000/generate/sse"
    payload = {
        "prompt": "Write hello world in Python",
        "think": True
    }

    print(f"Sending: {json.dumps(payload)}")
    print("=" * 60)

    response = requests.post(url, json=payload, stream=True, timeout=(5, None))
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        print("\nFirst 20 SSE events:")
        print("-" * 40)

        count = 0
        thinking_events = 0

        try:
            for line in response.iter_lines():
                if count >= 20:
                    break

                if line:
                    line_str = line.decode('utf-8')
                    print(f"{count+1}: {line_str[:80]}")

                    if 'thinking' in line_str:
                        thinking_events += 1

                    count += 1

        except Exception as e:
            print(f"Stopped reading: {e}")

        print(f"\nFound {thinking_events} thinking-related events in first {count} events")

        response.close()

if __name__ == "__main__":
    test_sse()