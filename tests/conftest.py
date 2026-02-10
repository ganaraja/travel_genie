"""Pytest configuration and fixtures."""

import pytest
from datetime import date, timedelta

from core.models import (
    UserProfile,
    WeatherForecast,
    WeatherPeriod,
    FlightOption,
    HotelOption,
    ComfortLevel,
)


@pytest.fixture
def sample_user_profile():
    """Sample user profile for testing."""
    return UserProfile(
        user_id="test_user",
        preferred_temp_range=(75.0, 85.0),
        airfare_budget_soft=600.0,
        airfare_budget_hard=900.0,
        hotel_budget_min=150.0,
        hotel_budget_max=300.0,
        preferred_brands=["Marriott", "Hilton"],
        typical_trip_length_days=7,
        comfort_level=ComfortLevel.COMFORT,
        flexibility_days=5,
        safety_conscious=True,
        visa_required=False,
    )


@pytest.fixture
def sample_weather_forecast():
    """Sample weather forecast for testing."""
    today = date.today()
    return WeatherForecast(
        destination="Maui",
        forecast_periods=[
            WeatherPeriod(
                start_date=today,
                end_date=today + timedelta(days=6),
                avg_temp_f=82.0,
                min_temp_f=78.0,
                max_temp_f=86.0,
                precipitation_inches=0.1,
                storm_risk=False,
                conditions_summary="Warm and mostly sunny",
            ),
            WeatherPeriod(
                start_date=today + timedelta(days=7),
                end_date=today + timedelta(days=13),
                avg_temp_f=85.0,
                min_temp_f=80.0,
                max_temp_f=90.0,
                precipitation_inches=2.5,
                storm_risk=True,
                storm_severity="moderate",
                conditions_summary="Moderate storm expected",
            ),
            WeatherPeriod(
                start_date=today + timedelta(days=14),
                end_date=today + timedelta(days=20),
                avg_temp_f=88.0,
                min_temp_f=84.0,
                max_temp_f=92.0,
                precipitation_inches=0.2,
                storm_risk=False,
                conditions_summary="Hot and sunny",
            ),
        ],
        overall_summary="Generally warm weather with one storm period",
    )


@pytest.fixture
def sample_flight_options():
    """Sample flight options for testing."""
    today = date.today()
    return [
        FlightOption(
            departure_date=today + timedelta(days=7),
            return_date=today + timedelta(days=14),
            price_usd=580.0,
            airline="United",
            departure_time="08:30",
            return_time="14:20",
            is_red_eye=False,
            is_weekday=True,
            layovers=1,
            total_duration_hours=8.5,
            booking_code="FLT-001",
        ),
        FlightOption(
            departure_date=today + timedelta(days=8),
            return_date=today + timedelta(days=15),
            price_usd=620.0,
            airline="Hawaiian",
            departure_time="08:30",
            return_time="14:20",
            is_red_eye=False,
            is_weekday=True,
            layovers=0,
            total_duration_hours=6.0,
            booking_code="FLT-002",
        ),
        FlightOption(
            departure_date=today + timedelta(days=9),
            return_date=today + timedelta(days=16),
            price_usd=950.0,  # Over hard budget
            airline="Delta",
            departure_time="10:00",
            return_time="16:00",
            is_red_eye=False,
            is_weekday=False,
            layovers=1,
            total_duration_hours=9.0,
            booking_code="FLT-003",
        ),
    ]


@pytest.fixture
def sample_hotel_options():
    """Sample hotel options for testing."""
    today = date.today()
    return [
        HotelOption(
            check_in_date=today + timedelta(days=7),
            check_out_date=today + timedelta(days=14),
            nightly_rate_usd=220.0,
            total_price_usd=1540.0,
            brand="Marriott",
            name="Marriott Maui",
            rating=4.2,
            is_anomalous_pricing=False,
            booking_code="HTL-001",
        ),
        HotelOption(
            check_in_date=today + timedelta(days=7),
            check_out_date=today + timedelta(days=14),
            nightly_rate_usd=180.0,
            total_price_usd=1260.0,
            brand="Hilton",
            name="Hilton Maui",
            rating=3.8,
            is_anomalous_pricing=False,
            booking_code="HTL-002",
        ),
        HotelOption(
            check_in_date=today + timedelta(days=7),
            check_out_date=today + timedelta(days=14),
            nightly_rate_usd=350.0,  # Over budget
            total_price_usd=2450.0,
            brand="Four Seasons",
            name="Four Seasons Maui",
            rating=5.0,
            is_anomalous_pricing=False,
            booking_code="HTL-003",
        ),
    ]
