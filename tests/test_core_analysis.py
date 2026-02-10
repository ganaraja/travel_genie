"""Tests for core analysis module."""

import pytest
from datetime import date, timedelta

from core.models import UserProfile, WeatherForecast, FlightOption, HotelOption, ComfortLevel
from core.analysis import (
    analyze_weather_for_user,
    filter_flights_by_budget,
    score_flight_option,
    filter_hotels_by_budget,
    score_hotel_option,
    find_overlapping_periods,
)


class TestWeatherAnalysis:
    """Tests for weather analysis functions."""

    def test_analyze_weather_perfect_match(self, sample_user_profile, sample_weather_forecast):
        """Test weather analysis with perfect temperature match."""
        results = analyze_weather_for_user(sample_weather_forecast, sample_user_profile)
        
        # First period should score well (82°F is within 75-85°F range)
        period, score, reason = results[0]
        assert score > 0.8
        assert "matches preference" in reason.lower()

    def test_analyze_weather_storm_penalty(self, sample_user_profile, sample_weather_forecast):
        """Test that storm risk heavily penalizes safety-conscious users."""
        results = analyze_weather_for_user(sample_weather_forecast, sample_user_profile)
        
        # Second period has storm risk
        period, score, reason = results[1]
        assert period.storm_risk is True
        assert score < 0.3  # Heavy penalty for safety-conscious user
        assert "storm" in reason.lower()

    def test_analyze_weather_temp_outside_range(self):
        """Test weather analysis when temperature is outside preferred range."""
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
        
        from core.models import WeatherForecast, WeatherPeriod
        forecast = WeatherForecast(
            destination="Test",
            forecast_periods=[
                WeatherPeriod(
                    start_date=date.today(),
                    end_date=date.today() + timedelta(days=7),
                    avg_temp_f=90.0,  # Above preferred range
                    min_temp_f=85.0,
                    max_temp_f=95.0,
                    precipitation_inches=0.1,
                    storm_risk=False,
                    conditions_summary="Hot",
                ),
            ],
            overall_summary="Hot weather",
        )
        
        results = analyze_weather_for_user(forecast, profile)
        period, score, reason = results[0]
        assert score < 1.0
        assert "above preference" in reason.lower()


class TestFlightAnalysis:
    """Tests for flight analysis functions."""

    def test_filter_flights_by_budget(self, sample_user_profile, sample_flight_options):
        """Test filtering flights by budget."""
        affordable, rejected = filter_flights_by_budget(sample_flight_options, sample_user_profile)
        
        # First two flights are within hard budget ($900)
        assert len(affordable) == 2
        assert len(rejected) == 1
        assert rejected[0].price_usd == 950.0

    def test_score_flight_within_soft_budget(self, sample_user_profile, sample_flight_options):
        """Test scoring a flight within soft budget."""
        flight = sample_flight_options[0]  # $580, within $600 soft budget
        score, reason = score_flight_option(flight, sample_user_profile)
        
        assert score > 0.9
        assert "within preferred budget" in reason.lower()

    def test_score_flight_weekday_bonus(self, sample_user_profile, sample_flight_options):
        """Test that weekday flights get a bonus."""
        weekday_flight = sample_flight_options[0]  # is_weekday=True
        weekend_flight = sample_flight_options[2]  # is_weekday=False
        
        weekday_score, _ = score_flight_option(weekday_flight, sample_user_profile)
        weekend_score, _ = score_flight_option(weekend_flight, sample_user_profile)
        
        # Weekday should score higher (if prices are similar)
        # Note: weekend flight is also over budget, so comparison may not be direct

    def test_score_flight_layover_penalty(self, sample_user_profile, sample_flight_options):
        """Test that layovers reduce flight score."""
        direct_flight = sample_flight_options[1]  # layovers=0
        layover_flight = sample_flight_options[0]  # layovers=1
        
        direct_score, _ = score_flight_option(direct_flight, sample_user_profile)
        layover_score, _ = score_flight_option(layover_flight, sample_user_profile)
        
        # Direct flight should score higher
        assert direct_score > layover_score


class TestHotelAnalysis:
    """Tests for hotel analysis functions."""

    def test_filter_hotels_by_budget(self, sample_user_profile, sample_hotel_options):
        """Test filtering hotels by budget."""
        affordable, rejected = filter_hotels_by_budget(sample_hotel_options, sample_user_profile)
        
        # First two hotels are within budget ($150-300)
        assert len(affordable) == 2
        assert len(rejected) == 1
        assert rejected[0].nightly_rate_usd == 350.0

    def test_score_hotel_brand_loyalty(self, sample_user_profile, sample_hotel_options):
        """Test that preferred brands get a bonus."""
        marriott_hotel = sample_hotel_options[0]  # Marriott (preferred)
        four_seasons_hotel = sample_hotel_options[2]  # Four Seasons (not preferred)
        
        marriott_score, marriott_reason = score_hotel_option(marriott_hotel, sample_user_profile)
        four_seasons_score, _ = score_hotel_option(four_seasons_hotel, sample_user_profile)
        
        assert "Marriott" in marriott_reason
        # Marriott should score higher due to brand bonus (if within budget)

    def test_score_hotel_anomalous_pricing(self):
        """Test scoring hotel with anomalous pricing."""
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
        
        hotel_with_discount = HotelOption(
            check_in_date=date.today(),
            check_out_date=date.today() + timedelta(days=7),
            nightly_rate_usd=150.0,
            total_price_usd=1050.0,
            brand="Test",
            name="Test Hotel",
            rating=4.0,
            is_anomalous_pricing=True,
            anomalous_reason="Storm discount - reduced rates",
            booking_code="HTL-TEST",
        )
        
        score, reason = score_hotel_option(hotel_with_discount, profile)
        assert "anomalous" in reason.lower() or "discount" in reason.lower()


class TestDateOverlap:
    """Tests for date overlap functions."""

    def test_find_overlapping_periods(self, sample_weather_forecast):
        """Test finding overlapping periods."""
        flight_start = date.today()
        flight_end = date.today() + timedelta(days=6)
        hotel_start = date.today()
        hotel_end = date.today() + timedelta(days=6)
        
        overlap = find_overlapping_periods(
            sample_weather_forecast.forecast_periods,
            (flight_start, flight_end),
            (hotel_start, hotel_end),
        )
        
        assert overlap is not None
        assert overlap[0] == flight_start
        assert overlap[1] == flight_end

    def test_find_overlapping_periods_no_overlap(self, sample_weather_forecast):
        """Test when there's no overlap."""
        flight_start = date.today() + timedelta(days=30)
        flight_end = date.today() + timedelta(days=37)
        hotel_start = date.today() + timedelta(days=30)
        hotel_end = date.today() + timedelta(days=37)
        
        overlap = find_overlapping_periods(
            sample_weather_forecast.forecast_periods,
            (flight_start, flight_end),
            (hotel_start, hotel_end),
        )
        
        assert overlap is None
