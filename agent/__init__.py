"""Google ADK coordinator agent for travel recommendations."""

import sys
import os

# Ensure parent directory is in path
_parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Now import coordinator
from agent.coordinator import root_agent

__all__ = ["root_agent"]
