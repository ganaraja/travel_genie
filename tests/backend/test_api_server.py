"""Tests for Flask API server endpoints."""

import pytest
import json
from datetime import date, timedelta
from api_server import app, check_visa_requirements, synthesize_recommendation


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for /api/health endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint returns 200."""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert data["service"] == "Travel Genie API"


class TestRecommendEndpoint:
    """Tests for /api/recommend endpoint."""

    def test_recommend_with_valid_query(self, client):
        """Test recommendation endpoint with valid query."""
        payload = {
            "query": "Should I go to Maui?",
            "userId": "default"
        }
        
        response = client.post(
            '/api/recommend',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "recommendation" in data
        assert data["query"] == "Should I go to Maui?"
        assert data["userId"] == "default"

    def test_recommend_without_query(self, client):
        """Test recommendation endpoint without query returns 400."""
        payload = {
            "userId": "default"
        }
        
        response = client.post(
            '/api/recommend',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_recommend_with_default_user_id(self, client):
        """Test recommendation endpoint defaults to 'default' user."""
        payload = {
            "query": "Should I go to Paris?"
        }
        
        response = client.post(
            '/api/recommend',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["userId"] == "default"

    def test_recommend_includes_visa_info(self, client):
        """Test that recommendation includes visa information."""
        payload = {
            "query": "Should I go to Tokyo?",
            "userId": "default"
        }
        
        response = client.post(
            '/api/recommend',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        recommendation = data["recommendation"]
        
        # Should mention visa or entry requirements
        assert "visa" in recommendation.lower() or "entry" in recommendation.lower()

    def test_recommend_maui_destination(self, client):
        """Test recommendation for Maui destination."""
        payload = {
            "query": "When should I visit Hawaii?",
            "userId": "user_123"
        }
        
        response = client.post(
            '/api/recommend',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        recommendation = data["recommendation"]
        
        # Should mention Maui or Hawaii
        assert "maui" in recommendation.lower() or "hawaii" in recommendation.lower()

    def test_recommend_paris_destination(self, client):
        """Test recommendation for Paris destination."""
        payload = {
            "query": "Should I go to Paris?",
            "userId": "default"
        }
        
        response = client.post(
            '/api/recommend',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        recommendation = data["recommendation"]
        
        assert "paris" in recommendation.lower()

    def test_recommend_tokyo_destination(self, client):
        """Test recommendation for Tokyo destination."""
        payload = {
            "query": "Is Tokyo a good destination?",
            "userId": "default"
        }
        
        response = client.post(
            '/api/recommend',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        recommendation = data["recommendation"]
        
        assert "tokyo" in recommendation.lower()

    def test_recommend_bali_destination(self, client):
        """Test recommendation for Bali destination."""
        payload = {
            "query": "What about Bali?",
            "userId": "default"
        }
        
        response = client.post(
            '/api/recommend',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        recommendation = data["recommendation"]
        
        assert "bali" in recommendation.lower()

    def test_recommend_zurich_destination(self, client):
        """Test recommendation for Zurich destination."""
        payload = {
            "query": "best time to visit zurich",
            "userId": "default"
        }
        
        response = client.post(
            '/api/recommend',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        recommendation = data["recommendation"]
        
        # Should mention Zurich or Switzerland
        assert "zurich" in recommendation.lower() or "switzerland" in recommendation.lower()
        # Should NOT mention Maui (common bug)
        assert "maui" not in recommendation.lower()
        # Should mention ZRH airport code
        assert "zrh" in recommendation.lower() or "zurich" in recommendation.lower()


class TestUserProfileEndpoint:
    """Tests for /api/user-profile/<user_id> endpoint."""

    def test_get_user_profile_user_123(self, client):
        """Test getting user_123 profile."""
        response = client.get('/api/user-profile/user_123')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["userId"] == "user_123"
        assert data["preferredTempRange"] == [75.0, 85.0]
        assert data["airfareBudgetSoft"] == 600.0
        assert data["airfareBudgetHard"] == 900.0
        assert "Marriott" in data["preferredBrands"]

    def test_get_user_profile_default(self, client):
        """Test getting default profile."""
        response = client.get('/api/user-profile/default')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["userId"] == "default"
        assert data["preferredTempRange"] == [70.0, 80.0]
        assert data["airfareBudgetSoft"] == 500.0

    def test_get_user_profile_unknown_returns_default(self, client):
        """Test that unknown user returns default profile."""
        response = client.get('/api/user-profile/unknown_user')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["userId"] == "default"


class TestSynthesizeRecommendation:
    """Tests for synthesize_recommendation function."""

    def test_synthesize_includes_profile_info(self):
        """Test that synthesis includes profile information."""
        profile = {
            "citizenship": "USA",
            "preferred_temp_range": (75.0, 85.0),
            "airfare_budget_soft": 600.0,
            "airfare_budget_hard": 900.0,
            "hotel_budget_min": 150.0,
            "hotel_budget_max": 300.0,
            "preferred_brands": ["Marriott"],
            "typical_trip_length_days": 7,
            "flexibility_days": 5,
            "safety_conscious": True,
        }
        
        weather = {
            "overall_summary": "Warm weather expected",
            "periods": []
        }
        
        flights = {
            "options": []
        }
        
        hotels = {
            "options": []
        }
        
        visa_note = "No visa required"
        
        result = synthesize_recommendation(
            "Should I go to Maui?",
            "Maui",
            profile,
            weather,
            flights,
            hotels,
            visa_note
        )
        
        assert "citizenship" in result.lower() or "usa" in result.lower()
        assert "visa" in result.lower()

    def test_synthesize_includes_weather_info(self):
        """Test that synthesis includes weather information."""
        profile = {
            "citizenship": "USA",
            "preferred_temp_range": (75.0, 85.0),
            "airfare_budget_soft": 600.0,
            "airfare_budget_hard": 900.0,
            "hotel_budget_min": 150.0,
            "hotel_budget_max": 300.0,
            "preferred_brands": [],
            "typical_trip_length_days": 7,
            "flexibility_days": 3,
            "safety_conscious": False,
        }
        
        weather = {
            "overall_summary": "Perfect beach weather with sunny skies",
            "periods": [
                {
                    "start_date": date.today().isoformat(),
                    "end_date": (date.today() + timedelta(days=7)).isoformat(),
                    "avg_temp_f": 82.0,
                    "storm_risk": False,
                }
            ]
        }
        
        flights = {"options": []}
        hotels = {"options": []}
        visa_note = "No visa required"
        
        result = synthesize_recommendation(
            "Should I go?",
            "Maui",
            profile,
            weather,
            flights,
            hotels,
            visa_note
        )
        
        assert "weather" in result.lower()

    def test_synthesize_includes_flight_info(self):
        """Test that synthesis includes flight information."""
        today = date.today()
        profile = {
            "citizenship": "USA",
            "preferred_temp_range": (75.0, 85.0),
            "airfare_budget_soft": 600.0,
            "airfare_budget_hard": 900.0,
            "hotel_budget_min": 150.0,
            "hotel_budget_max": 300.0,
            "preferred_brands": [],
            "typical_trip_length_days": 7,
            "flexibility_days": 3,
            "safety_conscious": False,
        }
        
        weather = {"overall_summary": "Good weather", "periods": []}
        
        flights = {
            "options": [
                {
                    "departure_date": (today + timedelta(days=7)).isoformat(),
                    "return_date": (today + timedelta(days=14)).isoformat(),
                    "price_usd": 550.0,
                    "airline": "United",
                    "departure_time": "08:30",
                    "return_time": "14:20",
                    "is_red_eye": False,
                    "total_duration_hours": 8.5,
                    "layovers": 1,
                }
            ]
        }
        
        hotels = {"options": []}
        visa_note = "No visa required"
        
        result = synthesize_recommendation(
            "Should I go?",
            "Maui",
            profile,
            weather,
            flights,
            hotels,
            visa_note
        )
        
        assert "flight" in result.lower()
        assert "$550" in result or "550" in result

    def test_synthesize_includes_hotel_info(self):
        """Test that synthesis includes hotel information."""
        today = date.today()
        profile = {
            "citizenship": "USA",
            "preferred_temp_range": (75.0, 85.0),
            "airfare_budget_soft": 600.0,
            "airfare_budget_hard": 900.0,
            "hotel_budget_min": 150.0,
            "hotel_budget_max": 300.0,
            "preferred_brands": ["Marriott"],
            "typical_trip_length_days": 7,
            "flexibility_days": 3,
            "safety_conscious": False,
        }
        
        weather = {"overall_summary": "Good weather", "periods": []}
        flights = {"options": []}
        
        hotels = {
            "options": [
                {
                    "check_in_date": (today + timedelta(days=7)).isoformat(),
                    "check_out_date": (today + timedelta(days=14)).isoformat(),
                    "nightly_rate_usd": 200.0,
                    "total_price_usd": 1400.0,
                    "brand": "Marriott",
                    "name": "Marriott Maui",
                    "rating": 4.2,
                    "is_anomalous_pricing": False,
                }
            ]
        }
        
        visa_note = "No visa required"
        
        result = synthesize_recommendation(
            "Should I go?",
            "Maui",
            profile,
            weather,
            flights,
            hotels,
            visa_note
        )
        
        assert "hotel" in result.lower()
        assert "marriott" in result.lower()
