#!/usr/bin/env python3
"""Test that destinations are correctly reflected in output."""

from api_server import get_travel_recommendation

def test_destination(city, user_id='default'):
    """Test a specific destination."""
    query = f"When should I visit {city}?"
    print(f"\n{'='*70}")
    print(f"Testing: {query}")
    print('='*70)
    
    result = get_travel_recommendation(query, user_id)
    
    # Count occurrences
    city_count = result.count(city)
    maui_count = result.count('Maui')
    
    print(f"\n📊 Destination Verification:")
    print(f"  '{city}' appears: {city_count} times")
    print(f"  'Maui' appears: {maui_count} times")
    
    # Extract key sections
    sections = {
        'Weather': '🌤️ WEATHER ANALYSIS' in result,
        'Flights': '✈️ FLIGHT OPTIONS' in result,
        'Hotels': '🏨 HOTEL OPTIONS' in result,
        'Visa': '🛂 VISA' in result
    }
    
    print(f"\n✅ Sections Present:")
    for section, present in sections.items():
        print(f"  {section}: {'✓' if present else '✗'}")
    
    # Show weather line
    for line in result.split('\n'):
        if 'Weather forecast for' in line or 'Forecast for' in line:
            print(f"\n🌤️  Weather Line: {line.strip()}")
            break
    
    # Show hotel lines
    print(f"\n🏨 Hotel Lines:")
    for line in result.split('\n'):
        if city in line and ('hotel' in line.lower() or any(brand in line for brand in ['Marriott', 'Hilton', 'Hyatt'])):
            print(f"  {line.strip()}")
    
    # Verify correctness
    assert city_count > 0, f"❌ {city} should appear in output"
    assert maui_count == 0 or city == 'Maui', f"❌ Maui should not appear when asking about {city}"
    
    print(f"\n✅ Test PASSED for {city}!")
    return True

if __name__ == "__main__":
    cities = [
        'Bangalore',
        'Mumbai',
        'Delhi',
        'Hyderabad',
        'Goa',
        'Paris',
        'Tokyo'
    ]
    
    print("🧪 Testing Destination-Specific Output")
    print("="*70)
    
    passed = 0
    failed = 0
    
    for city in cities:
        try:
            test_destination(city)
            passed += 1
        except AssertionError as e:
            print(f"\n❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            failed += 1
    
    print(f"\n{'='*70}")
    print(f"📊 Final Results: {passed} passed, {failed} failed out of {len(cities)} tests")
    print('='*70)
    
    if failed == 0:
        print("✅ All tests passed! Destinations are correctly reflected in output.")
    else:
        print(f"⚠️  {failed} test(s) failed. Please check the output above.")
