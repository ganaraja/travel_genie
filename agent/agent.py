"""Agent definition file for Google ADK."""

import sys
import os

# Add parent directory to path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.coordinator import root_agent

# ADK expects root_agent to be available at module level
__all__ = ["root_agent"]
