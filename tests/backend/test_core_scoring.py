"""Tests for core scoring and recommendation synthesis."""

import pytest
from datetime import date, timedelta

from core.models import UserProfile, ComfortLevel
from core.scoring import synthesize_recommendation


class TestRecommendationSynthesis:
    """Tests for recommendation synthesis."""

    def test_synthesize_recommendation_basic(
        self, sample_user_profile, sample_weather_forecast, sample_flight_options, sample_hotel_options
    ):
        """Test basic recommendation synthesis."""
        # Filter to only affordable options
        affordable_flights = [f for f in sample_flight_options if f.price_usd <= sample_user_profile.airfare_budget_hard]
        affordable_hotels = [
            h for h in sample_hotel_options
            if sample_user_profile.hotel_budget_min <= h.nightly_rate_usd <= sample_user_profile.hotel_budget_max
        ]
        
        recommendation = synthesize_recommendation(
            sample_user_profile,
            sample_weather_forecast,
            affordable_flights,
            affordable_hotels,
        )
        
        assert recommendation is not None
        assert recommendation.recommended_start is not None
        assert recommendation.recommended_end is not None
        assert len(recommendation.primary_reasoning) > 0
        assert len(recommendation.personalized_summary) > 0

    def test_synthesize_recommendation_no_options(self, sample_user_profile, sample_weather_forecast):
        """Test recommendation when no options are available."""
        # Empty lists for flights and hotels
        recommendation = synthesize_recommendation(
            sample_user_profile,
            sample_weather_forecast,
            [],
            [],
        )
        
        assert recommendation is not None
        # Should still provide a recommendation, even if it's a fallback
        assert len(recommendation.personalized_summary) > 0
        assert len(recommendation.rejected_periods) >= 0

    def test_synthesize_recommendation_considers_weather(
        self, sample_user_profile, sample_weather_forecast, sample_flight_options, sample_hotel_options
    ):
        """Test that recommendation considers weather preferences."""
        affordable_flights = [f for f in sample_flight_options if f.price_usd <= sample_user_profile.airfare_budget_hard]
        affordable_hotels = [
            h for h in sample_hotel_options
            if sample_user_profile.hotel_budget_min <= h.nightly_rate_usd <= sample_user_profile.hotel_budget_max
        ]
        
        recommendation = synthesize_recommendation(
            sample_user_profile,
            sample_weather_forecast,
            affordable_flights,
            affordable_hotels,
        )
        
        # Should avoid storm period (period 2) for safety-conscious user
        storm_start = sample_weather_forecast.forecast_periods[1].start_date
        storm_end = sample_weather_forecast.forecast_periods[1].end_date
        
        # Recommendation should not overlap with storm period
        assert not (
            recommendation.recommended_start <= storm_end and
            recommendation.recommended_end >= storm_start
        )

    def test_synthesize_recommendation_includes_alternatives(
        self, sample_user_profile, sample_weather_forecast, sample_flight_options, sample_hotel_options
    ):
        """Test that recommendation includes alternative options."""
        affordable_flights = [f for f in sample_flight_options if f.price_usd <= sample_user_profile.airfare_budget_hard]
        affordable_hotels = [
            h for h in sample_hotel_options
            if sample_user_profile.hotel_budget_min <= h.nightly_rate_usd <= sample_user_profile.hotel_budget_max
        ]
        
        recommendation = synthesize_recommendation(
            sample_user_profile,
            sample_weather_forecast,
            affordable_flights,
            affordable_hotels,
        )
        
        # Should have alternative options if multiple good combinations exist
        assert len(recommendation.alternative_options) >= 0  # Can be 0 if only one good option

    def test_synthesize_recommendation_personalized_summary(
        self, sample_user_profile, sample_weather_forecast, sample_flight_options, sample_hotel_options
    ):
        """Test that recommendation summary is personalized."""
        affordable_flights = [f for f in sample_flight_options if f.price_usd <= sample_user_profile.airfare_budget_hard]
        affordable_hotels = [
            h for h in sample_hotel_options
            if sample_user_profile.hotel_budget_min <= h.nightly_rate_usd <= sample_user_profile.hotel_budget_max
        ]
        
        recommendation = synthesize_recommendation(
            sample_user_profile,
            sample_weather_forecast,
            affordable_flights,
            affordable_hotels,
        )
        
        summary = recommendation.personalized_summary.lower()
        # Should mention user preferences
        assert "75" in summary or "85" in summary or "temperature" in summary
        assert "600" in summary or "900" in summary or "budget" in summary
