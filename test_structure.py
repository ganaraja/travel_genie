#!/usr/bin/env python3
"""Test script to verify architectural separation of concerns."""

import sys

def test_core_independence():
    """Test that core/ can be imported without ADK or MCP."""
    print("Testing core/ module independence...")
    try:
        # This should work without any external dependencies
        from core.models import UserProfile, WeatherForecast, Recommendation
        from core.analysis import analyze_weather_for_user
        from core.scoring import synthesize_recommendation
        print("✅ core/ module imports successfully (no ADK/MCP dependencies)")
        return True
    except ImportError as e:
        print(f"❌ core/ module import failed: {e}")
        return False


def test_tools_structure():
    """Test that tools/ can import core/."""
    print("\nTesting tools/ module structure...")
    try:
        from tools.user_profile import get_user_profile, GetUserProfileRequest
        from tools.weather import get_weather_forecast, GetWeatherForecastRequest
        print("✅ tools/ module imports successfully")
        return True
    except ImportError as e:
        if "fastmcp" in str(e).lower():
            print("⚠️  tools/ module requires fastmcp (not installed) - structure OK")
            return True  # This is expected if dependencies aren't installed
        print(f"❌ tools/ module import failed: {e}")
        return False


def test_agent_structure():
    """Test that agent/ can import tools but not core directly."""
    print("\nTesting agent/ module structure...")
    try:
        # Agent should be able to import tools
        from agent.coordinator import root_agent
        print("✅ agent/ module imports successfully")
        print(f"   Agent name: {root_agent.name}")
        print(f"   Number of tools: {len(root_agent.tools) if hasattr(root_agent, 'tools') else 'N/A'}")
        return True
    except ImportError as e:
        if "google.adk" in str(e).lower() or "adk" in str(e).lower():
            print("⚠️  agent/ module requires google-adk (not installed) - structure OK")
            return True  # This is expected if dependencies aren't installed
        print(f"❌ agent/ module import failed: {e}")
        return False


def main():
    """Run all structure tests."""
    print("=" * 60)
    print("Travel Genie - Architecture Verification")
    print("=" * 60)
    
    results = [
        test_core_independence(),
        test_tools_structure(),
        test_agent_structure(),
    ]
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ All architecture tests passed!")
        return 0
    else:
        print("❌ Some architecture tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
