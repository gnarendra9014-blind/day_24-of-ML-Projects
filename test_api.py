import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = "my-super-secret-key-2024"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

def test_health():
    res = requests.get(f"{BASE_URL}/health")
    print(f"Health: {res.json()}")

def test_complete():
    res = requests.post(f"{BASE_URL}/complete", headers=HEADERS, json={
        "prompt": "What is machine learning? Answer in 2 sentences.",
        "model": "llama-3.1-8b-instant",
        "max_tokens": 100
    })
    data = res.json()
    print(f"\nCompletion test:")
    if res.status_code != 200:
        print(f"  Error: {res.status_code} - {data}")
        return
    print(f"  Response: {data['response'][:80]}...")
    print(f"  Tokens: {data['tokens_used']}")
    print(f"  Latency: {data['latency_ms']}ms")

def test_chat():
    res = requests.post(f"{BASE_URL}/chat", headers=HEADERS, json={
        "messages": [
            {"role": "user", "content": "Hello! What can you do?"}
        ]
    })
    data = res.json()
    print(f"\nChat test:")
    if res.status_code != 200:
        print(f"  Error: {res.status_code} - {data}")
        return
    print(f"  Response: {data['response'][:80]}...")

def test_no_auth():
    res = requests.post(f"{BASE_URL}/complete", json={
        "prompt": "Hello"
    })
    print(f"\nNo auth test (should fail): {res.status_code} — {res.json()['detail']}")

def test_wrong_key():
    res = requests.post(f"{BASE_URL}/complete",
                       headers={"X-API-Key": "wrong-key"},
                       json={"prompt": "Hello"})
    print(f"Wrong key test (should fail): {res.status_code} — {res.json()['detail']}")

if __name__ == "__main__":
    print("=== Testing LLM API ===")
    test_health()
    test_no_auth()
    test_wrong_key()
    test_complete()
    test_chat()
    print("\nAll tests done!")
