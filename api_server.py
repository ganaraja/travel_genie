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
    
    # Step 2: Extract destination from query (enhanced parsing)
    destination = "Maui"  # Default
    destination_country = "USA"
    airport_code = "OGG"
    
    # Destination mapping: city -> (display_name, country, airport_code)
    destinations = {
        "paris": ("Paris", "France", "CDG"),
        "tokyo": ("Tokyo", "Japan", "NRT"),
        "bali": ("Bali", "Indonesia", "DPS"),
        "hawaii": ("Maui", "USA", "OGG"),
        "maui": ("Maui", "USA", "OGG"),
        # India - Major Cities
        "bangalore": ("Bangalore", "India", "BLR"),
        "bengaluru": ("Bangalore", "India", "BLR"),
        "mumbai": ("Mumbai", "India", "BOM"),
        "bombay": ("Mumbai", "India", "BOM"),
        "delhi": ("Delhi", "India", "DEL"),
        "new delhi": ("Delhi", "India", "DEL"),
        "hyderabad": ("Hyderabad", "India", "HYD"),
        "chennai": ("Chennai", "India", "MAA"),
        "madras": ("Chennai", "India", "MAA"),
        "kolkata": ("Kolkata", "India", "CCU"),
        "calcutta": ("Kolkata", "India", "CCU"),
        "pune": ("Pune", "India", "PNQ"),
        "ahmedabad": ("Ahmedabad", "India", "AMD"),
        "jaipur": ("Jaipur", "India", "JAI"),
        "goa": ("Goa", "India", "GOI"),
        "kochi": ("Kochi", "India", "COK"),
        "cochin": ("Kochi", "India", "COK"),
        "trivandrum": ("Trivandrum", "India", "TRV"),
        "thiruvananthapuram": ("Trivandrum", "India", "TRV"),
        "chandigarh": ("Chandigarh", "India", "IXC"),
        "lucknow": ("Lucknow", "India", "LKO"),
        "indore": ("Indore", "India", "IDR"),
        "bhubaneswar": ("Bhubaneswar", "India", "BBI"),
        "coimbatore": ("Coimbatore", "India", "CJB"),
        "visakhapatnam": ("Visakhapatnam", "India", "VTZ"),
        "vizag": ("Visakhapatnam", "India", "VTZ"),
        "nagpur": ("Nagpur", "India", "NAG"),
        "surat": ("Surat", "India", "STV"),
        "vadodara": ("Vadodara", "India", "BDQ"),
        "baroda": ("Vadodara", "India", "BDQ"),
        "amritsar": ("Amritsar", "India", "ATQ"),
        "varanasi": ("Varanasi", "India", "VNS"),
        "banaras": ("Varanasi", "India", "VNS"),
        "agra": ("Agra", "India", "AGR"),
        "udaipur": ("Udaipur", "India", "UDR"),
        "jodhpur": ("Jodhpur", "India", "JDH"),
        "mangalore": ("Mangalore", "India", "IXE"),
        "mangaluru": ("Mangalore", "India", "IXE"),
        # Other destinations
        "london": ("London", "UK", "LHR"),
        "new york": ("New York", "USA", "JFK"),
        "nyc": ("New York", "USA", "JFK"),
        "los angeles": ("Los Angeles", "USA", "LAX"),
        "la": ("Los Angeles", "USA", "LAX"),
        "san francisco": ("San Francisco", "USA", "SFO"),
        "sf": ("San Francisco", "USA", "SFO"),
        "dubai": ("Dubai", "UAE", "DXB"),
        "singapore": ("Singapore", "Singapore", "SIN"),
        "hong kong": ("Hong Kong", "Hong Kong", "HKG"),
        "sydney": ("Sydney", "Australia", "SYD"),
        "melbourne": ("Melbourne", "Australia", "MEL"),
        "bangkok": ("Bangkok", "Thailand", "BKK"),
        "shanghai": ("Shanghai", "China", "PVG"),
        "beijing": ("Beijing", "China", "PEK"),
        "seoul": ("Seoul", "South Korea", "ICN"),
        "rome": ("Rome", "Italy", "FCO"),
        "barcelona": ("Barcelona", "Spain", "BCN"),
        "amsterdam": ("Amsterdam", "Netherlands", "AMS"),
        "berlin": ("Berlin", "Germany", "BER"),
        "zurich": ("Zurich", "Switzerland", "ZRH"),
        "vienna": ("Vienna", "Austria", "VIE"),
        "prague": ("Prague", "Czech Republic", "PRG"),
        "istanbul": ("Istanbul", "Turkey", "IST"),
        "cairo": ("Cairo", "Egypt", "CAI"),
        "cape town": ("Cape Town", "South Africa", "CPT"),
        "rio": ("Rio de Janeiro", "Brazil", "GIG"),
        "rio de janeiro": ("Rio de Janeiro", "Brazil", "GIG"),
        "buenos aires": ("Buenos Aires", "Argentina", "EZE"),
        "mexico city": ("Mexico City", "Mexico", "MEX"),
        "cancun": ("Cancun", "Mexico", "CUN"),
        "toronto": ("Toronto", "Canada", "YYZ"),
        "vancouver": ("Vancouver", "Canada", "YVR"),
        "montreal": ("Montreal", "Canada", "YUL"),
    }
    
    # Search for destination in query
    query_lower = query.lower()
    for key, (city, country, airport) in destinations.items():
        if key in query_lower:
            destination = city
            destination_country = country
            airport_code = airport
            break
    
    # Step 3: Check visa requirements BEFORE searching flights
    # IMPORTANT: Visa depends on citizenship, not booking location!
    visa_info = check_visa_requirements(destination_country, profile['citizenship'])
    
    # If visa is required, provide guidance
    if visa_info['required']:
        visa_type = visa_info.get('type', 'visa')
        
        if visa_type == "visa_on_arrival":
            # Visa on arrival is easy - just inform
            visa_note = f"""✅ Visa available on arrival at {destination}
Type: Visa on Arrival
Cost: {visa_info['cost']}
Max stay: {visa_info.get('max_stay', 'Varies')}

You can obtain this visa when you arrive at the airport. Make sure to have:
• Valid passport (6+ months validity)
• Return ticket
• Proof of accommodation
• Cash for visa fee

"""
        elif visa_type == "e-visa":
            # E-visa requires advance application but is easier
            visa_note = f"""⚠️ E-Visa required for {destination}
Type: Electronic Visa (e-Visa)
Processing time: {visa_info['processing_time']}
Cost: {visa_info['cost']}

You must apply online BEFORE booking flights. Allow {visa_info['processing_time']} for processing.

"""
        elif visa_type == "esta":
            # ESTA for USA
            visa_note = f"""✅ ESTA required for {destination}
Type: Electronic System for Travel Authorization
Processing time: {visa_info['processing_time']}
Cost: {visa_info['cost']}
Max stay: {visa_info.get('max_stay', '90 days')}

Apply online at least 72 hours before travel.

"""
        else:
            # Full visa required - stop here
            return f"""⚠️ IMPORTANT: Visa Required for {destination}

Before I search for flights and hotels, I need to inform you that as a {profile['citizenship']} citizen, you need a visa to enter {destination_country}.

📋 VISA INFORMATION
Your citizenship: {profile['citizenship']}
Destination: {destination_country}
Visa type: {visa_type.replace('_', ' ').title()}
Processing time: {visa_info['processing_time']}
Cost: {visa_info['cost']}
{f"Maximum stay: {visa_info.get('max_stay')}" if 'max_stay' in visa_info else ''}

❌ I recommend obtaining your visa BEFORE booking flights to avoid:
• Non-refundable flight costs if visa is denied
• Rush fees for expedited processing
• Stress and uncertainty

NEXT STEPS:
1. Apply for {destination_country} visa (allow {visa_info['processing_time']})
2. Once approved, ask me again: "I have my visa, when should I go to {destination}?"
3. Or ask: "Where can I travel without a visa?"

💡 TIP: Some countries offer e-visas or visa-on-arrival which are faster!

Would you like me to suggest visa-free destinations instead?
"""
    else:
        # No visa required or visa-free
        visa_type = visa_info.get('type', 'visa_free')
        if visa_type == "domestic":
            visa_note = f"""✅ No visa required (domestic travel within {destination_country})

"""
        elif visa_type == "visa_waiver":
            visa_note = f"""✅ Visa-free travel to {destination}
As a {profile['citizenship']} citizen, you can visit {destination_country} without a visa.
Maximum stay: {visa_info.get('max_stay', 'Check immigration rules')}

"""
        else:
            visa_note = f"""✅ No visa required for {destination}
As a {profile['citizenship']} citizen, you can visit {destination_country} visa-free.
{f"Maximum stay: {visa_info.get('max_stay')}" if 'max_stay' in visa_info else ''}

"""
    
    # Step 4: Get weather forecast
    weather = get_weather_forecast_tool(destination)
    
    # Step 5: Search flights (assuming SFO origin)
    today = date.today()
    dep_date = (today + timedelta(days=14)).isoformat()
    ret_date = (today + timedelta(days=21)).isoformat()
    
    flights = search_flights_tool(
        origin="SFO",
        destination=airport_code,
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
        query, destination, profile, weather, flights, hotels, visa_note
    )
    
    return recommendation


def check_visa_requirements(destination_country, citizenship):
    """
    Check if visa is required based on citizenship and destination.
    This is the CORRECT way - visa depends on passport/citizenship, not booking location.
    
    Args:
        destination_country: Country being visited
        citizenship: Traveler's citizenship/passport country
        
    Returns:
        Dictionary with visa requirements
    """
    # Visa requirements matrix: {(citizenship, destination): requirements}
    # Format: (from_country, to_country): {required, processing_time, cost, type}
    
    visa_matrix = {
        # USA citizens traveling to:
        ("USA", "USA"): {"required": False, "type": "domestic"},
        ("USA", "France"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Japan"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Indonesia"): {"required": True, "type": "visa_on_arrival", "processing_time": "On arrival", "cost": "$35", "max_stay": "30 days"},
        ("USA", "China"): {"required": True, "type": "visa", "processing_time": "4-10 business days", "cost": "$140"},
        ("USA", "India"): {"required": True, "type": "e-visa", "processing_time": "2-4 business days", "cost": "$25-100"},
        ("USA", "UK"): {"required": False, "type": "visa_waiver", "max_stay": "6 months"},
        ("USA", "UAE"): {"required": False, "type": "visa_free", "max_stay": "90 days"},
        ("USA", "Singapore"): {"required": False, "type": "visa_free", "max_stay": "90 days"},
        ("USA", "Thailand"): {"required": False, "type": "visa_free", "max_stay": "30 days"},
        ("USA", "Australia"): {"required": True, "type": "e-visa", "processing_time": "1-2 business days", "cost": "$20"},
        ("USA", "South Korea"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Hong Kong"): {"required": False, "type": "visa_free", "max_stay": "90 days"},
        ("USA", "Mexico"): {"required": False, "type": "visa_free", "max_stay": "180 days"},
        ("USA", "Canada"): {"required": False, "type": "visa_free", "max_stay": "6 months"},
        ("USA", "Brazil"): {"required": True, "type": "e-visa", "processing_time": "5-10 business days", "cost": "$80"},
        ("USA", "Argentina"): {"required": False, "type": "visa_free", "max_stay": "90 days"},
        ("USA", "Italy"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Spain"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Germany"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Netherlands"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Switzerland"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Austria"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Czech Republic"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("USA", "Turkey"): {"required": True, "type": "e-visa", "processing_time": "Instant", "cost": "$50"},
        ("USA", "Egypt"): {"required": True, "type": "visa_on_arrival", "processing_time": "On arrival", "cost": "$25", "max_stay": "30 days"},
        ("USA", "South Africa"): {"required": False, "type": "visa_free", "max_stay": "90 days"},
        
        # India citizens traveling to:
        ("India", "India"): {"required": False, "type": "domestic"},
        ("India", "USA"): {"required": True, "type": "visa", "processing_time": "3-5 weeks", "cost": "$160"},
        ("India", "France"): {"required": True, "type": "schengen_visa", "processing_time": "15 days", "cost": "€80"},
        ("India", "Japan"): {"required": True, "type": "visa", "processing_time": "5-7 business days", "cost": "$30"},
        ("India", "Indonesia"): {"required": False, "type": "visa_free", "max_stay": "30 days"},
        ("India", "UK"): {"required": True, "type": "visa", "processing_time": "3 weeks", "cost": "£100"},
        ("India", "UAE"): {"required": False, "type": "visa_on_arrival", "processing_time": "On arrival", "cost": "$60", "max_stay": "60 days"},
        ("India", "Singapore"): {"required": True, "type": "e-visa", "processing_time": "1-3 business days", "cost": "$30"},
        ("India", "Thailand"): {"required": False, "type": "visa_on_arrival", "processing_time": "On arrival", "cost": "$35", "max_stay": "15 days"},
        ("India", "Australia"): {"required": True, "type": "e-visa", "processing_time": "1-2 business days", "cost": "$145"},
        
        # UK citizens traveling to:
        ("UK", "USA"): {"required": False, "type": "esta", "processing_time": "72 hours", "cost": "$21", "max_stay": "90 days"},
        ("UK", "France"): {"required": False, "type": "visa_free", "max_stay": "90 days"},
        ("UK", "Japan"): {"required": False, "type": "visa_waiver", "max_stay": "90 days"},
        ("UK", "Indonesia"): {"required": False, "type": "visa_free", "max_stay": "30 days"},
        ("UK", "India"): {"required": True, "type": "e-visa", "processing_time": "2-4 business days", "cost": "$25-100"},
        ("UK", "Australia"): {"required": True, "type": "e-visa", "processing_time": "1-2 business days", "cost": "$20"},
    }
    
    # Get visa requirement
    key = (citizenship, destination_country)
    visa_req = visa_matrix.get(key)
    
    if not visa_req:
        # Default: assume visa required if not in matrix
        return {
            "required": True,
            "type": "visa",
            "processing_time": "Unknown - please check embassy",
            "cost": "Varies",
            "country": destination_country,
            "citizenship": citizenship,
            "note": "Visa requirements not in database. Please verify with embassy."
        }
    
    return {
        "required": visa_req["required"],
        "type": visa_req.get("type", "visa"),
        "processing_time": visa_req.get("processing_time", "N/A"),
        "cost": visa_req.get("cost", "$0"),
        "max_stay": visa_req.get("max_stay", "Varies"),
        "country": destination_country,
        "citizenship": citizenship
    }


def synthesize_recommendation(query, destination, profile, weather, flights, hotels, visa_note):
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
    
    if flight_options:
        flight_analysis += f"Price range: ${min(f['price_usd'] for f in flight_options):.0f} - ${max(f['price_usd'] for f in flight_options):.0f}\n"
        flight_analysis += f"Within soft budget (${ profile['airfare_budget_soft']:.0f}): {len(affordable_flights)} options\n"
        
        # Always show top 3 flight options
        flight_analysis += f"\n📋 Top 3 Flight Options:\n"
        for i, flight in enumerate(flight_options[:3], 1):
            within_budget = "✓ Within budget" if flight['price_usd'] <= profile['airfare_budget_soft'] else "⚠️ Over soft budget"
            flight_analysis += f"\n{i}. {flight['airline']} - ${flight['price_usd']:.0f} {within_budget}\n"
            flight_analysis += f"   Departure: {flight['departure_date']} at {flight['departure_time']}\n"
            flight_analysis += f"   Return: {flight['return_date']} at {flight['return_time']}\n"
            flight_analysis += f"   Duration: {flight['total_duration_hours']:.1f}h, Layovers: {flight['layovers']}\n"
    else:
        flight_analysis += "No flight options available for the specified dates.\n"
    
    # Analyze hotels
    hotel_options = hotels['options']
    affordable_hotels = [h for h in hotel_options if h['nightly_rate_usd'] >= profile['hotel_budget_min'] and h['nightly_rate_usd'] <= profile['hotel_budget_max']]
    preferred_hotels = [h for h in affordable_hotels if h['brand'] in profile['preferred_brands']]
    anomalous_hotels = [h for h in hotel_options if h['is_anomalous_pricing']]
    
    hotel_analysis = f"\n🏨 HOTEL OPTIONS ({len(hotel_options)} found)\n"
    
    if hotel_options:
        hotel_analysis += f"Nightly rate range: ${min(h['nightly_rate_usd'] for h in hotel_options):.0f} - ${max(h['nightly_rate_usd'] for h in hotel_options):.0f}\n"
        hotel_analysis += f"Within your budget: {len(affordable_hotels)} options\n"
        hotel_analysis += f"Preferred brands available: {len(preferred_hotels)} options\n"
        
        # Always show top 3 hotel options
        hotel_analysis += f"\n📋 Top 3 Hotel Options:\n"
        for i, hotel in enumerate(hotel_options[:3], 1):
            within_budget = "✓ Within budget" if profile['hotel_budget_min'] <= hotel['nightly_rate_usd'] <= profile['hotel_budget_max'] else "⚠️ Outside budget"
            preferred = "⭐ Preferred brand" if hotel['brand'] in profile['preferred_brands'] else ""
            special = f"💰 {hotel['anomalous_reason']}" if hotel['is_anomalous_pricing'] else ""
            
            hotel_analysis += f"\n{i}. {hotel['name']} - ${hotel['nightly_rate_usd']:.0f}/night {within_budget} {preferred}\n"
            hotel_analysis += f"   Rating: {hotel['rating']:.1f}/5.0\n"
            hotel_analysis += f"   Total for {profile['typical_trip_length_days']} nights: ${hotel['total_price_usd']:.0f}\n"
            if special:
                hotel_analysis += f"   {special}\n"
    else:
        hotel_analysis += "No hotel options available for the specified dates.\n"
    
    # Build recommendation with visa info first
    recommendation = f"""Based on your travel preferences and current conditions, here's my analysis for {destination}:

👤 YOUR PROFILE
Citizenship: {profile.get('citizenship', 'USA')}
Temperature preference: {temp_min}°F - {temp_max}°F
Flight budget: ${profile['airfare_budget_soft']:.0f} (soft) / ${profile['airfare_budget_hard']:.0f} (hard)
Hotel budget: ${profile['hotel_budget_min']:.0f} - ${profile['hotel_budget_max']:.0f}/night
Preferred brands: {', '.join(profile['preferred_brands']) if profile['preferred_brands'] else 'None'}
Safety conscious: {'Yes' if profile['safety_conscious'] else 'No'}
Flexibility: ±{profile['flexibility_days']} days

🛂 VISA & ENTRY REQUIREMENTS
{visa_note}

🌤️ WEATHER ANALYSIS
{weather_analysis}

{flight_analysis}

{hotel_analysis}

✨ RECOMMENDED TRAVEL WINDOW
"""
    
    # Use the best available option (first in sorted list)
    if flight_options and hotel_options:
        best_flight = flight_options[0]
        best_hotel = hotel_options[0]
        
        # Check if they're within budget
        flight_in_budget = best_flight['price_usd'] <= profile['airfare_budget_soft']
        hotel_in_budget = profile['hotel_budget_min'] <= best_hotel['nightly_rate_usd'] <= profile['hotel_budget_max']
        
        recommendation += f"""
Dates: {best_flight['departure_date']} to {best_flight['return_date']}

💡 Best Available Option:
• Flight: {best_flight['airline']} - ${best_flight['price_usd']:.0f} {'(within your budget ✓)' if flight_in_budget else '(over your soft budget)'}
• Hotel: {best_hotel['name']} - ${best_hotel['nightly_rate_usd']:.0f}/night {'(within your budget ✓)' if hotel_in_budget else '(outside your budget range)'}
• Total estimated cost: ${best_flight['price_usd'] + best_hotel['total_price_usd']:.0f}

Why this option:
• Weather conditions: {weather['overall_summary'].split('.')[0]}
• Flight duration: {best_flight['total_duration_hours']:.1f} hours with {best_flight['layovers']} layover(s)
• Hotel rating: {best_hotel['rating']:.1f}/5.0
"""
        
        if storm_periods and profile['safety_conscious']:
            recommendation += f"\n⚠️ Note: As a safety-conscious traveler, I recommend avoiding {storm_periods[0]['start_date']} to {storm_periods[0]['end_date']} due to storm risk.\n"
        
        # Budget recommendations
        if not flight_in_budget or not hotel_in_budget:
            recommendation += f"\n💰 Budget Considerations:\n"
            if not flight_in_budget:
                recommendation += f"• Flights are ${best_flight['price_usd'] - profile['airfare_budget_soft']:.0f} over your soft budget\n"
                if affordable_flights:
                    recommendation += f"• {len(affordable_flights)} cheaper flight option(s) available\n"
            if not hotel_in_budget:
                if best_hotel['nightly_rate_usd'] < profile['hotel_budget_min']:
                    recommendation += f"• This hotel is below your minimum budget (great value!)\n"
                else:
                    recommendation += f"• Hotel is ${best_hotel['nightly_rate_usd'] - profile['hotel_budget_max']:.0f}/night over your budget\n"
                if affordable_hotels:
                    recommendation += f"• {len(affordable_hotels)} hotel(s) within your budget available\n"
    
    else:
        recommendation += "\nBased on current availability, I recommend adjusting your dates or budget for better options.\n"
    
    # Add alternatives if available - format like Top 3 options
    if len(flight_options) > 1 and len(hotel_options) > 1:
        alt_flight = flight_options[1]
        alt_hotel = hotel_options[1]
        
        recommendation += f"""
🔄 ALTERNATIVE OPTION

📋 Alternative Flight:

1. {alt_flight['airline']} - ${alt_flight['price_usd']:.0f} {'✓ Within budget' if alt_flight['price_usd'] <= profile['airfare_budget_soft'] else '⚠️ Over soft budget'}
   Departure: {alt_flight['departure_date']} at {alt_flight['departure_time']}
   Return: {alt_flight['return_date']} at {alt_flight['return_time']}
   Duration: {alt_flight['total_duration_hours']:.1f}h, Layovers: {alt_flight['layovers']}
   Reason: {'Red-eye flight for lower price' if alt_flight['is_red_eye'] else 'Different dates for flexibility'}

📋 Alternative Hotel:

1. {alt_hotel['name']} - ${alt_hotel['nightly_rate_usd']:.0f}/night {'✓ Within budget' if profile['hotel_budget_min'] <= alt_hotel['nightly_rate_usd'] <= profile['hotel_budget_max'] else '⚠️ Outside budget'} {'⭐ Preferred brand' if alt_hotel['brand'] in profile['preferred_brands'] else ''}
   Rating: {alt_hotel['rating']:.1f}/5.0
   Total for {profile['typical_trip_length_days']} nights: ${alt_hotel['total_price_usd']:.0f}
"""
        if alt_hotel['is_anomalous_pricing']:
            recommendation += f"   💰 {alt_hotel['anomalous_reason']}\n"
    
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
