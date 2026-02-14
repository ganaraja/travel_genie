"""Tests for user profile with citizenship fields."""

import pytest
from core.models import UserProfile, ComfortLevel
from tools.user_profile import _MOCK_PROFILES


class TestUserProfileCitizenship:
    """Tests for UserProfile citizenship fields."""

    def test_user_profile_has_citizenship_field(self):
        """Test that UserProfile has citizenship field."""
        profile = UserProfile(
            user_id="test",
            citizenship="USA",
            passport_country="USA",
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
        
        assert hasattr(profile, "citizenship")
        assert profile.citizenship == "USA"

    def test_user_profile_has_passport_country_field(self):
        """Test that UserProfile has passport_country field."""
        profile = UserProfile(
            user_id="test",
            citizenship="USA",
            passport_country="USA",
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
        
        assert hasattr(profile, "passport_country")
        assert profile.passport_country == "USA"

    def test_user_profile_citizenship_defaults_to_usa(self):
        """Test that citizenship defaults to USA."""
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
        
        assert profile.citizenship == "USA"
        assert profile.passport_country == "USA"

    def test_user_profile_different_citizenships(self):
        """Test creating profiles with different citizenships."""
        citizenships = ["USA", "India", "UK", "Canada", "France", "Japan"]
        
        for citizenship in citizenships:
            profile = UserProfile(
                user_id=f"test_{citizenship}",
                citizenship=citizenship,
                passport_country=citizenship,
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
            
            assert profile.citizenship == citizenship
            assert profile.passport_country == citizenship

    def test_mock_profiles_have_citizenship(self):
        """Test that mock profiles include citizenship fields."""
        for user_id, profile in _MOCK_PROFILES.items():
            assert hasattr(profile, "citizenship")
            assert hasattr(profile, "passport_country")
            assert isinstance(profile.citizenship, str)
            assert isinstance(profile.passport_country, str)
            assert len(profile.citizenship) > 0
            assert len(profile.passport_country) > 0

    def test_mock_profile_user_123_citizenship(self):
        """Test user_123 mock profile citizenship."""
        profile = _MOCK_PROFILES["user_123"]
        
        assert profile.citizenship == "USA"
        assert profile.passport_country == "USA"

    def test_mock_profile_default_citizenship(self):
        """Test default mock profile citizenship."""
        profile = _MOCK_PROFILES["default"]
        
        assert profile.citizenship == "USA"
        assert profile.passport_country == "USA"

    def test_user_profile_citizenship_passport_can_differ(self):
        """Test that citizenship and passport_country can be different."""
        # Example: Dual citizenship or different passport
        profile = UserProfile(
            user_id="test_dual",
            citizenship="USA",
            passport_country="UK",  # Different from citizenship
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
        
        assert profile.citizenship == "USA"
        assert profile.passport_country == "UK"
        assert profile.citizenship != profile.passport_country


class TestUserProfileIntegration:
    """Integration tests for user profile with visa checking."""

    def test_profile_citizenship_used_for_visa_check(self):
        """Test that profile citizenship is used for visa requirements."""
        from api_server import check_visa_requirements
        
        profile = _MOCK_PROFILES["user_123"]
        
        # Check visa for USA citizen going to Japan
        visa_info = check_visa_requirements("Japan", profile.citizenship)
        
        assert visa_info["citizenship"] == profile.citizenship
        assert visa_info["country"] == "Japan"

    def test_profile_supports_multiple_nationalities(self):
        """Test creating profiles for different nationalities."""
        nationalities = [
            ("India", "India"),
            ("UK", "UK"),
            ("Canada", "Canada"),
            ("Australia", "Australia"),
        ]
        
        for citizenship, passport in nationalities:
            profile = UserProfile(
                user_id=f"test_{citizenship}",
                citizenship=citizenship,
                passport_country=passport,
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
            
            assert profile.citizenship == citizenship
            assert profile.passport_country == passport
