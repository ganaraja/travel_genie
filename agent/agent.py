"""Agent definition file for Google ADK."""

from .coordinator import root_agent

# ADK expects root_agent to be available at module level
__all__ = ["root_agent"]
