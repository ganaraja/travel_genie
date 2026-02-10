"""Analysis logic for weather, flights, and hotels - pure business logic."""

from datetime import date, timedelta
from typing import List, Tuple, Optional

from .models import (
    UserProfile,
    WeatherForecast,
    WeatherPeriod,
    FlightOption,
    HotelOption,
    TemperaturePreference,
)


def analyze_weather_for_user(
    forecast: WeatherForecast, profile: UserProfile
) -> List[Tuple[WeatherPeriod, float, str]]:
    """
    Analyze weather periods against user preferences.
    
    Returns: List of (period, score, reasoning) tuples.
    Score is 0-1, where 1 is perfect match.
    """
    results = []
    
    for period in forecast.forecast_periods:
        score = 1.0
        reasons = []
        
        # Temperature matching
        avg_temp = period.avg_temp_f
        min_pref, max_pref = profile.preferred_temp_range
        
        if min_pref <= avg_temp <= max_pref:
            temp_score = 1.0
            reasons.append(f"Temperature {avg_temp:.0f}°F matches preference")
        elif avg_temp < min_pref:
            temp_score = max(0.0, 1.0 - (min_pref - avg_temp) / 20.0)
            reasons.append(f"Temperature {avg_temp:.0f}°F is {min_pref - avg_temp:.0f}°F below preference")
        else:
            temp_score = max(0.0, 1.0 - (avg_temp - max_pref) / 20.0)
            reasons.append(f"Temperature {avg_temp:.0f}°F is {avg_temp - max_pref:.0f}°F above preference")
        
        score *= temp_score
        
        # Storm risk penalty
        if period.storm_risk:
            if profile.safety_conscious:
                score *= 0.2  # Heavy penalty for safety-conscious users
                reasons.append(f"Storm risk ({period.storm_severity}) - major concern")
            else:
                score *= 0.6  # Moderate penalty
                reasons.append(f"Storm risk ({period.storm_severity}) - moderate concern")
        
        # Precipitation penalty
        if period.precipitation_inches > 2.0:
            score *= 0.7
            reasons.append(f"High precipitation ({period.precipitation_inches:.1f}\")")
        
        results.append((period, score, "; ".join(reasons)))
    
    return results


def filter_flights_by_budget(
    flights: List[FlightOption], profile: UserProfile
) -> Tuple[List[FlightOption], List[FlightOption]]:
    """
    Separate flights into affordable vs. over-budget.
    
    Returns: (affordable_flights, rejected_flights)
    """
    affordable = []
    rejected = []
    
    for flight in flights:
        if flight.price_usd <= profile.airfare_budget_hard:
            affordable.append(flight)
        else:
            rejected.append(flight)
    
    return affordable, rejected


def score_flight_option(flight: FlightOption, profile: UserProfile) -> Tuple[float, str]:
    """
    Score a flight option based on user preferences.
    
    Returns: (score 0-1, reasoning)
    """
    score = 1.0
    reasons = []
    
    # Price scoring (within budget)
    if flight.price_usd <= profile.airfare_budget_soft:
        price_score = 1.0
        reasons.append("Price within preferred budget")
    else:
        # Linear penalty between soft and hard budget
        overage = flight.price_usd - profile.airfare_budget_soft
        max_overage = profile.airfare_budget_hard - profile.airfare_budget_soft
        price_score = max(0.5, 1.0 - (overage / max_overage) * 0.5)
        reasons.append(f"Price ${flight.price_usd:.0f} exceeds preferred budget by ${overage:.0f}")
    
    score *= price_score
    
    # Schedule preferences
    if flight.is_weekday:
        score *= 1.1  # Slight bonus for weekday (usually cheaper)
        reasons.append("Weekday departure")
    
    if flight.is_red_eye:
        score *= 0.9  # Slight penalty for red-eye
        reasons.append("Red-eye flight")
    
    # Layover penalty
    if flight.layovers > 0:
        score *= (1.0 - flight.layovers * 0.1)
        reasons.append(f"{flight.layovers} layover(s)")
    
    return min(1.0, score), "; ".join(reasons)


def filter_hotels_by_budget(
    hotels: List[HotelOption], profile: UserProfile
) -> Tuple[List[HotelOption], List[HotelOption]]:
    """
    Separate hotels into affordable vs. over-budget.
    
    Returns: (affordable_hotels, rejected_hotels)
    """
    affordable = []
    rejected = []
    
    for hotel in hotels:
        if profile.hotel_budget_min <= hotel.nightly_rate_usd <= profile.hotel_budget_max:
            affordable.append(hotel)
        else:
            rejected.append(hotel)
    
    return affordable, rejected


def score_hotel_option(hotel: HotelOption, profile: UserProfile) -> Tuple[float, str]:
    """
    Score a hotel option based on user preferences.
    
    Returns: (score 0-1, reasoning)
    """
    score = 1.0
    reasons = []
    
    # Brand loyalty bonus
    if hotel.brand in profile.preferred_brands:
        score *= 1.2
        reasons.append(f"{hotel.brand} brand matches preference")
    
    # Price scoring (within budget range)
    budget_mid = (profile.hotel_budget_min + profile.hotel_budget_max) / 2
    if hotel.nightly_rate_usd <= budget_mid:
        price_score = 1.0
        reasons.append("Price within budget")
    else:
        overage = hotel.nightly_rate_usd - budget_mid
        max_overage = profile.hotel_budget_max - budget_mid
        price_score = max(0.6, 1.0 - (overage / max_overage) * 0.4)
        reasons.append(f"Price ${hotel.nightly_rate_usd:.0f} exceeds mid-budget")
    
    score *= price_score
    
    # Anomalous pricing (could be good or bad)
    if hotel.is_anomalous_pricing:
        if "discount" in hotel.anomalous_reason.lower():
            score *= 1.1
            reasons.append(f"Anomalous pricing: {hotel.anomalous_reason}")
        else:
            score *= 0.9
            reasons.append(f"Anomalous pricing: {hotel.anomalous_reason}")
    
    # Comfort level matching
    if profile.comfort_level.value == "luxury" and hotel.rating < 4.5:
        score *= 0.8
        reasons.append("Rating below luxury expectation")
    elif profile.comfort_level.value == "budget" and hotel.rating > 4.0:
        score *= 0.9  # Slight penalty for over-quality
        reasons.append("Rating exceeds budget expectation")
    
    return min(1.0, score), "; ".join(reasons)


def find_overlapping_periods(
    weather_periods: List[WeatherPeriod],
    flight_dates: Tuple[date, date],
    hotel_dates: Tuple[date, date],
) -> Optional[Tuple[date, date]]:
    """
    Find overlapping date range for weather, flight, and hotel availability.
    
    Returns: (start_date, end_date) if overlap exists, None otherwise
    """
    flight_start, flight_end = flight_dates
    hotel_start, hotel_end = hotel_dates
    
    # Find intersection of flight and hotel dates
    overlap_start = max(flight_start, hotel_start)
    overlap_end = min(flight_end, hotel_end)
    
    if overlap_start > overlap_end:
        return None
    
    # Check if any weather period covers this overlap
    for period in weather_periods:
        if period.start_date <= overlap_start and overlap_end <= period.end_date:
            return (overlap_start, overlap_end)
    
    return None
