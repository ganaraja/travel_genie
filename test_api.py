"""Test the Travel Genie API server."""

import requests
import json

API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check passed\n")

def test_user_profile():
    """Test user profile endpoint."""
    print("Testing user profile endpoint...")
    response = requests.get(f"{API_URL}/api/user-profile/user_123")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    assert response.json()["userId"] == "user_123"
    print("✅ User profile test passed\n")

def test_recommendation():
    """Test recommendation endpoint."""
    print("Testing recommendation endpoint...")
    print("This will take 10-30 seconds as the AI agent processes the query...\n")
    
    payload = {
        "query": "Is it a good time to go to Maui?",
        "userId": "user_123"
    }
    
    response = requests.post(
        f"{API_URL}/api/recommend",
        json=payload,
        timeout=60
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Query: {data.get('query')}")
        print(f"\nRecommendation:\n{data.get('recommendation')}\n")
        assert data["success"] == True
        assert len(data["recommendation"]) > 0
        print("✅ Recommendation test passed\n")
    else:
        print(f"Error: {response.text}")
        raise Exception("Recommendation test failed")

if __name__ == "__main__":
    print("=" * 60)
    print("Travel Genie API Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_user_profile()
        test_recommendation()
        
        print("=" * 60)
        print("🎉 All API tests passed!")
        print("=" * 60)
        print()
        print("The API is working correctly. You can now:")
        print("1. Start the frontend: cd frontend && npm start")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Start using Travel Genie!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server")
        print("Please start the API server first:")
        print("  uv run python api_server.py")
    except Exception as e:
        print(f"❌ Test failed: {e}")
