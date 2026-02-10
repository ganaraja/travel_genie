"""FastMCP tool for weather forecasts."""

from datetime import date, timedelta
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from core.models import WeatherForecast, WeatherPeriod

mcp = FastMCP("Travel Genie Tools")


class GetWeatherForecastRequest(BaseModel):
    """Request for weather forecast."""
    destination: str = Field(..., description="Destination city or location")
    start_date: str = Field(..., description="Start date in YYYY-MM-DD format")
    days_ahead: int = Field(default=30, description="Number of days to forecast (max 30)")


class WeatherPeriodResponse(BaseModel):
    """Weather period summary."""
    start_date: str = Field(..., description="Start date YYYY-MM-DD")
    end_date: str = Field(..., description="End date YYYY-MM-DD")
    avg_temp_f: float = Field(..., description="Average temperature in Fahrenheit")
    storm_risk: bool = Field(..., description="Whether storm risk exists")
    storm_severity: str | None = Field(None, description="Storm severity if applicable: minor, moderate, severe")
    conditions_summary: str = Field(..., description="Brief summary of conditions")


class WeatherForecastResponse(BaseModel):
    """Weather forecast response - summarized for agent reasoning."""
    destination: str
    overall_summary: str = Field(..., description="High-level summary of forecast period")
    periods: list[WeatherPeriodResponse] = Field(..., description="Weather periods with key conditions")


@mcp.tool()
def get_weather_forecast(request: GetWeatherForecastRequest) -> WeatherForecastResponse:
    """
    Retrieve forward-looking weather forecast for a destination.
    
    This tool provides summarized weather data, not raw dumps. Key features:
    - 30-day forward-looking forecast
    - Storm periods explicitly flagged with severity
    - Temperature ranges and precipitation summaries
    - Brief condition summaries per period
    
    Returns only fields required for reasoning - periods are grouped to avoid
    overwhelming the agent with daily data.
    """
    # Mock weather data (in production, would call weather API)
    start = date.fromisoformat(request.start_date)
    periods = []
    
    # Generate mock periods (grouped by week)
    for week in range(0, min(request.days_ahead, 30), 7):
        period_start = start + timedelta(days=week)
        period_end = min(period_start + timedelta(days=6), start + timedelta(days=request.days_ahead - 1))
        
        # Mock weather patterns
        base_temp = 82.0  # Maui baseline
        temp_variation = (week % 3) * 3.0  # Some variation
        
        # Simulate storm in week 2
        has_storm = week == 7
        storm_severity = "moderate" if has_storm else None
        
        avg_temp = base_temp + temp_variation
        precipitation = 0.5 if has_storm else 0.1
        
        conditions = f"Warm and mostly sunny"
        if has_storm:
            conditions = f"Moderate storm expected with increased precipitation"
        elif avg_temp > 85:
            conditions = f"Hot and sunny"
        
        periods.append(WeatherPeriodResponse(
            start_date=period_start.isoformat(),
            end_date=period_end.isoformat(),
            avg_temp_f=avg_temp,
            storm_risk=has_storm,
            storm_severity=storm_severity,
            conditions_summary=conditions,
        ))
    
    # Build overall summary
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


if __name__ == "__main__":
    mcp.run()
