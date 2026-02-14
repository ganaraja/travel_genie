#!/usr/bin/env python3
"""Run all tests for Travel Genie."""

import sys
import subprocess


def run_tests():
    """Run pytest with coverage."""
    print("=" * 70)
    print("Running Travel Genie Test Suite")
    print("=" * 70)
    print()
    
    # Run pytest with coverage
    cmd = [
        "pytest",
        "tests/",
        "-v",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-W", "ignore::DeprecationWarning",
    ]
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print("Error: pytest not found. Install with: uv pip install pytest pytest-cov")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
