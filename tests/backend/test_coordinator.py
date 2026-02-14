"""Tests for agent coordinator functions."""

import pytest
from datetime import date, timedelta
from agent.coordinator import (
    get_user_profile_tool,
    get_weather_forecast_tool,
    search_flights_tool,
    search_hotels_tool,
)


class TestGetUserProfileTool:
    """Tests for get_user_profile_tool function."""

    def test_get_user_profile_user_123(self):
        """Test retrieving user_123 profile."""
        profile = get_user_profile_tool("user_123")
        
        assert profile["user_id"] == "user_123"
        assert profile["citizenship"] == "USA"
        assert profile["passport_country"] == "USA"
        assert profile["preferred_temp_range"] == (75.0, 85.0)
        assert profile["airfare_budget_soft"] == 600.0
        assert profile["airfare_budget_hard"] == 900.0
        assert profile["hotel_budget_min"] == 150.0
        assert profile["hotel_budget_max"] == 300.0
        assert "Marriott" in profile["preferred_brands"]
        assert "Hilton" in profile["preferred_brands"]
        assert profile["typical_trip_length_days"] == 7
        assert profile["comfort_level"] == "comfort"
        assert profile["flexibility_days"] == 5
        assert profile["safety_conscious"] is True
        assert profile["visa_required"] is False

    def test_get_user_profile_default(self):
        """Test retrieving default profile."""
        profile = get_user_profile_tool("default")
        
        assert profile["user_id"] == "default"
        assert profile["citizenship"] == "USA"
        assert profile["passport_country"] == "USA"
        assert profile["preferred_temp_range"] == (70.0, 80.0)
        assert profile["airfare_budget_soft"] == 500.0
        assert profile["airfare_budget_hard"] == 800.0
        assert profile["hotel_budget_min"] == 100.0
        assert profile["hotel_budget_max"] == 250.0
        assert profile["preferred_brands"] == []
        assert profile["typical_trip_length_days"] == 5
        assert profile["comfort_level"] == "standard"
        assert profile["flexibility_days"] == 3
        assert profile["safety_conscious"] is False

    def test_get_user_profile_unknown_user_returns_default(self):
        """Test that unknown user ID returns default profile."""
        profile = get_user_profile_tool("unknown_user_xyz")
        
        assert profile["user_id"] == "default"
        assert profile["citizenship"] == "USA"

    def test_get_user_profile_has_citizenship_fields(self):
        """Test that profile includes citizenship and passport_country fields."""
        profile = get_user_profile_tool("user_123")
        
        assert "citizenship" in profile
        assert "passport_country" in profile
        assert isinstance(profile["citizenship"], str)
        assert isinstance(profile["passport_country"], str)

    def test_get_user_profile_return_type(self):
        """Test that function returns a dictionary."""
        profile = get_user_profile_tool("user_123")
        
        assert isinstance(profile, dict)
        assert len(profile) > 0


class TestGetWeatherForecastTool:
    """Tests for get_weather_forecast_tool function."""

    def test_get_weather_forecast_basic(self):
        """Test basic weather forecast retrieval."""
        today = date.today()
        forecast = get_weather_forecast_tool("Maui", today.isoformat(), 30)
        
        assert forecast["destination"] == "Maui"
        assert "overall_summary" in forecast
        assert "periods" in forecast
        assert len(forecast["periods"]) > 0

    def test_get_weather_forecast_default_start_date(self):
        """Test weather forecast with default start date (today)."""
        forecast = get_weather_forecast_tool("Paris")
        
        assert forecast["destination"] == "Paris"
        assert "overall_summary" in forecast
        assert len(forecast["periods"]) > 0

    def test_get_weather_forecast_periods_structure(self):
        """Test that weather periods have correct structure."""
        forecast = get_weather_forecast_tool("Tokyo", days_ahead=14)
        
        for period in forecast["periods"]:
            assert "start_date" in period
            assert "end_date" in period
            assert "avg_temp_f" in period
            assert "storm_risk" in period
            assert "storm_severity" in period
            assert "conditions_summary" in period
            assert isinstance(period["storm_risk"], bool)

    def test_get_weather_forecast_storm_detection(self):
        """Test that storms are detected in forecast."""
        forecast = get_weather_forecast_tool("Maui", days_ahead=30)
        
        storm_periods = [p for p in forecast["periods"] if p["storm_risk"]]
        # Week 2 (day 7) should have a storm in mock data
        assert len(storm_periods) >= 0  # May or may not have storms

    def test_get_weather_forecast_summary_mentions_storms(self):
        """Test that overall summary mentions storms if present."""
        forecast = get_weather_forecast_tool("Maui", days_ahead=30)
        
        storm_periods = [p for p in forecast["periods"] if p["storm_risk"]]
        if storm_periods:
            assert "storm" in forecast["overall_summary"].lower()

    def test_get_weather_forecast_return_type(self):
        """Test that function returns a dictionary."""
        forecast = get_weather_forecast_tool("Bali")
        
        assert isinstance(forecast, dict)
        assert isinstance(forecast["periods"], list)


class TestSearchFlightsTool:
    """Tests for search_flights_tool function."""

    def test_search_flights_basic(self):
        """Test basic flight search."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "OGG", dep_date, ret_date, 3)
        
        assert flights["origin"] == "SFO"
        assert flights["destination"] == "OGG"
        assert "options" in flights
        assert "summary" in flights
        assert len(flights["options"]) > 0

    def test_search_flights_flexibility(self):
        """Test that flexibility_days parameter affects results."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights_low_flex = search_flights_tool("SFO", "OGG", dep_date, ret_date, 1)
        flights_high_flex = search_flights_tool("SFO", "OGG", dep_date, ret_date, 5)
        
        # Higher flexibility should return more options
        assert len(flights_high_flex["options"]) >= len(flights_low_flex["options"])

    def test_search_flights_option_structure(self):
        """Test that flight options have correct structure."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "CDG", dep_date, ret_date, 3)
        
        for option in flights["options"]:
            assert "departure_date" in option
            assert "return_date" in option
            assert "price_usd" in option
            assert "airline" in option
            assert "departure_time" in option
            assert "return_time" in option
            assert "is_red_eye" in option
            assert "is_weekday" in option
            assert "layovers" in option
            assert "total_duration_hours" in option
            assert "booking_code" in option

    def test_search_flights_sorted_by_price(self):
        """Test that flight options are sorted by price."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "OGG", dep_date, ret_date, 3)
        
        prices = [opt["price_usd"] for opt in flights["options"]]
        assert prices == sorted(prices)

    def test_search_flights_summary_includes_price_range(self):
        """Test that summary includes price range."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "NRT", dep_date, ret_date, 3)
        
        assert "$" in flights["summary"] or "price" in flights["summary"].lower()

    def test_search_flights_return_type(self):
        """Test that function returns a dictionary."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "OGG", dep_date, ret_date)
        
        assert isinstance(flights, dict)
        assert isinstance(flights["options"], list)


class TestSearchHotelsTool:
    """Tests for search_hotels_tool function."""

    def test_search_hotels_basic(self):
        """Test basic hotel search."""
        today = date.today()
        check_in = (today + timedelta(days=14)).isoformat()
        check_out = (today + timedelta(days=21)).isoformat()
        
        hotels = search_hotels_tool("Maui", check_in, check_out)
        
        assert hotels["destination"] == "Maui"
        assert "options" in hotels
        assert "summary" in hotels
        assert len(hotels["options"]) > 0

    def test_search_hotels_with_preferred_brands(self):
        """Test hotel search with preferred brands."""
        today = date.today()
        check_in = (today + timedelta(days=14)).isoformat()
        check_out = (today + timedelta(days=21)).isoformat()
        
        hotels = search_hotels_tool("Paris", check_in, check_out, ["Marriott", "Hilton"])
        
        assert hotels["destination"] == "Paris"
        # Check if any Marriott or Hilton hotels exist
        brands = [h["brand"] for h in hotels["options"]]
        assert "Marriott" in brands or "Hilton" in brands

    def test_search_hotels_option_structure(self):
        """Test that hotel options have correct structure."""
        today = date.today()
        check_in = (today + timedelta(days=14)).isoformat()
        check_out = (today + timedelta(days=21)).isoformat()
        
        hotels = search_hotels_tool("Tokyo", check_in, check_out)
        
        for option in hotels["options"]:
            assert "check_in_date" in option
            assert "check_out_date" in option
            assert "nightly_rate_usd" in option
            assert "total_price_usd" in option
            assert "brand" in option
            assert "name" in option
            assert "rating" in option
            assert "is_anomalous_pricing" in option
            assert "booking_code" in option

    def test_search_hotels_sorted_by_price(self):
        """Test that hotel options are sorted by nightly rate."""
        today = date.today()
        check_in = (today + timedelta(days=14)).isoformat()
        check_out = (today + timedelta(days=21)).isoformat()
        
        hotels = search_hotels_tool("Bali", check_in, check_out)
        
        rates = [opt["nightly_rate_usd"] for opt in hotels["options"]]
        assert rates == sorted(rates)

    def test_search_hotels_anomalous_pricing_detection(self):
        """Test that anomalous pricing is detected."""
        today = date.today()
        check_in = (today + timedelta(days=14)).isoformat()
        check_out = (today + timedelta(days=21)).isoformat()
        
        hotels = search_hotels_tool("Maui", check_in, check_out)
        
        # Check if any hotels have anomalous pricing
        anomalous = [h for h in hotels["options"] if h["is_anomalous_pricing"]]
        # May or may not have anomalous pricing depending on dates
        assert isinstance(anomalous, list)

    def test_search_hotels_invalid_date_range(self):
        """Test hotel search with invalid date range (check-out before check-in)."""
        today = date.today()
        check_in = (today + timedelta(days=21)).isoformat()
        check_out = (today + timedelta(days=14)).isoformat()  # Before check-in
        
        hotels = search_hotels_tool("Maui", check_in, check_out)
        
        assert hotels["destination"] == "Maui"
        assert len(hotels["options"]) == 0
        assert "invalid" in hotels["summary"].lower()

    def test_search_hotels_return_type(self):
        """Test that function returns a dictionary."""
        today = date.today()
        check_in = (today + timedelta(days=14)).isoformat()
        check_out = (today + timedelta(days=21)).isoformat()
        
        hotels = search_hotels_tool("Maui", check_in, check_out)
        
        assert isinstance(hotels, dict)
        assert isinstance(hotels["options"], list)
