#!/usr/bin/env python3
"""Test Bangalore query handling."""

from api_server import get_travel_recommendation

def test_bangalore_query():
    """Test that Bangalore queries are handled correctly."""
    print("Testing: 'When should I visit Bangalore?'")
    print("=" * 70)
    
    result = get_travel_recommendation('When should I visit Bangalore?', 'default')
    
    # Check that result contains expected information
    assert 'Bangalore' in result, "Result should mention Bangalore"
    assert 'visa' in result.lower() or 'e-visa' in result.lower(), "Result should mention visa requirements"
    assert 'USA' in result, "Result should mention user citizenship"
    assert 'weather' in result.lower(), "Result should include weather information"
    assert 'flight' in result.lower(), "Result should include flight information"
    assert 'hotel' in result.lower(), "Result should include hotel information"
    
    print(result)
    print("\n" + "=" * 70)
    print("✅ Test passed! Bangalore query is handled correctly.")
    print("\nKey features verified:")
    print("  ✓ Destination: Bangalore")
    print("  ✓ Visa requirements: E-visa for USA citizens")
    print("  ✓ Weather forecast included")
    print("  ✓ Flight options included")
    print("  ✓ Hotel options included")
    print("  ✓ User profile (citizenship) included")

if __name__ == "__main__":
    test_bangalore_query()
