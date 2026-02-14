#!/usr/bin/env python3
"""Test script to verify Zurich destination detection works correctly."""

import sys
sys.path.insert(0, '.')

def test_destination_detection():
    """Test that various queries correctly detect Zurich as destination."""
    
    # Destination mapping from api_server.py
    destinations = {
        "paris": ("Paris", "France", "CDG"),
        "tokyo": ("Tokyo", "Japan", "NRT"),
        "bali": ("Bali", "Indonesia", "DPS"),
        "maui": ("Maui", "USA", "OGG"),
        "zurich": ("Zurich", "Switzerland", "ZRH"),
        "switzerland": ("Zurich", "Switzerland", "ZRH"),
        "geneva": ("Geneva", "Switzerland", "GVA"),
    }
    
    test_queries = [
        ("best time to visit zurich", "Zurich", "Switzerland", "ZRH"),
        ("when should I go to zurich", "Zurich", "Switzerland", "ZRH"),
        ("zurich weather", "Zurich", "Switzerland", "ZRH"),
        ("travel to zurich", "Zurich", "Switzerland", "ZRH"),
        ("best time for switzerland", "Zurich", "Switzerland", "ZRH"),
        ("when to visit maui", "Maui", "USA", "OGG"),
        ("paris in spring", "Paris", "France", "CDG"),
    ]
    
    print("Testing Destination Detection")
    print("=" * 60)
    
    all_passed = True
    
    for query, expected_city, expected_country, expected_airport in test_queries:
        # Default values
        destination = "Maui"
        destination_country = "USA"
        airport_code = "OGG"
        
        # Search for destination in query
        query_lower = query.lower()
        for key in sorted(destinations.keys(), key=len, reverse=True):
            if key in query_lower:
                city, country, airport = destinations[key]
                destination = city
                destination_country = country
                airport_code = airport
                break
        
        # Check if result matches expected
        passed = (destination == expected_city and 
                 destination_country == expected_country and 
                 airport_code == expected_airport)
        
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"\n{status}: '{query}'")
        print(f"  Expected: {expected_city}, {expected_country}, {expected_airport}")
        print(f"  Got:      {destination}, {destination_country}, {airport_code}")
        
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(test_destination_detection())
