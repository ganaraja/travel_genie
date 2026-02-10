"""Scoring and recommendation synthesis logic - pure business logic."""

from datetime import date, timedelta
from typing import List, Tuple

from .models import (
    UserProfile,
    WeatherForecast,
    FlightOption,
    HotelOption,
    Recommendation,
    RecommendationReason,
)
from .analysis import (
    analyze_weather_for_user,
    filter_flights_by_budget,
    score_flight_option,
    filter_hotels_by_budget,
    score_hotel_option,
    find_overlapping_periods,
)


def synthesize_recommendation(
    profile: UserProfile,
    forecast: WeatherForecast,
    flights: List[FlightOption],
    hotels: List[HotelOption],
) -> Recommendation:
    """
    Synthesize a final recommendation from all inputs.
    
    This is the core business logic that combines weather, flight, and hotel
    analysis into a personalized recommendation.
    """
    # Analyze weather
    weather_scores = analyze_weather_for_user(forecast, profile)
    
    # Filter and score flights
    affordable_flights, rejected_flights = filter_flights_by_budget(flights, profile)
    flight_scores = [
        (flight, *score_flight_option(flight, profile))
        for flight in affordable_flights
    ]
    
    # Filter and score hotels
    affordable_hotels, rejected_hotels = filter_hotels_by_budget(hotels, profile)
    hotel_scores = [
        (hotel, *score_hotel_option(hotel, profile))
        for hotel in affordable_hotels
    ]
    
    # Find best combinations
    best_options = []
    rejected_periods = []
    
    # Try combinations of flights and hotels
    for flight, flight_score, flight_reason in flight_scores[:5]:  # Top 5 flights
        for hotel, hotel_score, hotel_reason in hotel_scores[:5]:  # Top 5 hotels
            # Check date overlap
            overlap = find_overlapping_periods(
                forecast.forecast_periods,
                (flight.departure_date, flight.return_date),
                (hotel.check_in_date, hotel.check_out_date),
            )
            
            if not overlap:
                continue
            
            start_date, end_date = overlap
            
            # Find matching weather period
            weather_score = 0.0
            weather_reason = ""
            for period, score, reason in weather_scores:
                if period.start_date <= start_date <= period.end_date:
                    weather_score = score
                    weather_reason = reason
                    break
            
            # Combined score (weighted)
            combined_score = (
                weather_score * 0.4 +  # Weather is important
                flight_score * 0.3 +   # Flight convenience
                hotel_score * 0.3      # Hotel quality
            )
            
            if combined_score > 0.6:  # Threshold for recommendation
                best_options.append({
                    "start": start_date,
                    "end": end_date,
                    "score": combined_score,
                    "flight": flight,
                    "hotel": hotel,
                    "weather_score": weather_score,
                    "weather_reason": weather_reason,
                    "flight_reason": flight_reason,
                    "hotel_reason": hotel_reason,
                })
            else:
                rejected_periods.append({
                    "start": start_date,
                    "end": end_date,
                    "reason": f"Low combined score ({combined_score:.2f}): weather={weather_score:.2f}, flight={flight_score:.2f}, hotel={hotel_score:.2f}",
                })
    
    # Sort by score
    best_options.sort(key=lambda x: x["score"], reverse=True)
    
    if not best_options:
        # No good options found
        return Recommendation(
            recommended_start=date.today() + timedelta(days=30),
            recommended_end=date.today() + timedelta(days=37),
            primary_reasoning=[
                RecommendationReason(
                    factor="availability",
                    assessment="No suitable combinations found matching all criteria",
                    positive=False,
                )
            ],
            alternative_options=[],
            rejected_periods=[
                (r["start"], r["end"], r["reason"])
                for r in rejected_periods[:3]
            ],
            personalized_summary="Unable to find a suitable travel window that meets all your preferences. Consider adjusting dates or budget constraints.",
        )
    
    # Best option
    best = best_options[0]
    
    # Build reasoning
    reasoning = [
        RecommendationReason(
            factor="weather",
            assessment=best["weather_reason"],
            positive=best["weather_score"] > 0.7,
        ),
        RecommendationReason(
            factor="flight",
            assessment=best["flight_reason"],
            positive=True,
        ),
        RecommendationReason(
            factor="hotel",
            assessment=best["hotel_reason"],
            positive=True,
        ),
    ]
    
    # Alternatives (next 2 best)
    alternatives = []
    for opt in best_options[1:3]:
        alternatives.append((
            opt["start"],
            opt["end"],
            f"Score {opt['score']:.2f}: {opt['weather_reason'][:50]}",
        ))
    
    # Build personalized summary
    summary_parts = [
        f"Based on your preferences (temperature {profile.preferred_temp_range[0]:.0f}-{profile.preferred_temp_range[1]:.0f}°F, "
        f"budget ${profile.airfare_budget_soft:.0f}-${profile.airfare_budget_hard:.0f} for flights), "
        f"I recommend traveling from {best['start']} to {best['end']}."
    ]
    
    summary_parts.append(f"Weather: {best['weather_reason']}")
    summary_parts.append(f"Flight: {best['flight_reason']}")
    summary_parts.append(f"Hotel: {best['hotel_reason']}")
    
    if alternatives:
        summary_parts.append(
            f"Alternative options available on {alternatives[0][0]} or {alternatives[1][0] if len(alternatives) > 1 else alternatives[0][0]}."
        )
    
    return Recommendation(
        recommended_start=best["start"],
        recommended_end=best["end"],
        primary_reasoning=reasoning,
        alternative_options=alternatives,
        rejected_periods=[
            (r["start"], r["end"], r["reason"])
            for r in rejected_periods[:3]
        ],
        personalized_summary=" ".join(summary_parts),
    )
