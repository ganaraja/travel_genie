"""FastMCP tool for hotel search."""

from datetime import date, timedelta
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from core.models import HotelOption

mcp = FastMCP("Travel Genie Tools")


class SearchHotelsRequest(BaseModel):
    """Request for hotel search."""
    destination: str = Field(..., description="Destination city or location")
    check_in_date: str = Field(..., description="Check-in date YYYY-MM-DD")
    check_out_date: str = Field(..., description="Check-out date YYYY-MM-DD")
    preferred_brands: list[str] = Field(default_factory=list, description="Preferred hotel brands")


class HotelOptionResponse(BaseModel):
    """Hotel option summary."""
    check_in_date: str = Field(..., description="Check-in date YYYY-MM-DD")
    check_out_date: str = Field(..., description="Check-out date YYYY-MM-DD")
    nightly_rate_usd: float = Field(..., description="Nightly rate in USD")
    total_price_usd: float = Field(..., description="Total price for stay in USD")
    brand: str = Field(..., description="Hotel brand")
    name: str = Field(..., description="Hotel name")
    rating: float = Field(..., description="Hotel rating 1-5 stars")
    is_anomalous_pricing: bool = Field(..., description="Whether pricing is anomalous")
    anomalous_reason: str | None = Field(None, description="Reason for anomalous pricing")
    booking_code: str = Field(..., description="Unique booking code for idempotency")


class HotelSearchResponse(BaseModel):
    """Hotel search response - summarized for agent reasoning."""
    destination: str
    options: list[HotelOptionResponse] = Field(..., description="Hotel options")
    summary: str = Field(..., description="Brief summary of options and price range")


@mcp.tool()
def search_hotels(request: SearchHotelsRequest) -> HotelSearchResponse:
    """
    Search for hotel options at a destination.
    
    This tool evaluates lodging options considering:
    - Nightly rates against user budget preferences
    - Brand loyalty (preferred brands highlighted)
    - Anomalous pricing (e.g., storm discounts) explicitly flagged
    
    Returns only essential fields - no raw API dumps. Options are pre-filtered
    to reasonable candidates.
    
    Idempotent: same booking_code can be reused safely.
    """
    check_in = date.fromisoformat(request.check_in_date)
    check_out = date.fromisoformat(request.check_out_date)
    nights = (check_out - check_in).days
    
    if nights <= 0:
        return HotelSearchResponse(
            destination=request.destination,
            options=[],
            summary="Invalid date range.",
        )
    
    # Mock hotel options
    brands = ["Marriott", "Hilton", "Hyatt", "Westin", "Four Seasons", "Budget Inn"]
    options = []
    
    # Check for storm period (simplified - in production would check weather)
    # Assume storm around check_in + 7 days if it's a specific date
    has_storm_discount = False  # Simplified
    
    for i, brand in enumerate(brands):
        # Base pricing
        base_rate = 120.0 + (i * 40.0)  # Range from $120 to $360
        
        # Brand preference affects availability/price
        is_preferred = brand in request.preferred_brands
        if is_preferred:
            base_rate *= 0.95  # Slight discount for preferred
        
        # Anomalous pricing check
        is_anomalous = False
        anomalous_reason = None
        
        # Simulate storm discount for some dates
        if i < 2 and check_in.day % 7 == 0:  # Rough heuristic
            is_anomalous = True
            anomalous_reason = "Storm discount - reduced rates due to weather forecast"
            base_rate *= 0.75
        
        # Rating correlates with price tier
        rating = 3.0 + (i * 0.4)
        if rating > 5.0:
            rating = 5.0
        
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
    
    # Sort by nightly rate
    options.sort(key=lambda x: x.nightly_rate_usd)
    
    # Build summary
    if options:
        min_rate = min(o.nightly_rate_usd for o in options)
        max_rate = max(o.nightly_rate_usd for o in options)
        preferred_matches = [o for o in options if o.brand in request.preferred_brands]
        anomalous = [o for o in options if o.is_anomalous_pricing]
        
        summary = (
            f"Found {len(options)} hotel options. Nightly rate range: ${min_rate:.0f}-${max_rate:.0f}. "
        )
        
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
