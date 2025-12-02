#!/usr/bin/env python3
"""Test which parameters break thinking mode."""

import requests
import json


def test_with_params(desc, payload):
    """Test with specific parameters."""
    url = "http://34.136.165.200:8000/generate/sse"
    headers = {"Content-Type": "application/json"}

    print(f"\nTesting: {desc}")
    print(f"Payload: {json.dumps(payload)}")

    response = requests.post(url, json=payload, headers=headers, stream=True, timeout=(5, None))

    if response.status_code == 200:
        event_types = {}
        count = 0
        for line in response.iter_lines():
            if count >= 50:
                break
            if line:
                line_str = line.decode('utf-8').strip()
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str and data_str != '[DONE]':
                        try:
                            data = json.loads(data_str)
                            event_type = data.get('type', 'no_type')
                            event_types[event_type] = event_types.get(event_type, 0) + 1
                            count += 1
                        except:
                            pass

        response.close()
        print(f"Event types: {event_types}")
        return 'thinking' in event_types


# Test different parameter combinations
tests = [
    ("Minimal (working)", {
        "prompt": "Write hello world",
        "think": True
    }),

    ("With model", {
        "prompt": "Write hello world",
        "think": True,
        "model": "deepseek-coder-optimized"
    }),

    ("With system", {
        "prompt": "Write hello world",
        "think": True,
        "system": "You are a helpful assistant"
    }),

    ("With temperature", {
        "prompt": "Write hello world",
        "think": True,
        "temperature": 0.7
    }),

    ("With max_tokens", {
        "prompt": "Write hello world",
        "think": True,
        "max_tokens": 100
    }),

    ("Model + temperature", {
        "prompt": "Write hello world",
        "think": True,
        "model": "deepseek-coder-optimized",
        "temperature": 0.7
    })
]

print("=" * 60)
print("Testing which parameters break thinking mode")
print("=" * 60)

for desc, payload in tests:
    has_thinking = test_with_params(desc, payload)
    print(f"Has thinking events: {has_thinking}")

print("\n" + "=" * 60)