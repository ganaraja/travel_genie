"""Standalone agent entry point for Google ADK CLI.

This file exists at the project root to work around ADK CLI's module loading behavior.
When ADK loads 'agent', it will load this file instead of the agent/ package,
allowing proper imports from the agent package.
"""

from agent import root_agent

__all__ = ["root_agent"]
