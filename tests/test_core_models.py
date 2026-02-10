"""Tests for core models."""

import pytest
from datetime import date, timedelta

from core.models import (
    UserProfile,
    WeatherForecast,
    WeatherPeriod,
    FlightOption,
    HotelOption,
    Recommendation,
    RecommendationReason,
    ComfortLevel,
)


class TestUserProfile:
    """Tests for UserProfile model."""

    def test_user_profile_creation(self):
        """Test creating a user profile."""
        profile = UserProfile(
            user_id="test_user",
            preferred_temp_range=(75.0, 85.0),
            airfare_budget_soft=600.0,
            airfare_budget_hard=900.0,
            hotel_budget_min=150.0,
            hotel_budget_max=300.0,
            preferred_brands=["Marriott"],
            typical_trip_length_days=7,
            comfort_level=ComfortLevel.COMFORT,
            flexibility_days=5,
            safety_conscious=True,
        )
        assert profile.user_id == "test_user"
        assert profile.preferred_temp_range == (75.0, 85.0)
        assert profile.airfare_budget_soft == 600.0
        assert profile.safety_conscious is True

    def test_user_profile_defaults(self):
        """Test user profile default values."""
        profile = UserProfile(
            user_id="test",
            preferred_temp_range=(70.0, 80.0),
            airfare_budget_soft=500.0,
            airfare_budget_hard=800.0,
            hotel_budget_min=100.0,
            hotel_budget_max=250.0,
            preferred_brands=[],
            typical_trip_length_days=5,
            comfort_level=ComfortLevel.STANDARD,
            flexibility_days=3,
            safety_conscious=False,
        )
        assert profile.visa_required is False
        assert profile.notes is None


class TestWeatherPeriod:
    """Tests for WeatherPeriod model."""

    def test_weather_period_creation(self):
        """Test creating a weather period."""
        period = WeatherPeriod(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            avg_temp_f=82.0,
            min_temp_f=78.0,
            max_temp_f=86.0,
            precipitation_inches=0.1,
            storm_risk=False,
            conditions_summary="Sunny",
        )
        assert period.avg_temp_f == 82.0
        assert period.storm_risk is False
        assert period.storm_severity is None

    def test_weather_period_with_storm(self):
        """Test weather period with storm risk."""
        period = WeatherPeriod(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            avg_temp_f=85.0,
            min_temp_f=80.0,
            max_temp_f=90.0,
            precipitation_inches=2.5,
            storm_risk=True,
            storm_severity="moderate",
            conditions_summary="Storm expected",
        )
        assert period.storm_risk is True
        assert period.storm_severity == "moderate"


class TestFlightOption:
    """Tests for FlightOption model."""

    def test_flight_option_creation(self):
        """Test creating a flight option."""
        flight = FlightOption(
            departure_date=date.today(),
            return_date=date.today() + timedelta(days=7),
            price_usd=600.0,
            airline="United",
            departure_time="08:30",
            return_time="14:20",
            is_red_eye=False,
            is_weekday=True,
            layovers=1,
            total_duration_hours=8.5,
            booking_code="FLT-001",
        )
        assert flight.price_usd == 600.0
        assert flight.is_weekday is True
        assert flight.layovers == 1


class TestHotelOption:
    """Tests for HotelOption model."""

    def test_hotel_option_creation(self):
        """Test creating a hotel option."""
        hotel = HotelOption(
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=7),
            nightly_rate_usd=200.0,
            total_price_usd=1400.0,
            brand="Marriott",
            name="Marriott Maui",
            rating=4.2,
            is_anomalous_pricing=False,
            booking_code="HTL-001",
        )
        assert hotel.nightly_rate_usd == 200.0
        assert hotel.brand == "Marriott"
        assert hotel.is_anomalous_pricing is False


class TestRecommendation:
    """Tests for Recommendation model."""

    def test_recommendation_creation(self):
        """Test creating a recommendation."""
        reasoning = [
            RecommendationReason(
                factor="weather",
                assessment="Perfect temperature",
                positive=True,
            ),
            RecommendationReason(
                factor="price",
                assessment="Within budget",
                positive=True,
            ),
        ]
        
        recommendation = Recommendation(
            recommended_start=date.today() + timedelta(days=7),
            recommended_end=date.today() + timedelta(days=14),
            primary_reasoning=reasoning,
            alternative_options=[
                (date.today() + timedelta(days=8), date.today() + timedelta(days=15), "Alternative dates"),
            ],
            rejected_periods=[
                (date.today() + timedelta(days=1), date.today() + timedelta(days=8), "Storm risk"),
            ],
            personalized_summary="Great time to visit!",
        )
        assert len(recommendation.primary_reasoning) == 2
        assert len(recommendation.alternative_options) == 1
        assert len(recommendation.rejected_periods) == 1
