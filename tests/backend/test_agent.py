"""Tests for agent module."""

import pytest
import os
from unittest.mock import patch, MagicMock


class TestAgentStructure:
    """Tests for agent structure and configuration."""

    def test_agent_import(self):
        """Test that agent can be imported."""
        # This test verifies the agent module structure
        try:
            from agent.coordinator import root_agent
            assert root_agent is not None
            assert hasattr(root_agent, 'name')
            assert root_agent.name == "travel_coordinator"
        except ImportError as e:
            # If dependencies aren't installed, that's OK for structure test
            if "google.adk" in str(e).lower():
                pytest.skip("Google ADK not installed - structure test skipped")
            else:
                raise

    def test_agent_has_tools(self):
        """Test that agent has tools configured."""
        try:
            from agent.coordinator import root_agent
            if hasattr(root_agent, 'tools'):
                assert len(root_agent.tools) > 0
                # Should have at least 4 tools
                assert len(root_agent.tools) >= 4
        except ImportError:
            pytest.skip("Google ADK not installed")

    def test_agent_tool_functions_exist(self):
        """Test that tool wrapper functions exist."""
        from agent.coordinator import (
            get_user_profile_tool,
            get_weather_forecast_tool,
            search_flights_tool,
            search_hotels_tool,
        )
        
        assert callable(get_user_profile_tool)
        assert callable(get_weather_forecast_tool)
        assert callable(search_flights_tool)
        assert callable(search_hotels_tool)

    def test_get_user_profile_tool(self):
        """Test user profile tool wrapper."""
        from agent.coordinator import get_user_profile_tool
        
        result = get_user_profile_tool("user_123")
        
        assert isinstance(result, dict)
        assert "user_id" in result
        assert "preferred_temp_range" in result
        assert "airfare_budget_soft" in result

    def test_get_weather_forecast_tool(self):
        """Test weather forecast tool wrapper."""
        from agent.coordinator import get_weather_forecast_tool
        
        result = get_weather_forecast_tool("Maui")
        
        assert isinstance(result, dict)
        assert "destination" in result
        assert "overall_summary" in result
        assert "periods" in result

    def test_search_flights_tool(self):
        """Test flight search tool wrapper."""
        from agent.coordinator import search_flights_tool
        from datetime import date, timedelta
        
        today = date.today()
        result = search_flights_tool(
            origin="SFO",
            destination="OGG",
            departure_date=(today + timedelta(days=7)).isoformat(),
            return_date=(today + timedelta(days=14)).isoformat(),
        )
        
        assert isinstance(result, dict)
        assert "origin" in result
        assert "destination" in result
        assert "options" in result

    def test_search_hotels_tool(self):
        """Test hotel search tool wrapper."""
        from agent.coordinator import search_hotels_tool
        from datetime import date, timedelta
        
        today = date.today()
        result = search_hotels_tool(
            destination="Maui",
            check_in_date=(today + timedelta(days=7)).isoformat(),
            check_out_date=(today + timedelta(days=14)).isoformat(),
        )
        
        assert isinstance(result, dict)
        assert "destination" in result
        assert "options" in result
