"""Tests for destination-specific weather, flights, and hotels."""

import pytest
from datetime import date, timedelta
from agent.coordinator import (
    get_weather_forecast_tool,
    search_flights_tool,
    search_hotels_tool
)


class TestDestinationSpecificWeather:
    """Tests that weather varies by destination."""

    def test_maui_tropical_weather(self):
        """Test Maui has tropical weather with warm temperatures."""
        weather = get_weather_forecast_tool("Maui")
        
        assert weather["destination"] == "Maui"
        # Tropical destinations should be warm (75-90°F range)
        for period in weather["periods"]:
            assert 75 <= period["avg_temp_f"] <= 90, f"Maui temp {period['avg_temp_f']} not in tropical range"
        
        # Check climate type mentioned in summary
        assert "tropical" in weather["overall_summary"].lower()

    def test_zurich_alpine_weather(self):
        """Test Zurich has alpine/cool weather."""
        weather = get_weather_forecast_tool("Zurich")
        
        assert weather["destination"] == "Zurich"
        # Alpine destinations should be cooler (40-65°F range)
        for period in weather["periods"]:
            assert 40 <= period["avg_temp_f"] <= 65, f"Zurich temp {period['avg_temp_f']} not in alpine range"
        
        # Check climate type mentioned in summary
        assert "alpine" in weather["overall_summary"].lower()

    def test_dubai_desert_weather(self):
        """Test Dubai has hot desert weather."""
        weather = get_weather_forecast_tool("Dubai")
        
        assert weather["destination"] == "Dubai"
        # Desert destinations should be hot (80-100°F range)
        for period in weather["periods"]:
            assert 80 <= period["avg_temp_f"] <= 105, f"Dubai temp {period['avg_temp_f']} not in desert range"
        
        # Check climate type mentioned in summary
        assert "desert" in weather["overall_summary"].lower()

    def test_paris_temperate_weather(self):
        """Test Paris has temperate weather."""
        weather = get_weather_forecast_tool("Paris")
        
        assert weather["destination"] == "Paris"
        # Temperate destinations should be moderate (45-70°F range)
        for period in weather["periods"]:
            assert 45 <= period["avg_temp_f"] <= 75, f"Paris temp {period['avg_temp_f']} not in temperate range"
        
        # Check climate type mentioned in summary
        assert "temperate" in weather["overall_summary"].lower()

    def test_tokyo_temperate_weather(self):
        """Test Tokyo has temperate weather with wider variation."""
        weather = get_weather_forecast_tool("Tokyo")
        
        assert weather["destination"] == "Tokyo"
        # Tokyo should have moderate temps with variation
        temps = [period["avg_temp_f"] for period in weather["periods"]]
        assert 50 <= min(temps) <= 75, "Tokyo min temp out of range"
        assert 55 <= max(temps) <= 80, "Tokyo max temp out of range"

    def test_bangalore_tropical_weather(self):
        """Test Bangalore has tropical weather."""
        weather = get_weather_forecast_tool("Bangalore")
        
        assert weather["destination"] == "Bangalore"
        # Bangalore should be warm tropical
        for period in weather["periods"]:
            assert 70 <= period["avg_temp_f"] <= 90, f"Bangalore temp {period['avg_temp_f']} not in tropical range"
        
        assert "tropical" in weather["overall_summary"].lower()

    def test_different_destinations_different_temps(self):
        """Test that different destinations have significantly different temperatures."""
        maui = get_weather_forecast_tool("Maui")
        zurich = get_weather_forecast_tool("Zurich")
        dubai = get_weather_forecast_tool("Dubai")
        
        maui_avg = sum(p["avg_temp_f"] for p in maui["periods"]) / len(maui["periods"])
        zurich_avg = sum(p["avg_temp_f"] for p in zurich["periods"]) / len(zurich["periods"])
        dubai_avg = sum(p["avg_temp_f"] for p in dubai["periods"]) / len(dubai["periods"])
        
        # Zurich should be significantly cooler than Maui
        assert zurich_avg < maui_avg - 20, "Zurich should be much cooler than Maui"
        
        # Dubai should be hotter than Maui
        assert dubai_avg > maui_avg, "Dubai should be hotter than Maui"
        
        # Dubai should be much hotter than Zurich
        assert dubai_avg > zurich_avg + 30, "Dubai should be much hotter than Zurich"

    def test_storm_risk_varies_by_destination(self):
        """Test that storm risk is destination-specific."""
        # Maui has storms at week 7
        maui = get_weather_forecast_tool("Maui")
        maui_storms = [p for p in maui["periods"] if p["storm_risk"]]
        assert len(maui_storms) > 0, "Maui should have storm risk"
        
        # Paris has no storms
        paris = get_weather_forecast_tool("Paris")
        paris_storms = [p for p in paris["periods"] if p["storm_risk"]]
        assert len(paris_storms) == 0, "Paris should have no storm risk"
        
        # Dubai has no storms (desert)
        dubai = get_weather_forecast_tool("Dubai")
        dubai_storms = [p for p in dubai["periods"] if p["storm_risk"]]
        assert len(dubai_storms) == 0, "Dubai should have no storm risk"
        
        # Bangkok has storms (tropical)
        bangkok = get_weather_forecast_tool("Bangkok")
        bangkok_storms = [p for p in bangkok["periods"] if p["storm_risk"]]
        assert len(bangkok_storms) > 0, "Bangkok should have storm risk"


class TestDestinationSpecificFlights:
    """Tests that flight durations and prices vary by destination."""

    def test_maui_short_flight(self):
        """Test Maui has short flight duration from SFO."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "OGG", dep_date, ret_date)
        
        assert len(flights["options"]) > 0
        # Maui flights should be 5-9 hours
        for flight in flights["options"]:
            assert 5 <= flight["total_duration_hours"] <= 9, \
                f"Maui flight duration {flight['total_duration_hours']}h not in expected range"

    def test_zurich_long_flight(self):
        """Test Zurich has long flight duration from SFO."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "ZRH", dep_date, ret_date)
        
        assert len(flights["options"]) > 0
        # Zurich flights should be 10-15 hours
        for flight in flights["options"]:
            assert 10 <= flight["total_duration_hours"] <= 15, \
                f"Zurich flight duration {flight['total_duration_hours']}h not in expected range"

    def test_bangalore_very_long_flight(self):
        """Test Bangalore has very long flight duration from SFO."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "BLR", dep_date, ret_date)
        
        assert len(flights["options"]) > 0
        # Bangalore flights should be 16-22 hours
        for flight in flights["options"]:
            assert 16 <= flight["total_duration_hours"] <= 22, \
                f"Bangalore flight duration {flight['total_duration_hours']}h not in expected range"

    def test_tokyo_medium_flight(self):
        """Test Tokyo has medium flight duration from SFO."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        flights = search_flights_tool("SFO", "NRT", dep_date, ret_date)
        
        assert len(flights["options"]) > 0
        # Tokyo flights should be 10-15 hours
        for flight in flights["options"]:
            assert 10 <= flight["total_duration_hours"] <= 15, \
                f"Tokyo flight duration {flight['total_duration_hours']}h not in expected range"

    def test_different_destinations_different_durations(self):
        """Test that flight durations vary significantly by destination."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        maui = search_flights_tool("SFO", "OGG", dep_date, ret_date)
        zurich = search_flights_tool("SFO", "ZRH", dep_date, ret_date)
        bangalore = search_flights_tool("SFO", "BLR", dep_date, ret_date)
        
        maui_duration = maui["options"][0]["total_duration_hours"]
        zurich_duration = zurich["options"][0]["total_duration_hours"]
        bangalore_duration = bangalore["options"][0]["total_duration_hours"]
        
        # Maui should be shortest
        assert maui_duration < zurich_duration, "Maui should be shorter than Zurich"
        assert maui_duration < bangalore_duration, "Maui should be shorter than Bangalore"
        
        # Bangalore should be longest
        assert bangalore_duration > zurich_duration, "Bangalore should be longer than Zurich"
        assert bangalore_duration > maui_duration + 10, "Bangalore should be much longer than Maui"

    def test_destination_specific_airlines(self):
        """Test that airlines vary by destination."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        # Maui should have Hawaiian airlines
        maui = search_flights_tool("SFO", "OGG", dep_date, ret_date)
        maui_airlines = {f["airline"] for f in maui["options"]}
        assert "Hawaiian" in maui_airlines, "Maui should have Hawaiian airlines"
        
        # Zurich should have Swiss airlines
        zurich = search_flights_tool("SFO", "ZRH", dep_date, ret_date)
        zurich_airlines = {f["airline"] for f in zurich["options"]}
        assert "Swiss" in zurich_airlines, "Zurich should have Swiss airlines"
        
        # Bangalore should have Air India
        bangalore = search_flights_tool("SFO", "BLR", dep_date, ret_date)
        bangalore_airlines = {f["airline"] for f in bangalore["options"]}
        assert "Air India" in bangalore_airlines, "Bangalore should have Air India"

    def test_destination_specific_prices(self):
        """Test that flight prices vary by destination distance."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        maui = search_flights_tool("SFO", "OGG", dep_date, ret_date)
        zurich = search_flights_tool("SFO", "ZRH", dep_date, ret_date)
        bangalore = search_flights_tool("SFO", "BLR", dep_date, ret_date)
        
        maui_price = min(f["price_usd"] for f in maui["options"])
        zurich_price = min(f["price_usd"] for f in zurich["options"])
        bangalore_price = min(f["price_usd"] for f in bangalore["options"])
        
        # Longer flights should generally be more expensive
        assert maui_price < zurich_price, "Maui should be cheaper than Zurich"
        assert maui_price < bangalore_price, "Maui should be cheaper than Bangalore"


class TestDestinationSpecificHotels:
    """Tests that hotels are destination-specific."""

    def test_hotel_names_include_destination(self):
        """Test that hotel names include the destination."""
        today = date.today()
        check_in = (today + timedelta(days=14)).isoformat()
        check_out = (today + timedelta(days=21)).isoformat()
        
        maui = search_hotels_tool("Maui", check_in, check_out)
        zurich = search_hotels_tool("Zurich", check_in, check_out)
        bangalore = search_hotels_tool("Bangalore", check_in, check_out)
        
        # Check hotel names include destination
        for hotel in maui["options"]:
            assert "Maui" in hotel["name"], f"Hotel name should include Maui: {hotel['name']}"
        
        for hotel in zurich["options"]:
            assert "Zurich" in hotel["name"], f"Hotel name should include Zurich: {hotel['name']}"
        
        for hotel in bangalore["options"]:
            assert "Bangalore" in hotel["name"], f"Hotel name should include Bangalore: {hotel['name']}"

    def test_hotels_return_for_all_destinations(self):
        """Test that hotels are returned for various destinations."""
        today = date.today()
        check_in = (today + timedelta(days=14)).isoformat()
        check_out = (today + timedelta(days=21)).isoformat()
        
        destinations = ["Maui", "Zurich", "Tokyo", "Bangalore", "Paris", "Dubai"]
        
        for dest in destinations:
            hotels = search_hotels_tool(dest, check_in, check_out)
            assert len(hotels["options"]) > 0, f"No hotels found for {dest}"
            assert hotels["destination"] == dest
            
            # Verify all hotels have the destination in their name
            for hotel in hotels["options"]:
                assert dest in hotel["name"], f"Hotel name missing destination: {hotel['name']}"


class TestEndToEndDestinationSpecificity:
    """Integration tests for complete destination-specific recommendations."""

    def test_maui_recommendation_consistency(self):
        """Test that Maui recommendation has consistent tropical characteristics."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        weather = get_weather_forecast_tool("Maui")
        flights = search_flights_tool("SFO", "OGG", dep_date, ret_date)
        hotels = search_hotels_tool("Maui", dep_date, ret_date)
        
        # Weather should be tropical
        assert "tropical" in weather["overall_summary"].lower()
        avg_temp = sum(p["avg_temp_f"] for p in weather["periods"]) / len(weather["periods"])
        assert 75 <= avg_temp <= 90, "Maui should have tropical temperatures"
        
        # Flights should be short
        assert flights["options"][0]["total_duration_hours"] < 10, "Maui flights should be under 10 hours"
        
        # Hotels should be for Maui
        assert all("Maui" in h["name"] for h in hotels["options"])

    def test_zurich_recommendation_consistency(self):
        """Test that Zurich recommendation has consistent alpine characteristics."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        weather = get_weather_forecast_tool("Zurich")
        flights = search_flights_tool("SFO", "ZRH", dep_date, ret_date)
        hotels = search_hotels_tool("Zurich", dep_date, ret_date)
        
        # Weather should be alpine/cool
        assert "alpine" in weather["overall_summary"].lower()
        avg_temp = sum(p["avg_temp_f"] for p in weather["periods"]) / len(weather["periods"])
        assert 40 <= avg_temp <= 65, "Zurich should have alpine temperatures"
        
        # Flights should be long (transatlantic)
        assert flights["options"][0]["total_duration_hours"] >= 10, "Zurich flights should be 10+ hours"
        
        # Hotels should be for Zurich
        assert all("Zurich" in h["name"] for h in hotels["options"])

    def test_bangalore_recommendation_consistency(self):
        """Test that Bangalore recommendation has consistent tropical characteristics."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        weather = get_weather_forecast_tool("Bangalore")
        flights = search_flights_tool("SFO", "BLR", dep_date, ret_date)
        hotels = search_hotels_tool("Bangalore", dep_date, ret_date)
        
        # Weather should be tropical
        assert "tropical" in weather["overall_summary"].lower()
        avg_temp = sum(p["avg_temp_f"] for p in weather["periods"]) / len(weather["periods"])
        assert 70 <= avg_temp <= 90, "Bangalore should have tropical temperatures"
        
        # Flights should be very long (to India)
        assert flights["options"][0]["total_duration_hours"] >= 16, "Bangalore flights should be 16+ hours"
        
        # Hotels should be for Bangalore
        assert all("Bangalore" in h["name"] for h in hotels["options"])

    def test_multiple_destinations_are_distinct(self):
        """Test that recommendations for different destinations are clearly distinct."""
        today = date.today()
        dep_date = (today + timedelta(days=14)).isoformat()
        ret_date = (today + timedelta(days=21)).isoformat()
        
        destinations = [
            ("Maui", "OGG"),
            ("Zurich", "ZRH"),
            ("Tokyo", "NRT"),
            ("Bangalore", "BLR"),
            ("Dubai", "DXB")
        ]
        
        weather_data = {}
        flight_data = {}
        hotel_data = {}
        
        for dest_name, airport_code in destinations:
            weather_data[dest_name] = get_weather_forecast_tool(dest_name)
            flight_data[dest_name] = search_flights_tool("SFO", airport_code, dep_date, ret_date)
            hotel_data[dest_name] = search_hotels_tool(dest_name, dep_date, ret_date)
        
        # Verify each destination has unique characteristics
        temps = {dest: sum(p["avg_temp_f"] for p in weather_data[dest]["periods"]) / len(weather_data[dest]["periods"]) 
                 for dest, _ in destinations}
        
        durations = {dest: flight_data[dest]["options"][0]["total_duration_hours"] 
                     for dest, _ in destinations}
        
        # Temperatures should vary significantly
        temp_range = max(temps.values()) - min(temps.values())
        assert temp_range > 30, "Destinations should have at least 30°F temperature variation"
        
        # Flight durations should vary significantly
        duration_range = max(durations.values()) - min(durations.values())
        assert duration_range > 10, "Destinations should have at least 10 hour flight duration variation"
        
        # All hotels should have correct destination names
        for dest_name, _ in destinations:
            for hotel in hotel_data[dest_name]["options"]:
                assert dest_name in hotel["name"], f"Hotel should be in {dest_name}: {hotel['name']}"
