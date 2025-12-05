"""
Test script for AI Inference Service API
"""
import requests
import json

BASE_URL = "http://localhost:7000"


def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_chat_completion():
    """Test chat completions endpoint"""
    print("Testing /v1/chat/completions endpoint...")
    
    data = {
        "model": "mistral-7b",
        "messages": [
            {"role": "user", "content": "Write a Python function to calculate fibonacci numbers"}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/chat/completions",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Generated text:")
        print(result['choices'][0]['message']['content'])
        print(f"\nToken usage: {result['usage']}")
    else:
        print(f"Error: {response.text}")
    print()


def test_completion():
    """Test completions endpoint"""
    print("Testing /v1/completions endpoint...")
    
    data = {
        "model": "mistral-7b",
        "prompt": "The capital of France is",
        "temperature": 0.3,
        "max_tokens": 50
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/completions",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Generated text: {result['choices'][0]['text']}")
        print(f"Token usage: {result['usage']}")
    else:
        print(f"Error: {response.text}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("AI Inference Service - API Tests")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_chat_completion()
        test_completion()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to service at", BASE_URL)
        print("Make sure the service is running with: python run.py")
    except Exception as e:
        print(f"ERROR: {str(e)}")
