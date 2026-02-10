"""Unified FastMCP server combining all travel tools."""

from fastmcp import FastMCP

# Create unified MCP server
mcp = FastMCP("Travel Genie")

# Import and register all tools
# Each module's mcp instance will be registered with the main server
from .user_profile import get_user_profile
from .weather import get_weather_forecast
from .flights import search_flights
from .hotels import search_hotels

# Register tools from each module
mcp.tool()(get_user_profile)
mcp.tool()(get_weather_forecast)
mcp.tool()(search_flights)
mcp.tool()(search_hotels)


if __name__ == "__main__":
    mcp.run()
