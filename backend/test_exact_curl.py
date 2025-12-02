#!/usr/bin/env python3
"""Test with exact same format as curl."""

import requests
import json

def test_exact():
    """Test with minimal payload like curl."""

    url = "http://34.136.165.200:8000/generate/sse"

    # Minimal payload exactly like curl that worked
    payload = {
        "prompt": "Write hello world in Python",
        "think": True  # This becomes lowercase "true" in JSON
    }

    headers = {"Content-Type": "application/json"}

    print(f"Sending minimal payload: {json.dumps(payload)}")
    print("=" * 60)

    events = []
    response = requests.post(url, json=payload, headers=headers, stream=True, timeout=(5, None))
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        event_count = 0
        for line in response.iter_lines():
            event_count += 1
            if line:
                line_str = line.decode('utf-8').strip()
                if event_count <= 20:
                    print(f"Line {event_count}: {line_str[:80]}")

                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str and data_str != '[DONE]' and not data_str.startswith(':'):
                        try:
                            data = json.loads(data_str)
                            events.append(data)
                        except json.JSONDecodeError:
                            pass

            if event_count >= 100:
                break

        response.close()

    print(f"\nEvent types found:")
    event_types = {}
    for e in events:
        event_type = e.get('type', 'no_type')
        event_types[event_type] = event_types.get(event_type, 0) + 1
    for event_type, count in event_types.items():
        print(f"  {event_type}: {count}")

if __name__ == "__main__":
    test_exact()