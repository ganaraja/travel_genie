"""Google ADK coordinator agent that orchestrates reasoning and tool use."""

import os
from datetime import date, timedelta
from typing import Optional

from google.adk.agents.llm_agent import Agent
from google.adk.tools.function_tool import FunctionTool

# Import tool functions (these will call MCP server)
# In production, these would be MCP client calls
# For now, we'll create wrapper functions that the agent can call
# Note: The agent does NOT import core logic directly - it only uses tools


def get_user_profile_tool(user_id: str) -> dict:
    """
    Retrieve user profile with travel preferences and constraints.
    
    This tool MUST be called before consulting external data sources.
    The agent must recognize that questions are underspecified without
    user profile information.
    
    Args:
        user_id: Unique identifier for the user
        
    Returns:
        Dictionary with user profile fields
    """
    # In production, this would call the MCP server
    # For now, we'll use the mock data directly
    from tools.user_profile import _MOCK_PROFILES
    
    profile = _MOCK_PROFILES.get(user_id, _MOCK_PROFILES["default"])
    
    return {
        "user_id": profile.user_id,
        "preferred_temp_range": profile.preferred_temp_range,
        "airfare_budget_soft": profile.airfare_budget_soft,
        "airfare_budget_hard": profile.airfare_budget_hard,
        "hotel_budget_min": profile.hotel_budget_min,
        "hotel_budget_max": profile.hotel_budget_max,
        "preferred_brands": profile.preferred_brands,
        "typical_trip_length_days": profile.typical_trip_length_days,
        "comfort_level": profile.comfort_level.value,
        "flexibility_days": profile.flexibility_days,
        "safety_conscious": profile.safety_conscious,
        "visa_required": profile.visa_required,
    }


def get_weather_forecast_tool(destination: str, start_date: Optional[str] = None, days_ahead: int = 30) -> dict:
    """
    Retrieve forward-looking weather forecast for a destination.
    
    Provides summarized weather data, not raw dumps:
    - 30-day forward-looking forecast
    - Storm periods explicitly flagged with severity
    - Temperature ranges and precipitation summaries
    - Brief condition summaries per period
    
    Args:
        destination: Destination city or location
        start_date: Start date in YYYY-MM-DD format (defaults to today)
        days_ahead: Number of days to forecast (max 30)
        
    Returns:
        Dictionary with weather forecast summary and periods
    """
    if start_date is None:
        start_date = date.today().isoformat()
    
    start = date.fromisoformat(start_date)
    periods = []
    
    for week in range(0, min(days_ahead, 30), 7):
        period_start = start + timedelta(days=week)
        period_end = min(period_start + timedelta(days=6), start + timedelta(days=days_ahead - 1))
        
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
        
        periods.append({
            "start_date": period_start.isoformat(),
            "end_date": period_end.isoformat(),
            "avg_temp_f": avg_temp,
            "storm_risk": has_storm,
            "storm_severity": storm_severity,
            "conditions_summary": conditions,
        })
    
    storm_periods = [p for p in periods if p["storm_risk"]]
    if storm_periods:
        overall_summary = (
            f"Forecast for {destination}: Generally warm weather ({periods[0]['avg_temp_f']:.0f}-{periods[-1]['avg_temp_f']:.0f}°F). "
            f"Storm risk identified: {storm_periods[0]['start_date']} to {storm_periods[0]['end_date']} ({storm_periods[0]['storm_severity']} severity). "
            f"Other periods are clear."
        )
    else:
        overall_summary = (
            f"Forecast for {destination}: Stable warm weather expected "
            f"({periods[0]['avg_temp_f']:.0f}-{periods[-1]['avg_temp_f']:.0f}°F) with minimal precipitation."
        )
    
    return {
        "destination": destination,
        "overall_summary": overall_summary,
        "periods": periods,
    }


def search_flights_tool(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str,
    flexibility_days: int = 3,
) -> dict:
    """
    Search for flight options between origin and destination.
    
    Considers schedule flexibility (weekday vs weekend, red-eye options)
    and returns multiple candidate itineraries. Prices must be compared
    against user affordability thresholds.
    
    Args:
        origin: Origin airport code (e.g., SFO)
        destination: Destination airport code (e.g., OGG for Maui)
        departure_date: Preferred departure date YYYY-MM-DD
        return_date: Preferred return date YYYY-MM-DD
        flexibility_days: Days +/- to consider for flexibility
        
    Returns:
        Dictionary with flight options and summary
    """
    dep_date = date.fromisoformat(departure_date)
    ret_date = date.fromisoformat(return_date)
    options = []
    base_prices = [550, 620, 680, 720, 750, 800, 850]
    
    for day_offset in range(-flexibility_days, flexibility_days + 1):
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
                
                options.append({
                    "departure_date": candidate_dep.isoformat(),
                    "return_date": candidate_ret.isoformat(),
                    "price_usd": price,
                    "airline": "United" if variant == 0 else "Hawaiian",
                    "departure_time": "08:30" if not is_red_eye else "23:45",
                    "return_time": "14:20",
                    "is_red_eye": is_red_eye,
                    "is_weekday": is_weekday,
                    "layovers": 1 if variant == 0 else 0,
                    "total_duration_hours": 8.5 if variant == 0 else 6.0,
                    "booking_code": f"FLT-{candidate_dep.isoformat()}-{variant}",
                })
    
    options.sort(key=lambda x: x["price_usd"])
    
    if options:
        min_price = min(o["price_usd"] for o in options)
        max_price = max(o["price_usd"] for o in options)
        weekday_options = [o for o in options if o["is_weekday"]]
        red_eye_options = [o for o in options if o["is_red_eye"]]
        summary = (
            f"Found {len(options)} flight options. Price range: ${min_price:.0f}-${max_price:.0f}. "
            f"{len(weekday_options)} weekday options, {len(red_eye_options)} red-eye options available."
        )
    else:
        summary = "No flight options found for specified dates."
    
    return {
        "origin": origin,
        "destination": destination,
        "options": options[:10],
        "summary": summary,
    }


def search_hotels_tool(
    destination: str,
    check_in_date: str,
    check_out_date: str,
    preferred_brands: Optional[list[str]] = None,
) -> dict:
    """
    Search for hotel options at a destination.
    
    Evaluates lodging options considering:
    - Nightly rates against user budget preferences
    - Brand loyalty (preferred brands highlighted)
    - Anomalous pricing (e.g., storm discounts) explicitly flagged
    
    Args:
        destination: Destination city or location
        check_in_date: Check-in date YYYY-MM-DD
        check_out_date: Check-out date YYYY-MM-DD
        preferred_brands: List of preferred hotel brands
        
    Returns:
        Dictionary with hotel options and summary
    """
    if preferred_brands is None:
        preferred_brands = []
    
    check_in = date.fromisoformat(check_in_date)
    check_out = date.fromisoformat(check_out_date)
    nights = (check_out - check_in).days
    
    if nights <= 0:
        return {
            "destination": destination,
            "options": [],
            "summary": "Invalid date range.",
        }
    
    brands = ["Marriott", "Hilton", "Hyatt", "Westin", "Four Seasons", "Budget Inn"]
    options = []
    
    for i, brand in enumerate(brands):
        base_rate = 120.0 + (i * 40.0)
        is_preferred = brand in preferred_brands
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
        
        options.append({
            "check_in_date": check_in.isoformat(),
            "check_out_date": check_out.isoformat(),
            "nightly_rate_usd": nightly_rate,
            "total_price_usd": total_price,
            "brand": brand,
            "name": f"{brand} {destination}",
            "rating": rating,
            "is_anomalous_pricing": is_anomalous,
            "anomalous_reason": anomalous_reason,
            "booking_code": f"HTL-{check_in.isoformat()}-{brand}-{i}",
        })
    
    options.sort(key=lambda x: x["nightly_rate_usd"])
    
    if options:
        min_rate = min(o["nightly_rate_usd"] for o in options)
        max_rate = max(o["nightly_rate_usd"] for o in options)
        preferred_matches = [o for o in options if o["brand"] in preferred_brands]
        anomalous = [o for o in options if o["is_anomalous_pricing"]]
        
        summary = f"Found {len(options)} hotel options. Nightly rate range: ${min_rate:.0f}-${max_rate:.0f}. "
        if preferred_matches:
            summary += f"{len(preferred_matches)} options match preferred brands. "
        if anomalous:
            summary += f"{len(anomalous)} option(s) with anomalous pricing detected."
    else:
        summary = "No hotel options found for specified dates."
    
    return {
        "destination": destination,
        "options": options,
        "summary": summary,
    }


# Create function tools for the agent
get_user_profile_fn = FunctionTool(get_user_profile_tool)
get_weather_forecast_fn = FunctionTool(get_weather_forecast_tool)
search_flights_fn = FunctionTool(search_flights_tool)
search_hotels_fn = FunctionTool(search_hotels_tool)


# Create the root agent
root_agent = Agent(
    model=os.getenv("GOOGLE_API_MODEL", "gemini-2.0-flash-exp"),
    name="travel_coordinator",
    description=(
        "A travel recommendation coordinator that reasons about travel queries, "
        "retrieves user profiles, and consults weather, flight, and hotel data "
        "to provide personalized recommendations."
    ),
    instruction="""
You are a travel recommendation coordinator agent. Your role is to help users decide
when and how to travel to destinations.

CRITICAL WORKFLOW - You MUST follow these stages:

Stage 1: Epistemic Reflection
When a user asks about travel (e.g., "Is it a good time to go to Maui?"), you MUST
first recognize that the question is underspecified. Do NOT answer immediately.
Missing dimensions include:
- User preferences (temperature, budget, comfort level)
- Travel constraints (flexibility, trip duration)
- Safety considerations
- Brand preferences

You MUST decide to retrieve the user profile BEFORE consulting external data sources.
This decision itself is part of what is being evaluated.

Stage 2: User Profile Retrieval
Call get_user_profile_tool with a user_id (you may use "user_123" or "default").
The profile contains:
- Preferred temperature range
- Airfare budget (soft and hard ceilings)
- Hotel budget range
- Brand preferences (e.g., Marriott loyalty)
- Trip length
- Safety and comfort preferences

You MUST condition all subsequent reasoning on this profile.

Stage 3: Weather Analysis
Call get_weather_forecast_tool for the destination with a forward-looking forecast (30 days).
The tool provides summarized data, not raw dumps:
- Storm periods are explicitly flagged
- Temperature ranges are provided
- Brief condition summaries per period

You MUST reason about weather relative to user preferences from the profile.
Consider: Does the temperature match? Are there storms that concern a safety-conscious user?

Stage 4: Flight Search
Call search_flights_tool with origin, destination, and date ranges.
Consider:
- Multiple candidate itineraries
- Compare prices against user affordability thresholds (soft and hard budgets)
- Exploit schedule flexibility (weekday, red-eye, etc.)
- You must be able to say not only which options are good, but why others were rejected

Stage 5: Hotel Evaluation
Call search_hotels_tool with destination and date ranges.
Consider:
- Nightly rates against user budget preferences
- Brand loyalty (preferred brands from profile)
- Anomalous pricing (e.g., storm discounts) - these must be surfaced
- Recognize trade-offs between price, comfort, and environmental risk

Stage 6: Synthesis and Recommendation
Produce a final, user-facing recommendation that is:
- Personalized (based on the user profile)
- Nuanced (acknowledges trade-offs)
- Explicitly reasoned (explains why)
- Written in clear, human language

Your recommendation must include:
- A recommended time window (start and end dates)
- 1-2 alternative options with brief explanations
- A short explanation of why this recommendation fits the user
- A brief "why not" explanation for rejected periods

CONTEXT BUDGET DISCIPLINE:
- Do not dump raw tool outputs into your reasoning
- Summarize and extract only what's needed
- Each tool returns only fields required for reasoning
- Use the summaries provided by tools, not raw data

Remember: You are coordinating reasoning and tool use. The tools provide abstractions,
not databases. Use them thoughtfully to build a comprehensive recommendation.
""",
    tools=[
        get_user_profile_fn,
        get_weather_forecast_fn,
        search_flights_fn,
        search_hotels_fn,
    ],
)
