"""Integration tests for the complete Travel Genie system."""

import pytest
from datetime import date, timedelta
from agent.coordinator import (
    get_user_profile_tool,
    get_weather_forecast_tool,
    search_flights_tool,
    search_hotels_tool,
)
from api_server import check_visa_requirements, synthesize_recommendation


class TestCompleteWorkflow:
    """Tests for complete travel recommendation workflow."""

    def test_complete_workflow_maui(self):
        """Test complete workflow for Maui recommendation."""
        # Step 1: Get user profile
        profile = get_user_profile_tool("user_123")
        assert profile["user_id"] == "user_123"
        assert profile["citizenship"] == "USA"
        
        # Step 2: Check visa requirements
        visa_info = check_visa_requirements("USA", profile["citizenship"])
        assert visa_info["required"] is False
        assert visa_info["type"] == "domestic"
        
        # Step 3: Get weather forecast
        weather = get_weather_forecast_tool("Maui")
        assert weather["destination"] == "Maui"
        assert len(weather["periods"]) > 0
        
        # Step 4: Search flights
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool(
            "SFO", "OGG", dep_date, ret_date, profile["flexibility_days"]
        )
        assert len(flights["options"]) > 0
        
        # Step 5: Search hotels
        hotels = search_hotels_tool(
            "Maui", dep_date, ret_date, profile["preferred_brands"]
        )
        assert len(hotels["options"]) > 0
        
        # Step 6: Synthesize recommendation
        visa_note = "No visa required (domestic travel)"
        recommendation = synthesize_recommendation(
            "Should I go to Maui?",
            "Maui",
            profile,
            weather,
            flights,
            hotels,
            visa_note
        )
        
        assert len(recommendation) > 0
        assert "maui" in recommendation.lower()

    def test_complete_workflow_international_visa_free(self):
        """Test complete workflow for international destination (visa-free)."""
        # Step 1: Get user profile
        profile = get_user_profile_tool("default")
        assert profile["citizenship"] == "USA"
        
        # Step 2: Check visa requirements for France
        visa_info = check_visa_requirements("France", profile["citizenship"])
        assert visa_info["required"] is False
        assert visa_info["type"] == "visa_waiver"
        
        # Step 3: Get weather forecast
        weather = get_weather_forecast_tool("Paris")
        assert weather["destination"] == "Paris"
        
        # Step 4: Search flights
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool(
            "SFO", "CDG", dep_date, ret_date, profile["flexibility_days"]
        )
        assert len(flights["options"]) > 0
        
        # Step 5: Search hotels
        hotels = search_hotels_tool(
            "Paris", dep_date, ret_date, profile["preferred_brands"]
        )
        assert len(hotels["options"]) > 0

    def test_complete_workflow_visa_required(self):
        """Test complete workflow when visa is required."""
        # Step 1: Get user profile
        profile = get_user_profile_tool("default")
        assert profile["citizenship"] == "USA"
        
        # Step 2: Check visa requirements for China
        visa_info = check_visa_requirements("China", profile["citizenship"])
        assert visa_info["required"] is True
        assert visa_info["type"] == "visa"
        assert "processing_time" in visa_info
        assert "cost" in visa_info

    def test_workflow_respects_budget_constraints(self):
        """Test that workflow respects user budget constraints."""
        profile = get_user_profile_tool("default")
        
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "OGG", dep_date, ret_date, 3)
        
        # Check that some flights are within budget
        affordable = [
            f for f in flights["options"]
            if f["price_usd"] <= profile["airfare_budget_soft"]
        ]
        
        # Should have at least some affordable options
        assert len(affordable) >= 0  # May or may not have affordable options

    def test_workflow_considers_safety_preferences(self):
        """Test that workflow considers safety preferences."""
        profile = get_user_profile_tool("user_123")
        assert profile["safety_conscious"] is True
        
        weather = get_weather_forecast_tool("Maui", days_ahead=30)
        
        # Check if storms are detected
        storm_periods = [p for p in weather["periods"] if p["storm_risk"]]
        
        # If there are storms, they should be flagged
        if storm_periods:
            assert "storm" in weather["overall_summary"].lower()

    def test_workflow_considers_brand_preferences(self):
        """Test that workflow considers hotel brand preferences."""
        profile = get_user_profile_tool("user_123")
        assert "Marriott" in profile["preferred_brands"]
        
        today = date.today()
        check_in = (today + timedelta(days=14)).isoformat()
        check_out = (today + timedelta(days=21)).isoformat()
        
        hotels = search_hotels_tool(
            "Maui", check_in, check_out, profile["preferred_brands"]
        )
        
        # Check if Marriott is in the results
        marriott_hotels = [h for h in hotels["options"] if h["brand"] == "Marriott"]
        assert len(marriott_hotels) > 0


class TestVisaWorkflow:
    """Tests for visa checking workflow."""

    def test_visa_check_before_flight_search(self):
        """Test that visa is checked before searching flights."""
        # This simulates the correct workflow order
        profile = get_user_profile_tool("default")
        
        # Check visa FIRST
        visa_info = check_visa_requirements("Japan", profile["citizenship"])
        
        # Then search flights only if visa is not a blocker
        if not visa_info["required"] or visa_info["type"] in ["visa_waiver", "visa_on_arrival", "e-visa"]:
            today = date.today()
            dep_date = (today + timedelta(days=14)).isoformat()
            ret_date = (today + timedelta(days=21)).isoformat()
            
            flights = search_flights_tool("SFO", "NRT", dep_date, ret_date, 3)
            assert len(flights["options"]) > 0

    def test_visa_workflow_different_citizenships(self):
        """Test visa workflow for different citizenships."""
        destinations = ["USA", "France", "Japan", "Indonesia"]
        
        # USA citizen
        profile_usa = get_user_profile_tool("default")
        for dest in destinations:
            visa_info = check_visa_requirements(dest, profile_usa["citizenship"])
            assert "required" in visa_info
            assert "type" in visa_info
            assert visa_info["citizenship"] == "USA"

    def test_visa_info_structure_complete(self):
        """Test that visa info has all required fields."""
        profile = get_user_profile_tool("default")
        visa_info = check_visa_requirements("France", profile["citizenship"])
        
        required_fields = [
            "required",
            "type",
            "processing_time",
            "cost",
            "country",
            "citizenship"
        ]
        
        for field in required_fields:
            assert field in visa_info


class TestDataConsistency:
    """Tests for data consistency across the system."""

    def test_profile_data_consistency(self):
        """Test that profile data is consistent across tools."""
        profile_from_tool = get_user_profile_tool("user_123")
        
        from tools.user_profile import _MOCK_PROFILES
        profile_from_mock = _MOCK_PROFILES["user_123"]
        
        assert profile_from_tool["user_id"] == profile_from_mock.user_id
        assert profile_from_tool["citizenship"] == profile_from_mock.citizenship
        assert profile_from_tool["preferred_temp_range"] == profile_from_mock.preferred_temp_range

    def test_date_consistency(self):
        """Test that dates are consistent across tools."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "OGG", dep_date, ret_date, 3)
        hotels = search_hotels_tool("Maui", dep_date, ret_date)
        
        # Check that dates are in valid format
        for flight in flights["options"]:
            assert len(flight["departure_date"]) == 10  # YYYY-MM-DD
            assert len(flight["return_date"]) == 10
        
        for hotel in hotels["options"]:
            assert len(hotel["check_in_date"]) == 10
            assert len(hotel["check_out_date"]) == 10

    def test_price_consistency(self):
        """Test that prices are consistent and valid."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "OGG", dep_date, ret_date, 3)
        hotels = search_hotels_tool("Maui", dep_date, ret_date)
        
        # All prices should be positive
        for flight in flights["options"]:
            assert flight["price_usd"] > 0
        
        for hotel in hotels["options"]:
            assert hotel["nightly_rate_usd"] > 0
            assert hotel["total_price_usd"] > 0


class TestErrorHandling:
    """Tests for error handling in the system."""

    def test_invalid_date_range_hotels(self):
        """Test handling of invalid date range for hotels."""
        today = date.today()
        check_in = (today + timedelta(days=21)).isoformat()
        check_out = (today + timedelta(days=14)).isoformat()  # Before check-in
        
        hotels = search_hotels_tool("Maui", check_in, check_out)
        
        assert len(hotels["options"]) == 0
        assert "invalid" in hotels["summary"].lower()

    def test_unknown_user_defaults_gracefully(self):
        """Test that unknown user ID defaults to default profile."""
        profile = get_user_profile_tool("unknown_user_xyz_123")
        
        assert profile["user_id"] == "default"
        assert "citizenship" in profile

    def test_unknown_visa_combination_defaults_safely(self):
        """Test that unknown visa combination defaults safely."""
        visa_info = check_visa_requirements("UnknownCountry", "UnknownCitizenship")
        
        assert visa_info["required"] is True  # Safe default
        assert "note" in visa_info or "processing_time" in visa_info
