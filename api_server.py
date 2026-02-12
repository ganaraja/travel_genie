"""Flask API server to connect frontend to the Travel Genie agent."""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import date, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend


def get_travel_recommendation(query, user_id):
    """
    Generate a travel recommendation by calling tools directly.
    This simulates what the agent would do.
    """
    from tools.user_profile import _MOCK_PROFILES
    from agent.coordinator import (
        get_user_profile_tool,
        get_weather_forecast_tool,
        search_flights_tool,
        search_hotels_tool
    )
    
    # Step 1: Get user profile
    profile = get_user_profile_tool(user_id)
    
    # Step 2: Extract destination from query (simple parsing)
    destination = "Maui"  # Default
    destination_country = "USA"
    if "paris" in query.lower():
        destination = "Paris"
        destination_country = "France"
    elif "tokyo" in query.lower():
        destination = "Tokyo"
        destination_country = "Japan"
    elif "bali" in query.lower():
        destination = "Bali"
        destination_country = "Indonesia"
    elif "hawaii" in query.lower() or "maui" in query.lower():
        destination = "Maui"
        destination_country = "USA"
    
    # Step 3: Check visa requirements BEFORE searching flights
    visa_info = check_visa_requirements(destination_country, profile)
    
    # If visa is required and user doesn't have it, warn early
    if visa_info['required'] and not visa_info['user_has_visa']:
        return f"""⚠️ IMPORTANT: Visa Required for {destination}

Before I search for flights and hotels, I need to inform you that travel to {destination_country} requires a visa.

📋 VISA INFORMATION
Status: Required
Processing time: {visa_info['processing_time']}
Estimated cost: {visa_info['cost']}
User profile indicates: {'Visa obtained' if visa_info['user_has_visa'] else 'Visa NOT obtained'}

❌ I cannot recommend booking flights until you have obtained the necessary visa.

NEXT STEPS:
1. Apply for {destination_country} visa (allow {visa_info['processing_time']})
2. Once approved, ask me again and I'll find the best travel options
3. Or ask about visa-free destinations: "Where can I travel without a visa?"

Would you like me to suggest alternative destinations that don't require a visa?
"""
    
    # Step 4: Get weather forecast
    weather = get_weather_forecast_tool(destination)
    
    # Step 5: Search flights (assuming SFO origin)
    today = date.today()
    dep_date = (today + timedelta(days=14)).isoformat()
    ret_date = (today + timedelta(days=21)).isoformat()
    
    flights = search_flights_tool(
        origin="SFO",
        destination="OGG" if destination == "Maui" else "CDG" if destination == "Paris" else "NRT",
        departure_date=dep_date,
        return_date=ret_date,
        flexibility_days=profile['flexibility_days']
    )
    
    # Step 6: Search hotels
    hotels = search_hotels_tool(
        destination=destination,
        check_in_date=dep_date,
        check_out_date=ret_date,
        preferred_brands=profile['preferred_brands']
    )
    
    # Step 7: Synthesize recommendation (now includes visa info)
    recommendation = synthesize_recommendation(
        query, destination, profile, weather, flights, hotels, visa_info
    )
    
    return recommendation


def check_visa_requirements(country, profile):
    """
    Check if visa is required for the destination country.
    Returns visa information including requirements and user status.
    """
    # Mock visa requirements database
    visa_requirements = {
        "USA": {"required": False, "processing_time": "N/A", "cost": "$0"},
        "France": {"required": False, "processing_time": "N/A", "cost": "$0 (Schengen)"},
        "Japan": {"required": True, "processing_time": "5-10 business days", "cost": "$30-60"},
        "Indonesia": {"required": True, "processing_time": "3-7 business days", "cost": "$35"},
        "China": {"required": True, "processing_time": "4-10 business days", "cost": "$140"},
        "India": {"required": True, "processing_time": "2-4 business days (e-Visa)", "cost": "$25-100"},
    }
    
    visa_req = visa_requirements.get(country, {"required": False, "processing_time": "N/A", "cost": "$0"})
    
    return {
        "required": visa_req["required"],
        "processing_time": visa_req["processing_time"],
        "cost": visa_req["cost"],
        "user_has_visa": profile.get('visa_required', False),  # From user profile
        "country": country
    }


def synthesize_recommendation(query, destination, profile, weather, flights, hotels, visa_info):
    """Synthesize a comprehensive travel recommendation."""
    
    # Analyze weather
    temp_min, temp_max = profile['preferred_temp_range']
    weather_analysis = f"Weather forecast for {destination}: {weather['overall_summary']}\n\n"
    
    storm_periods = [p for p in weather['periods'] if p['storm_risk']]
    if storm_periods:
        weather_analysis += f"⚠️ Storm Alert: {len(storm_periods)} period(s) with storm risk detected.\n"
    
    # Analyze flights
    flight_options = flights['options']
    affordable_flights = [f for f in flight_options if f['price_usd'] <= profile['airfare_budget_soft']]
    budget_flights = [f for f in flight_options if f['price_usd'] <= profile['airfare_budget_hard']]
    
    flight_analysis = f"\n✈️ FLIGHT OPTIONS ({len(flight_options)} found)\n"
    flight_analysis += f"Price range: ${min(f['price_usd'] for f in flight_options):.0f} - ${max(f['price_usd'] for f in flight_options):.0f}\n"
    flight_analysis += f"Within soft budget (${ profile['airfare_budget_soft']:.0f}): {len(affordable_flights)} options\n"
    
    if affordable_flights:
        best_flight = affordable_flights[0]
        flight_analysis += f"\nBest option: {best_flight['airline']} - ${best_flight['price_usd']:.0f}\n"
        flight_analysis += f"  Departure: {best_flight['departure_date']} at {best_flight['departure_time']}\n"
        flight_analysis += f"  Return: {best_flight['return_date']} at {best_flight['return_time']}\n"
    
    # Analyze hotels
    hotel_options = hotels['options']
    affordable_hotels = [h for h in hotel_options if h['nightly_rate_usd'] >= profile['hotel_budget_min'] and h['nightly_rate_usd'] <= profile['hotel_budget_max']]
    preferred_hotels = [h for h in affordable_hotels if h['brand'] in profile['preferred_brands']]
    anomalous_hotels = [h for h in hotel_options if h['is_anomalous_pricing']]
    
    hotel_analysis = f"\n🏨 HOTEL OPTIONS ({len(hotel_options)} found)\n"
    hotel_analysis += f"Nightly rate range: ${min(h['nightly_rate_usd'] for h in hotel_options):.0f} - ${max(h['nightly_rate_usd'] for h in hotel_options):.0f}\n"
    hotel_analysis += f"Within your budget: {len(affordable_hotels)} options\n"
    hotel_analysis += f"Preferred brands available: {len(preferred_hotels)} options\n"
    
    if preferred_hotels:
        best_hotel = preferred_hotels[0]
        hotel_analysis += f"\nBest match: {best_hotel['name']} - ${best_hotel['nightly_rate_usd']:.0f}/night\n"
        hotel_analysis += f"  Rating: {best_hotel['rating']:.1f}/5.0\n"
        hotel_analysis += f"  Total for {profile['typical_trip_length_days']} nights: ${best_hotel['total_price_usd']:.0f}\n"
    
    if anomalous_hotels:
        hotel_analysis += f"\n💰 Special pricing detected: {len(anomalous_hotels)} hotel(s) with discounts\n"
        for h in anomalous_hotels[:2]:
            hotel_analysis += f"  {h['name']}: ${h['nightly_rate_usd']:.0f}/night - {h['anomalous_reason']}\n"
    
    # Build recommendation with visa info first
    recommendation = f"""Based on your travel preferences and current conditions, here's my analysis for {destination}:

👤 YOUR PROFILE
Temperature preference: {temp_min}°F - {temp_max}°F
Flight budget: ${profile['airfare_budget_soft']:.0f} (soft) / ${profile['airfare_budget_hard']:.0f} (hard)
Hotel budget: ${profile['hotel_budget_min']:.0f} - ${profile['hotel_budget_max']:.0f}/night
Preferred brands: {', '.join(profile['preferred_brands']) if profile['preferred_brands'] else 'None'}
Safety conscious: {'Yes' if profile['safety_conscious'] else 'No'}
Flexibility: ±{profile['flexibility_days']} days

"""
    
    # Add visa information section
    if visa_info['required']:
        recommendation += f"""🛂 VISA REQUIREMENTS
Status: ✅ Required for {visa_info['country']}
Your status: {'✅ Visa obtained' if visa_info['user_has_visa'] else '⚠️ Visa NOT obtained'}
Processing time: {visa_info['processing_time']}
Cost: {visa_info['cost']}

"""
        if not visa_info['user_has_visa']:
            recommendation += f"""⚠️ IMPORTANT: You'll need to obtain a visa before booking flights.
Allow {visa_info['processing_time']} for visa processing.

"""
    else:
        recommendation += f"""🛂 VISA REQUIREMENTS
Status: ✅ No visa required for {visa_info['country']}

"""
    
    recommendation += f"""🌤️ WEATHER ANALYSIS
{weather_analysis}

{flight_analysis}

{hotel_analysis}

✨ RECOMMENDED TRAVEL WINDOW
"""
    
    if affordable_flights and preferred_hotels:
        best_flight = affordable_flights[0]
        best_hotel = preferred_hotels[0]
        
        recommendation += f"""
Dates: {best_flight['departure_date']} to {best_flight['return_date']}

Why this works for you:
• Weather conditions align with your temperature preferences
• Flights at ${best_flight['price_usd']:.0f} are within your soft budget
• {best_hotel['brand']} available (your preferred brand) at ${best_hotel['nightly_rate_usd']:.0f}/night
• Total estimated cost: ${best_flight['price_usd'] + best_hotel['total_price_usd']:.0f}
"""
        
        if visa_info['required'] and not visa_info['user_has_visa']:
            recommendation += f"\n⚠️ Remember: Apply for visa first (allow {visa_info['processing_time']})\n"
        
        if storm_periods and profile['safety_conscious']:
            recommendation += f"\n⚠️ Note: As a safety-conscious traveler, I recommend avoiding {storm_periods[0]['start_date']} to {storm_periods[0]['end_date']} due to storm risk.\n"
    
    else:
        recommendation += "\nBased on current availability, I recommend adjusting your dates or budget for better options.\n"
    
    # Add alternatives
    if len(affordable_flights) > 1:
        alt_flight = affordable_flights[1]
        recommendation += f"""
🔄 ALTERNATIVE OPTION
Dates: {alt_flight['departure_date']} to {alt_flight['return_date']}
Flight: ${alt_flight['price_usd']:.0f} ({alt_flight['airline']})
Reason: {'Red-eye flight for lower price' if alt_flight['is_red_eye'] else 'Different dates for flexibility'}
"""
    
    # Add why not section
    expensive_flights = [f for f in flight_options if f['price_usd'] > profile['airfare_budget_hard']]
    if expensive_flights:
        recommendation += f"""
❌ WHY NOT other periods:
• {len(expensive_flights)} flight options exceed your hard budget limit
• Weekend flights tend to be ${(max(f['price_usd'] for f in expensive_flights) - min(f['price_usd'] for f in affordable_flights)):.0f} more expensive
"""
    
    recommendation += "\n\n💬 Feel free to ask follow-up questions like:\n"
    recommendation += "• 'What about next month?'\n"
    recommendation += "• 'Are there cheaper options?'\n"
    recommendation += "• 'What if I'm more flexible on dates?'\n"
    if visa_info['required']:
        recommendation += "• 'How do I apply for the visa?'\n"
        recommendation += "• 'What documents do I need for the visa?'\n"
    
    return recommendation


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "Travel Genie API"})


@app.route('/api/recommend', methods=['POST'])
def get_recommendation():
    """Get travel recommendation from the agent."""
    try:
        data = request.json
        query = data.get('query')
        user_id = data.get('userId', 'default')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Generate recommendation
        recommendation_text = get_travel_recommendation(query, user_id)
        
        return jsonify({
            "success": True,
            "query": query,
            "userId": user_id,
            "recommendation": recommendation_text,
            "timestamp": None
        })
            
    except Exception as e:
        print(f"Error processing recommendation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/user-profile/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    """Get user profile information."""
    try:
        from tools.user_profile import _MOCK_PROFILES
        
        profile = _MOCK_PROFILES.get(user_id, _MOCK_PROFILES.get("default"))
        
        if not profile:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({
            "userId": profile.user_id,
            "preferredTempRange": profile.preferred_temp_range,
            "airfareBudgetSoft": profile.airfare_budget_soft,
            "airfareBudgetHard": profile.airfare_budget_hard,
            "hotelBudgetMin": profile.hotel_budget_min,
            "hotelBudgetMax": profile.hotel_budget_max,
            "preferredBrands": profile.preferred_brands,
            "typicalTripLengthDays": profile.typical_trip_length_days,
            "comfortLevel": profile.comfort_level.value,
            "flexibilityDays": profile.flexibility_days,
            "safetyConscious": profile.safety_conscious,
            "visaRequired": profile.visa_required,
        })
        
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    print(f"Starting Travel Genie API server on port {port}...")
    print(f"Frontend should connect to: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
