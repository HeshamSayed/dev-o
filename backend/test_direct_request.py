#!/usr/bin/env python3
"""Direct test of the SSE request."""

import requests
import json

def test_direct():
    """Test SSE request directly."""

    url = "http://34.136.165.200:8000/generate/sse"
    payload = {
        "prompt": "Write hello world in Python",
        "think": True,
        "model": "deepseek-coder-optimized",
        "temperature": 0.7,
        "max_tokens": 4096,
        "system": "You are DEV-O, an expert AI coding assistant."
    }

    headers = {"Content-Type": "application/json"}

    print(f"Sending: {json.dumps(payload)}")
    print("=" * 60)

    events = []
    response = requests.post(url, json=payload, headers=headers, stream=True, timeout=(5, None))
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str and data_str != '[DONE]' and not data_str.startswith(':'):
                        try:
                            data = json.loads(data_str)
                            events.append(data)
                            if len(events) <= 10:
                                print(f"Event {len(events)}: {data}")
                        except json.JSONDecodeError as e:
                            print(f"Parse error: {e} for {data_str[:50]}")

            if len(events) >= 100:
                break

        response.close()

    print(f"\nTotal events collected: {len(events)}")
    thinking_events = sum(1 for e in events if e.get('type') == 'thinking')
    content_events = sum(1 for e in events if e.get('type') == 'content')
    print(f"Thinking events: {thinking_events}")
    print(f"Content events: {content_events}")

    return events

if __name__ == "__main__":
    events = test_direct()
    print(f"\nReturned {len(events)} events")