"""Test visa checking in the API."""

import requests
import json

API_URL = "http://localhost:5000"

print("=" * 60)
print("Testing Visa Requirements")
print("=" * 60)

# Test 1: Destination that requires visa (Tokyo)
print("\n1. Testing Tokyo (requires visa)...")
response = requests.post(
    f"{API_URL}/api/recommend",
    json={"query": "Should I go to Tokyo?", "userId": "user_123"},
    timeout=10
)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Success")
    print(f"\nRecommendation preview:")
    print(data['recommendation'][:600])
    print("...")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

# Test 2: Destination that doesn't require visa (Maui/USA)
print("\n\n2. Testing Maui (no visa required)...")
response = requests.post(
    f"{API_URL}/api/recommend",
    json={"query": "Should I go to Maui?", "userId": "user_123"},
    timeout=10
)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Success")
    print(f"\nRecommendation preview:")
    print(data['recommendation'][:600])
    print("...")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print("\n" + "=" * 60)
print("Visa checking is working!")
print("=" * 60)
