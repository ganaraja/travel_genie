"""Unified FastMCP server combining all travel tools."""

from fastmcp import FastMCP

# Create unified MCP server
mcp = FastMCP("Travel Genie")

# Import the raw tool functions (before decoration)
# and register them with our unified server
from tools.user_profile import GetUserProfileRequest, UserProfileResponse, _MOCK_PROFILES
from tools.weather import GetWeatherForecastRequest, WeatherForecastResponse
from tools.flights import SearchFlightsRequest, FlightSearchResponse
from tools.hotels import SearchHotelsRequest, HotelSearchResponse

from core.models import UserProfile, ComfortLevel
from datetime import date, timedelta


@mcp.tool()
def get_user_profile(request: GetUserProfileRequest) -> UserProfileResponse:
    """
    Retrieve user profile with travel preferences and constraints.
    
    This tool must be called before consulting external data sources.
    The profile contains structured fields needed for personalized recommendations.
    """
    profile = _MOCK_PROFILES.get(request.user_id, _MOCK_PROFILES["default"])
    
    return UserProfileResponse(
        user_id=profile.user_id,
        preferred_temp_range=profile.preferred_temp_range,
        airfare_budget_soft=profile.airfare_budget_soft,
        airfare_budget_hard=profile.airfare_budget_hard,
        hotel_budget_min=profile.hotel_budget_min,
        hotel_budget_max=profile.hotel_budget_max,
        preferred_brands=profile.preferred_brands,
        typical_trip_length_days=profile.typical_trip_length_days,
        comfort_level=profile.comfort_level.value,
        flexibility_days=profile.flexibility_days,
        safety_conscious=profile.safety_conscious,
        visa_required=profile.visa_required,
    )


@mcp.tool()
def get_weather_forecast(request: GetWeatherForecastRequest) -> WeatherForecastResponse:
    """
    Retrieve forward-looking weather forecast for a destination.
    
    Provides summarized weather data with storm periods explicitly flagged.
    """
    from tools.weather import WeatherPeriodResponse
    
    start = date.fromisoformat(request.start_date)
    periods = []
    
    for week in range(0, min(request.days_ahead, 30), 7):
        period_start = start + timedelta(days=week)
        period_end = min(period_start + timedelta(days=6), start + timedelta(days=request.days_ahead - 1))
        
        base_temp = 82.0
        temp_variation = (week % 3) * 3.0
        has_storm = week == 7
        storm_severity = "moderate" if has_storm else None
        avg_temp = base_temp + temp_variation
        
        conditions = "Warm and mostly sunny"
        if has_storm:
            conditions = "Moderate storm expected with increased precipitation"
        elif avg_temp > 85:
            conditions = "Hot and sunny"
        
        periods.append(WeatherPeriodResponse(
            start_date=period_start.isoformat(),
            end_date=period_end.isoformat(),
            avg_temp_f=avg_temp,
            storm_risk=has_storm,
            storm_severity=storm_severity,
            conditions_summary=conditions,
        ))
    
    storm_periods = [p for p in periods if p.storm_risk]
    if storm_periods:
        summary = (
            f"Forecast for {request.destination}: Generally warm weather ({periods[0].avg_temp_f:.0f}-{periods[-1].avg_temp_f:.0f}°F). "
            f"Storm risk identified: {storm_periods[0].start_date} to {storm_periods[0].end_date} ({storm_periods[0].storm_severity} severity). "
            f"Other periods are clear."
        )
    else:
        summary = (
            f"Forecast for {request.destination}: Stable warm weather expected "
            f"({periods[0].avg_temp_f:.0f}-{periods[-1].avg_temp_f:.0f}°F) with minimal precipitation."
        )
    
    return WeatherForecastResponse(
        destination=request.destination,
        overall_summary=summary,
        periods=periods,
    )


@mcp.tool()
def search_flights(request: SearchFlightsRequest) -> FlightSearchResponse:
    """
    Search for flight options between origin and destination.
    
    Considers schedule flexibility and returns multiple candidate itineraries.
    """
    from tools.flights import FlightOptionResponse
    
    dep_date = date.fromisoformat(request.departure_date)
    ret_date = date.fromisoformat(request.return_date)
    options = []
    base_prices = [550, 620, 680, 720, 750, 800, 850]
    
    for day_offset in range(-request.flexibility_days, request.flexibility_days + 1):
        candidate_dep = dep_date + timedelta(days=day_offset)
        candidate_ret = ret_date + timedelta(days=day_offset)
        
        if candidate_dep >= date.today() and candidate_ret > candidate_dep:
            day_of_week = candidate_dep.weekday()
            base_price = base_prices[day_of_week]
            price = base_price + (day_offset * 20) + (50 if day_of_week >= 5 else 0)
            
            for variant in range(2):
                is_red_eye = variant == 1
                is_weekday = day_of_week < 5
                if is_red_eye:
                    price *= 0.85
                
                options.append(FlightOptionResponse(
                    departure_date=candidate_dep.isoformat(),
                    return_date=candidate_ret.isoformat(),
                    price_usd=price,
                    airline="United" if variant == 0 else "Hawaiian",
                    departure_time="08:30" if not is_red_eye else "23:45",
                    return_time="14:20",
                    is_red_eye=is_red_eye,
                    is_weekday=is_weekday,
                    layovers=1 if variant == 0 else 0,
                    total_duration_hours=8.5 if variant == 0 else 6.0,
                    booking_code=f"FLT-{candidate_dep.isoformat()}-{variant}",
                ))
    
    options.sort(key=lambda x: x.price_usd)
    
    if options:
        min_price = min(o.price_usd for o in options)
        max_price = max(o.price_usd for o in options)
        weekday_options = [o for o in options if o.is_weekday]
        red_eye_options = [o for o in options if o.is_red_eye]
        summary = (
            f"Found {len(options)} flight options. Price range: ${min_price:.0f}-${max_price:.0f}. "
            f"{len(weekday_options)} weekday options, {len(red_eye_options)} red-eye options available."
        )
    else:
        summary = "No flight options found for specified dates."
    
    return FlightSearchResponse(
        origin=request.origin,
        destination=request.destination,
        options=options[:10],
        summary=summary,
    )


@mcp.tool()
def search_hotels(request: SearchHotelsRequest) -> HotelSearchResponse:
    """
    Search for hotel options at a destination.
    
    Evaluates lodging options with brand loyalty and anomalous pricing detection.
    """
    from tools.hotels import HotelOptionResponse
    
    check_in = date.fromisoformat(request.check_in_date)
    check_out = date.fromisoformat(request.check_out_date)
    nights = (check_out - check_in).days
    
    if nights <= 0:
        return HotelSearchResponse(
            destination=request.destination,
            options=[],
            summary="Invalid date range.",
        )
    
    brands = ["Marriott", "Hilton", "Hyatt", "Westin", "Four Seasons", "Budget Inn"]
    options = []
    
    for i, brand in enumerate(brands):
        base_rate = 120.0 + (i * 40.0)
        is_preferred = brand in request.preferred_brands
        if is_preferred:
            base_rate *= 0.95
        
        is_anomalous = False
        anomalous_reason = None
        if i < 2 and check_in.day % 7 == 0:
            is_anomalous = True
            anomalous_reason = "Storm discount - reduced rates due to weather forecast"
            base_rate *= 0.75
        
        rating = min(5.0, 3.0 + (i * 0.4))
        nightly_rate = base_rate
        total_price = nightly_rate * nights
        
        options.append(HotelOptionResponse(
            check_in_date=check_in.isoformat(),
            check_out_date=check_out.isoformat(),
            nightly_rate_usd=nightly_rate,
            total_price_usd=total_price,
            brand=brand,
            name=f"{brand} {request.destination}",
            rating=rating,
            is_anomalous_pricing=is_anomalous,
            anomalous_reason=anomalous_reason,
            booking_code=f"HTL-{check_in.isoformat()}-{brand}-{i}",
        ))
    
    options.sort(key=lambda x: x.nightly_rate_usd)
    
    if options:
        min_rate = min(o.nightly_rate_usd for o in options)
        max_rate = max(o.nightly_rate_usd for o in options)
        preferred_matches = [o for o in options if o.brand in request.preferred_brands]
        anomalous = [o for o in options if o.is_anomalous_pricing]
        
        summary = f"Found {len(options)} hotel options. Nightly rate range: ${min_rate:.0f}-${max_rate:.0f}. "
        if preferred_matches:
            summary += f"{len(preferred_matches)} options match preferred brands. "
        if anomalous:
            summary += f"{len(anomalous)} option(s) with anomalous pricing detected."
    else:
        summary = "No hotel options found for specified dates."
    
    return HotelSearchResponse(
        destination=request.destination,
        options=options,
        summary=summary,
    )


if __name__ == "__main__":
    mcp.run()
