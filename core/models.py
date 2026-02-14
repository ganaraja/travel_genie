"""Data models for travel recommendations - pure Python dataclasses."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional
from enum import Enum


class TemperaturePreference(Enum):
    """User temperature preferences."""
    COLD = "cold"  # < 60°F
    COOL = "cool"  # 60-70°F
    MILD = "mild"  # 70-80°F
    WARM = "warm"  # 80-90°F
    HOT = "hot"    # > 90°F


class ComfortLevel(Enum):
    """Comfort/safety preference levels."""
    BUDGET = "budget"
    STANDARD = "standard"
    COMFORT = "comfort"
    LUXURY = "luxury"


@dataclass
class UserProfile:
    """User travel preferences and constraints."""
    user_id: str
    citizenship: str = "USA"  # Country of citizenship for visa requirements
    passport_country: str = "USA"  # Passport issuing country
    preferred_temp_range: tuple[float, float] = (70.0, 80.0)  # (min, max) in Fahrenheit
    airfare_budget_soft: float = 500.0  # Preferred max in USD
    airfare_budget_hard: float = 800.0  # Absolute max in USD
    hotel_budget_min: float = 100.0  # Min nightly rate in USD
    hotel_budget_max: float = 250.0  # Max nightly rate in USD
    preferred_brands: List[str] = None  # e.g., ["Marriott", "Hilton"]
    typical_trip_length_days: int = 7
    comfort_level: ComfortLevel = ComfortLevel.STANDARD
    flexibility_days: int = 3  # How many days +/- they can shift
    safety_conscious: bool = False
    visa_required: bool = False  # Legacy field
    notes: Optional[str] = None
    
    def __post_init__(self):
        if self.preferred_brands is None:
            self.preferred_brands = []


@dataclass
class WeatherPeriod:
    """Weather conditions for a specific period."""
    start_date: date
    end_date: date
    avg_temp_f: float
    min_temp_f: float
    max_temp_f: float
    precipitation_inches: float
    storm_risk: bool
    storm_severity: Optional[str] = None  # "minor", "moderate", "severe"
    conditions_summary: str = ""  # Brief text summary


@dataclass
class WeatherForecast:
    """Weather forecast for a destination."""
    destination: str
    forecast_periods: List[WeatherPeriod]
    overall_summary: str  # High-level summary, not raw data dump


@dataclass
class FlightOption:
    """A single flight itinerary option."""
    departure_date: date
    return_date: date
    price_usd: float
    airline: str
    departure_time: str  # e.g., "08:30"
    return_time: str
    is_red_eye: bool
    is_weekday: bool
    layovers: int
    total_duration_hours: float
    booking_code: str  # For idempotency


@dataclass
class HotelOption:
    """A single hotel option."""
    check_in_date: date
    check_out_date: date
    nightly_rate_usd: float
    total_price_usd: float
    brand: str
    name: str
    rating: float  # 1-5 stars
    is_anomalous_pricing: bool  # e.g., storm discount
    anomalous_reason: Optional[str] = None
    booking_code: str = ""  # For idempotency


@dataclass
class RecommendationReason:
    """Reasoning component for a recommendation."""
    factor: str  # e.g., "weather", "price", "availability"
    assessment: str  # Brief explanation
    positive: bool  # Whether this factor supports the recommendation


@dataclass
class Recommendation:
    """Final travel recommendation."""
    recommended_start: date
    recommended_end: date
    primary_reasoning: List[RecommendationReason]
    alternative_options: List[tuple[date, date, str]]  # (start, end, brief reason)
    rejected_periods: List[tuple[date, date, str]]  # (start, end, why rejected)
    personalized_summary: str  # Human-readable explanation
