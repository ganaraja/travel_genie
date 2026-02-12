#!/usr/bin/env python3
"""Quick verification script for Travel Genie system."""

import sys
from datetime import date, timedelta


def test_core_imports():
    """Test that core module imports without external dependencies."""
    print("Testing core module imports...")
    try:
        from core.models import UserProfile, ComfortLevel, WeatherPeriod, FlightOption, HotelOption
        from core.analysis import analyze_weather_for_user, score_flight_option, score_hotel_option
        from core.scoring import synthesize_recommendation
        print("✅ Core module imports successfully")
        return True
    except Exception as e:
        print(f"❌ Core module import failed: {e}")
        return False


def test_tools_imports():
    """Test that tools module imports correctly."""
    print("\nTesting tools module imports...")
    try:
        from tools.user_profile import GetUserProfileRequest, UserProfileResponse
        from tools.weather import GetWeatherForecastRequest, WeatherForecastResponse
        from tools.flights import SearchFlightsRequest, FlightSearchResponse
        from tools.hotels import SearchHotelsRequest, HotelSearchResponse
        print("✅ Tools module imports successfully")
        return True
    except Exception as e:
        print(f"❌ Tools module import failed: {e}")
        return False


def test_core_logic():
    """Test basic core logic functionality."""
    print("\nTesting core logic functionality...")
    try:
        from core.models import UserProfile, ComfortLevel, WeatherPeriod, WeatherForecast
        from core.analysis import analyze_weather_for_user
        
        # Create test data
        profile = UserProfile(
            user_id="test",
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
        
        period = WeatherPeriod(
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7),
            avg_temp_f=80.0,
            min_temp_f=75.0,
            max_temp_f=85.0,
            precipitation_inches=0.1,
            storm_risk=False,
        )
        
        forecast = WeatherForecast(
            destination="Maui",
            forecast_periods=[period],
            overall_summary="Perfect weather",
        )
        
        # Test analysis
        results = analyze_weather_for_user(forecast, profile)
        assert len(results) == 1
        assert results[0][1] > 0.9  # Should have high score
        
        print("✅ Core logic works correctly")
        return True
    except Exception as e:
        print(f"❌ Core logic test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_functions():
    """Test that tool functions work (not wrapped tools)."""
    print("\nTesting tool functions...")
    try:
        from tools.user_profile import GetUserProfileRequest, _MOCK_PROFILES
        from tools.weather import GetWeatherForecastRequest
        from tools.flights import SearchFlightsRequest
        from tools.hotels import SearchHotelsRequest
        
        # Test user profile
        assert "user_123" in _MOCK_PROFILES
        assert "default" in _MOCK_PROFILES
        
        # Test request models
        profile_req = GetUserProfileRequest(user_id="user_123")
        assert profile_req.user_id == "user_123"
        
        weather_req = GetWeatherForecastRequest(
            destination="Maui",
            start_date=date.today().isoformat(),
            days_ahead=30,
        )
        assert weather_req.destination == "Maui"
        
        print("✅ Tool functions work correctly")
        return True
    except Exception as e:
        print(f"❌ Tool functions test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_architecture_separation():
    """Test that architecture separation is maintained."""
    print("\nTesting architecture separation...")
    try:
        # Core should not import ADK or MCP
        import core.models
        import core.analysis
        import core.scoring
        
        # Check that core modules don't have ADK/MCP imports
        core_modules = [core.models, core.analysis, core.scoring]
        for module in core_modules:
            source = module.__file__
            with open(source, 'r') as f:
                content = f.read()
                if 'google.adk' in content or 'fastmcp' in content:
                    print(f"❌ {module.__name__} imports ADK or MCP!")
                    return False
        
        print("✅ Architecture separation maintained")
        return True
    except Exception as e:
        print(f"❌ Architecture test failed: {e}")
        return False


def main():
    """Run all verification tests."""
    print("=" * 60)
    print("Travel Genie System Verification")
    print("=" * 60)
    
    results = []
    results.append(("Core Imports", test_core_imports()))
    results.append(("Tools Imports", test_tools_imports()))
    results.append(("Core Logic", test_core_logic()))
    results.append(("Tool Functions", test_tool_functions()))
    results.append(("Architecture Separation", test_architecture_separation()))
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:.<40} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All verification tests passed!")
        print("\nNext steps:")
        print("1. Review CURRENT_STATUS.md for known issues")
        print("2. Review QUICKSTART.md for usage instructions")
        print("3. Start implementing improvements from tasks.md")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check output above for details.")
        print("\nSee CURRENT_STATUS.md for troubleshooting guidance.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
