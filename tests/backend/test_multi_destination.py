"""Tests for multi-destination comparison queries."""

import pytest
import json
from api_server import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestMultiDestinationComparison:
    """Tests for comparing multiple destinations."""

    def test_mumbai_or_delhi_comparison(self, client):
        """Test comparison between Mumbai and Delhi."""
        payload = {
            "query": "Should I go to Mumbai or Delhi?",
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
        
        # Should mention both cities
        assert "Mumbai" in recommendation
        assert "Delhi" in recommendation
        
        # Should have comparison structure
        assert "1. Mumbai" in recommendation or "1. Delhi" in recommendation
        assert "2. Mumbai" in recommendation or "2. Delhi" in recommendation
        
        # Should have comparison summary
        assert "QUICK COMPARISON SUMMARY" in recommendation or "COMPARISON" in recommendation
        
        # Should show different weather for each
        assert "tropical" in recommendation.lower() or "subtropical" in recommendation.lower()

    def test_paris_or_tokyo_comparison(self, client):
        """Test comparison between Paris and Tokyo."""
        payload = {
            "query": "Paris or Tokyo?",
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
        
        # Should mention both cities
        assert "Paris" in recommendation
        assert "Tokyo" in recommendation
        
        # Should have numbered entries
        assert "1." in recommendation
        assert "2." in recommendation

    def test_zurich_vs_dubai_comparison(self, client):
        """Test comparison between Zurich and Dubai using 'vs'."""
        payload = {
            "query": "Zurich vs Dubai",
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
        
        # Should mention both cities
        assert "Zurich" in recommendation
        assert "Dubai" in recommendation
        
        # Should show different climates
        assert "alpine" in recommendation.lower() or "desert" in recommendation.lower()

    def test_single_destination_not_comparison(self, client):
        """Test that single destination query doesn't trigger comparison mode."""
        payload = {
            "query": "Should I go to Mumbai?",
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
        
        # Should mention Mumbai
        assert "Mumbai" in recommendation
        
        # Should NOT have comparison format (no numbered list of destinations)
        # It should have the standard format with "YOUR PROFILE", "WEATHER ANALYSIS", etc.
        assert "YOUR PROFILE" in recommendation or "WEATHER ANALYSIS" in recommendation

    def test_comparison_shows_different_temperatures(self, client):
        """Test that comparison shows different temperatures for different destinations."""
        payload = {
            "query": "Should I go to Zurich or Dubai?",
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
        
        # Extract temperature mentions
        import re
        temps = re.findall(r'(\d+)°F', recommendation)
        temps = [int(t) for t in temps]
        
        # Should have multiple different temperatures
        assert len(temps) >= 2
        # Zurich should be cooler (40-60°F) and Dubai hotter (80-100°F)
        assert any(t < 65 for t in temps), "Should have cool temperature for Zurich"
        assert any(t > 80 for t in temps), "Should have hot temperature for Dubai"

    def test_comparison_shows_different_flight_durations(self, client):
        """Test that comparison shows different flight durations."""
        payload = {
            "query": "Maui or Bangalore?",
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
        
        # Should mention both destinations
        assert "Maui" in recommendation
        assert "Bangalore" in recommendation
        
        # Extract flight durations
        import re
        durations = re.findall(r'Duration: ([\d.]+) hours', recommendation)
        durations = [float(d) for d in durations]
        
        # Should have different durations
        assert len(durations) >= 2
        # Maui should be short (~6h) and Bangalore long (~17h)
        assert any(d < 10 for d in durations), "Should have short flight for Maui"
        assert any(d > 15 for d in durations), "Should have long flight for Bangalore"

    def test_comparison_includes_visa_info(self, client):
        """Test that comparison includes visa information for each destination."""
        payload = {
            "query": "Mumbai or Paris?",
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
        
        # Should mention visa for both destinations
        assert "Visa" in recommendation or "visa" in recommendation
        # Should have multiple visa mentions (one for each destination)
        visa_count = recommendation.lower().count("visa")
        assert visa_count >= 2, "Should mention visa for each destination"

    def test_three_destinations_comparison(self, client):
        """Test comparison with three destinations."""
        payload = {
            "query": "Should I visit Paris, Tokyo, or Dubai?",
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
        
        # Should mention all three cities
        assert "Paris" in recommendation
        assert "Tokyo" in recommendation
        assert "Dubai" in recommendation
        
        # Should have three numbered entries
        assert "1." in recommendation
        assert "2." in recommendation
        assert "3." in recommendation


class TestNoDestinationHandling:
    """Tests for queries without identifiable destinations."""

    def test_no_destination_returns_helpful_message(self, client):
        """Test that queries without destinations get helpful guidance."""
        payload = {
            "query": "What is the weather like?",
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
        
        # Should indicate no destination was found
        assert "couldn't identify" in recommendation.lower() or "no destination" in recommendation.lower()
        
        # Should provide examples
        assert "Paris" in recommendation or "Tokyo" in recommendation or "Mumbai" in recommendation
        
        # Should suggest how to ask
        assert "Try asking" in recommendation or "try" in recommendation.lower()

    def test_generic_travel_query_returns_helpful_message(self, client):
        """Test that generic travel queries get helpful guidance."""
        payload = {
            "query": "Tell me about travel",
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
        
        # Should indicate no destination was found
        assert "couldn't identify" in recommendation.lower()
        
        # Should provide destination examples
        destination_count = sum([
            "Paris" in recommendation,
            "Tokyo" in recommendation,
            "Mumbai" in recommendation,
            "Delhi" in recommendation,
            "Dubai" in recommendation
        ])
        assert destination_count >= 3, "Should provide multiple destination examples"

    def test_empty_query_returns_helpful_message(self, client):
        """Test that empty or vague queries get helpful guidance."""
        payload = {
            "query": "Where should I go?",
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
        
        # Should provide helpful guidance
        assert "couldn't identify" in recommendation.lower() or "destination" in recommendation.lower()

    def test_valid_destination_still_works(self, client):
        """Test that valid destination queries still work normally."""
        payload = {
            "query": "Is it a good time to go to Paris?",
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
        
        # Should have normal recommendation format
        assert "Paris" in recommendation
        assert "WEATHER ANALYSIS" in recommendation or "Weather" in recommendation
        assert "FLIGHT OPTIONS" in recommendation or "Flight" in recommendation
        
        # Should NOT have the "couldn't identify" message
        assert "couldn't identify" not in recommendation.lower()
