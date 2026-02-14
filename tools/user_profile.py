"""FastMCP tool for retrieving user profiles."""

from fastmcp import FastMCP
from pydantic import BaseModel, Field

from core.models import UserProfile, ComfortLevel

mcp = FastMCP("Travel Genie Tools")


class GetUserProfileRequest(BaseModel):
    """Request to get user profile."""
    user_id: str = Field(..., description="Unique identifier for the user")


class UserProfileResponse(BaseModel):
    """User profile response - summarized for agent reasoning."""
    user_id: str
    citizenship: str = Field(..., description="Country of citizenship (e.g., 'USA', 'India', 'UK')")
    passport_country: str = Field(..., description="Passport issuing country")
    preferred_temp_range: tuple[float, float] = Field(..., description="(min, max) temperature in Fahrenheit")
    airfare_budget_soft: float = Field(..., description="Preferred maximum airfare in USD")
    airfare_budget_hard: float = Field(..., description="Absolute maximum airfare in USD")
    hotel_budget_min: float = Field(..., description="Minimum nightly hotel rate in USD")
    hotel_budget_max: float = Field(..., description="Maximum nightly hotel rate in USD")
    preferred_brands: list[str] = Field(..., description="Preferred hotel brands")
    typical_trip_length_days: int = Field(..., description="Typical trip duration in days")
    comfort_level: str = Field(..., description="Comfort level: budget, standard, comfort, or luxury")
    flexibility_days: int = Field(..., description="How many days +/- user can shift travel dates")
    safety_conscious: bool = Field(..., description="Whether user prioritizes safety over other factors")


# Mock user profile storage (in production, this would query a database)
_MOCK_PROFILES = {
    "user_123": UserProfile(
        user_id="user_123",
        citizenship="USA",
        passport_country="USA",
        preferred_temp_range=(75.0, 85.0),
        airfare_budget_soft=600.0,
        airfare_budget_hard=900.0,
        hotel_budget_min=150.0,
        hotel_budget_max=300.0,
        preferred_brands=["Marriott", "Hilton"],
        typical_trip_length_days=7,
        comfort_level=ComfortLevel.COMFORT,
        flexibility_days=5,
        safety_conscious=True,
        visa_required=False,
    ),
    "default": UserProfile(
        user_id="default",
        citizenship="USA",
        passport_country="USA",
        preferred_temp_range=(70.0, 80.0),
        airfare_budget_soft=500.0,
        airfare_budget_hard=800.0,
        hotel_budget_min=100.0,
        hotel_budget_max=250.0,
        preferred_brands=[],
        typical_trip_length_days=5,
        comfort_level=ComfortLevel.STANDARD,
        flexibility_days=3,
        safety_conscious=False,
        visa_required=False,
    ),
}


@mcp.tool()
def get_user_profile(request: GetUserProfileRequest) -> UserProfileResponse:
    """
    Retrieve user profile with travel preferences and constraints.
    
    This tool must be called before consulting external data sources.
    The profile contains structured fields needed for personalized recommendations:
    - Citizenship and passport information (for visa requirements)
    - Temperature preferences
    - Budget constraints (soft and hard ceilings)
    - Hotel preferences and brand loyalty
    - Trip duration and flexibility
    - Safety and comfort preferences
    
    Returns only the fields required for reasoning - no extraneous data.
    """
    profile = _MOCK_PROFILES.get(request.user_id, _MOCK_PROFILES["default"])
    
    return UserProfileResponse(
        user_id=profile.user_id,
        citizenship=profile.citizenship,
        passport_country=profile.passport_country,
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
    )


if __name__ == "__main__":
    mcp.run()
