"""FastMCP tool for flight search."""

from datetime import date, timedelta
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from core.models import FlightOption

mcp = FastMCP("Travel Genie Tools")


class SearchFlightsRequest(BaseModel):
    """Request for flight search."""
    origin: str = Field(..., description="Origin airport code (e.g., SFO)")
    destination: str = Field(..., description="Destination airport code (e.g., OGG for Maui)")
    departure_date: str = Field(..., description="Preferred departure date YYYY-MM-DD")
    return_date: str = Field(..., description="Preferred return date YYYY-MM-DD")
    flexibility_days: int = Field(default=3, description="Days +/- to consider for flexibility")


class FlightOptionResponse(BaseModel):
    """Flight option summary."""
    departure_date: str = Field(..., description="Departure date YYYY-MM-DD")
    return_date: str = Field(..., description="Return date YYYY-MM-DD")
    price_usd: float = Field(..., description="Total price in USD")
    airline: str = Field(..., description="Airline name")
    departure_time: str = Field(..., description="Departure time HH:MM")
    return_time: str = Field(..., description="Return time HH:MM")
    is_red_eye: bool = Field(..., description="Whether departure is red-eye")
    is_weekday: bool = Field(..., description="Whether departure is weekday")
    layovers: int = Field(..., description="Number of layovers")
    total_duration_hours: float = Field(..., description="Total flight duration")
    booking_code: str = Field(..., description="Unique booking code for idempotency")


class FlightSearchResponse(BaseModel):
    """Flight search response - summarized for agent reasoning."""
    origin: str
    destination: str
    options: list[FlightOptionResponse] = Field(..., description="Candidate flight options")
    summary: str = Field(..., description="Brief summary of options and price range")


@mcp.tool()
def search_flights(request: SearchFlightsRequest) -> FlightSearchResponse:
    """
    Search for flight options between origin and destination.
    
    This tool considers schedule flexibility (weekday vs weekend, red-eye options)
    and returns multiple candidate itineraries. Prices are compared against
    user affordability thresholds (handled by agent reasoning).
    
    Returns only essential fields - no raw API dumps. Options are pre-filtered
    to reasonable candidates (not all possible combinations).
    
    Idempotent: same booking_code can be reused safely.
    """
    dep_date = date.fromisoformat(request.departure_date)
    ret_date = date.fromisoformat(request.return_date)
    
    # Generate mock flight options with price variations
    options = []
    
    # Base price varies by day of week
    base_prices = [550, 620, 680, 720, 750, 800, 850]  # Sun-Sat
    
    for day_offset in range(-request.flexibility_days, request.flexibility_days + 1):
        candidate_dep = dep_date + timedelta(days=day_offset)
        candidate_ret = ret_date + timedelta(days=day_offset)
        
        if candidate_dep >= date.today() and candidate_ret > candidate_dep:
            day_of_week = candidate_dep.weekday()
            base_price = base_prices[day_of_week]
            
            # Add some variation
            price = base_price + (day_offset * 20) + (50 if day_of_week >= 5 else 0)
            
            # Generate a few options per date
            for variant in range(2):
                is_red_eye = variant == 1
                is_weekday = day_of_week < 5
                
                # Red-eye is cheaper
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
    
    # Sort by price
    options.sort(key=lambda x: x.price_usd)
    
    # Build summary
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
        options=options[:10],  # Limit to top 10
        summary=summary,
    )


if __name__ == "__main__":
    mcp.run()
