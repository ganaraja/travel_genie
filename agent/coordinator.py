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
    # For now, we'll use a mock implementation
    from tools.user_profile import get_user_profile, GetUserProfileRequest
    
    request = GetUserProfileRequest(user_id=user_id)
    response = get_user_profile(request)
    
    return {
        "user_id": response.user_id,
        "preferred_temp_range": response.preferred_temp_range,
        "airfare_budget_soft": response.airfare_budget_soft,
        "airfare_budget_hard": response.airfare_budget_hard,
        "hotel_budget_min": response.hotel_budget_min,
        "hotel_budget_max": response.hotel_budget_max,
        "preferred_brands": response.preferred_brands,
        "typical_trip_length_days": response.typical_trip_length_days,
        "comfort_level": response.comfort_level,
        "flexibility_days": response.flexibility_days,
        "safety_conscious": response.safety_conscious,
        "visa_required": response.visa_required,
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
    from tools.weather import get_weather_forecast, GetWeatherForecastRequest
    
    if start_date is None:
        start_date = date.today().isoformat()
    
    request = GetWeatherForecastRequest(
        destination=destination,
        start_date=start_date,
        days_ahead=min(days_ahead, 30),
    )
    response = get_weather_forecast(request)
    
    return {
        "destination": response.destination,
        "overall_summary": response.overall_summary,
        "periods": [
            {
                "start_date": p.start_date,
                "end_date": p.end_date,
                "avg_temp_f": p.avg_temp_f,
                "storm_risk": p.storm_risk,
                "storm_severity": p.storm_severity,
                "conditions_summary": p.conditions_summary,
            }
            for p in response.periods
        ],
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
    from tools.flights import search_flights, SearchFlightsRequest
    
    request = SearchFlightsRequest(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        return_date=return_date,
        flexibility_days=flexibility_days,
    )
    response = search_flights(request)
    
    return {
        "origin": response.origin,
        "destination": response.destination,
        "options": [
            {
                "departure_date": opt.departure_date,
                "return_date": opt.return_date,
                "price_usd": opt.price_usd,
                "airline": opt.airline,
                "departure_time": opt.departure_time,
                "return_time": opt.return_time,
                "is_red_eye": opt.is_red_eye,
                "is_weekday": opt.is_weekday,
                "layovers": opt.layovers,
                "total_duration_hours": opt.total_duration_hours,
                "booking_code": opt.booking_code,
            }
            for opt in response.options
        ],
        "summary": response.summary,
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
    from tools.hotels import search_hotels, SearchHotelsRequest
    
    request = SearchHotelsRequest(
        destination=destination,
        check_in_date=check_in_date,
        check_out_date=check_out_date,
        preferred_brands=preferred_brands or [],
    )
    response = search_hotels(request)
    
    return {
        "destination": response.destination,
        "options": [
            {
                "check_in_date": opt.check_in_date,
                "check_out_date": opt.check_out_date,
                "nightly_rate_usd": opt.nightly_rate_usd,
                "total_price_usd": opt.total_price_usd,
                "brand": opt.brand,
                "name": opt.name,
                "rating": opt.rating,
                "is_anomalous_pricing": opt.is_anomalous_pricing,
                "anomalous_reason": opt.anomalous_reason,
                "booking_code": opt.booking_code,
            }
            for opt in response.options
        ],
        "summary": response.summary,
    }


# Create function tools for the agent
get_user_profile_fn = FunctionTool.from_function(get_user_profile_tool)
get_weather_forecast_fn = FunctionTool.from_function(get_weather_forecast_tool)
search_flights_fn = FunctionTool.from_function(search_flights_tool)
search_hotels_fn = FunctionTool.from_function(search_hotels_tool)


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
