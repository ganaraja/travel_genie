#!/usr/bin/env python3
"""Simple wrapper to run the agent with proper imports."""

import sys
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure current directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the agent
from agent.coordinator import root_agent

print("=" * 60)
print("Travel Genie Agent - Interactive Mode")
print("=" * 60)
print(f"\n✅ Agent loaded with {len(root_agent.tools)} tools")
print("\nTo use the full ADK CLI features, the agent needs to be")
print("properly packaged. For now, you can:")
print("\n1. Use the web interface:")
print("   uv run adk web --port 8000")
print("\n2. Test with the test script:")
print("   uv run python test_agent.py")
print("\n3. Or implement the improvements from the spec:")
print("   cat .kiro/specs/travel-genie-improvements/tasks.md")
print("\n" + "=" * 60)
