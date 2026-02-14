# Travel Genie - Destination Support

The system now supports 40+ destinations worldwide with proper visa checking, weather forecasts, flight search, and hotel recommendations.

## Supported Destinations

### North America

- 🇺🇸 **United States**
  - Maui, Hawaii (OGG)
  - New York City (JFK)
  - Los Angeles (LAX)
  - San Francisco (SFO)
- 🇨🇦 **Canada**
  - Toronto (YYZ)
  - Vancouver (YVR)
  - Montreal (YUL)
- 🇲🇽 **Mexico**
  - Mexico City (MEX)
  - Cancun (CUN)

### Europe

- 🇫🇷 **France** - Paris (CDG)
- 🇬🇧 **United Kingdom** - London (LHR)
- 🇮🇹 **Italy** - Rome (FCO)
- 🇪🇸 **Spain** - Barcelona (BCN)
- 🇳🇱 **Netherlands** - Amsterdam (AMS)
- 🇩🇪 **Germany** - Berlin (BER)
- 🇨🇭 **Switzerland** - Zurich (ZRH)
- 🇦🇹 **Austria** - Vienna (VIE)
- 🇨🇿 **Czech Republic** - Prague (PRG)

### Asia

- 🇯🇵 **Japan** - Tokyo (NRT)
- 🇮🇳 **India** (30+ cities)
  - **Major Metro Cities**
    - Bangalore/Bengaluru (BLR)
    - Mumbai/Bombay (BOM)
    - Delhi/New Delhi (DEL)
    - Hyderabad (HYD)
    - Chennai/Madras (MAA)
    - Kolkata/Calcutta (CCU)
    - Pune (PNQ)
    - Ahmedabad (AMD)
  - **Tourist Destinations**
    - Goa (GOI)
    - Jaipur (JAI)
    - Agra (AGR)
    - Udaipur (UDR)
    - Jodhpur (JDH)
    - Varanasi/Banaras (VNS)
    - Amritsar (ATQ)
  - **South India**
    - Kochi/Cochin (COK)
    - Trivandrum/Thiruvananthapuram (TRV)
    - Coimbatore (CJB)
    - Mangalore/Mangaluru (IXE)
  - **Other Cities**
    - Chandigarh (IXC)
    - Lucknow (LKO)
    - Indore (IDR)
    - Bhubaneswar (BBI)
    - Visakhapatnam/Vizag (VTZ)
    - Nagpur (NAG)
    - Surat (STV)
    - Vadodara/Baroda (BDQ)
- 🇨🇳 **China**
  - Shanghai (PVG)
  - Beijing (PEK)
- 🇰🇷 **South Korea** - Seoul (ICN)
- 🇸🇬 **Singapore** - Singapore (SIN)
- 🇭🇰 **Hong Kong** - Hong Kong (HKG)
- 🇹🇭 **Thailand** - Bangkok (BKK)
- 🇮🇩 **Indonesia** - Bali (DPS)
- 🇦🇪 **UAE** - Dubai (DXB)
- 🇹🇷 **Turkey** - Istanbul (IST)

### Oceania

- 🇦🇺 **Australia**
  - Sydney (SYD)
  - Melbourne (MEL)

### South America

- 🇧🇷 **Brazil** - Rio de Janeiro (GIG)
- 🇦🇷 **Argentina** - Buenos Aires (EZE)

### Africa

- 🇪🇬 **Egypt** - Cairo (CAI)
- 🇿🇦 **South Africa** - Cape Town (CPT)

## Visa Requirements Coverage

The system includes comprehensive visa requirements for:

### USA Citizens

- ✅ Domestic travel (no visa)
- ✅ Visa waiver countries (France, Japan, UK, etc.)
- ✅ E-visa countries (India, Australia, Brazil, Turkey)
- ✅ Visa on arrival (Indonesia, Egypt)
- ✅ Full visa required (China)

### India Citizens

- ✅ Domestic travel (no visa)
- ✅ Visa-free destinations (Indonesia)
- ✅ E-visa destinations (Singapore, UAE, Australia)
- ✅ Full visa required (USA, UK, France, Japan)

### UK Citizens

- ✅ ESTA for USA
- ✅ Visa-free EU travel
- ✅ E-visa for India, Australia
- ✅ Visa waiver for Japan

## Example Queries

### India Cities

```
"When should I visit Bangalore?"
"Should I go to Mumbai or Delhi?"
"Best time to visit Goa?"
"When should I visit Jaipur?"
"Is it a good time to go to Hyderabad?"
"Should I visit Chennai or Kolkata?"
"Best time for Agra (Taj Mahal)?"
"When to visit Kerala (Kochi/Trivandrum)?"
```

**Response includes:**

- E-visa requirement for USA citizens ($25-100, 2-4 business days)
- Weather forecast for the specific city
- Flight options from SFO to the city's airport
- Hotel options in that city
- Budget analysis

### Bangalore/India

```
"When should I visit Bangalore?"
"Should I go to Bengaluru next month?"
"Best time to visit Bangalore?"
```

**Response includes:**

- E-visa requirement for USA citizens ($25-100, 2-4 business days)
- Weather forecast for Bangalore
- Flight options from SFO to BLR
- Hotel options in Bangalore
- Budget analysis

### Paris/France

```
"When should I visit Paris?"
"Is Paris a good destination?"
```

**Response includes:**

- Visa waiver (90 days) for USA citizens
- Weather forecast for Paris
- Flight options from SFO to CDG
- Hotel options in Paris

### Tokyo/Japan

```
"Should I go to Tokyo?"
"Best time for Tokyo?"
```

**Response includes:**

- Visa waiver (90 days) for USA citizens
- Weather forecast for Tokyo
- Flight options from SFO to NRT
- Hotel options in Tokyo

## How It Works

### 1. Destination Detection

The system uses keyword matching to detect destinations:

```python
destinations = {
    "bangalore": ("Bangalore", "India", "BLR"),
    "bengaluru": ("Bangalore", "India", "BLR"),
    "paris": ("Paris", "France", "CDG"),
    # ... 40+ destinations
}
```

### 2. Visa Checking

Based on user citizenship and destination country:

```python
visa_matrix = {
    ("USA", "India"): {
        "required": True,
        "type": "e-visa",
        "processing_time": "2-4 business days",
        "cost": "$25-100"
    },
    # ... comprehensive matrix
}
```

### 3. Flight Search

Uses airport codes for accurate flight search:

```python
flights = search_flights_tool(
    origin="SFO",
    destination="BLR",  # Bangalore airport code
    departure_date=dep_date,
    return_date=ret_date
)
```

### 4. Hotel Search

Searches hotels at the destination:

```python
hotels = search_hotels_tool(
    destination="Bangalore",
    check_in_date=dep_date,
    check_out_date=ret_date
)
```

## Adding New Destinations

To add a new destination, update `api_server.py`:

### 1. Add to destinations dictionary

```python
destinations = {
    # ... existing destinations
    "new_city": ("New City", "Country", "AIRPORT_CODE"),
}
```

### 2. Add visa requirements

```python
visa_matrix = {
    # ... existing requirements
    ("USA", "Country"): {
        "required": True/False,
        "type": "visa/e-visa/visa_on_arrival/visa_free",
        "processing_time": "X days",
        "cost": "$X"
    },
}
```

## Testing

Test any destination with:

```bash
python -c "from api_server import get_travel_recommendation; \
result = get_travel_recommendation('When should I visit CITY?', 'default'); \
print(result[:500])"
```

Example:

```bash
python test_bangalore_query.py
```

## Features

For each destination, the system provides:

1. **Visa Requirements**
   - Type (visa, e-visa, visa on arrival, visa-free)
   - Processing time
   - Cost
   - Maximum stay duration

2. **Weather Forecast**
   - 30-day forward-looking forecast
   - Storm risk detection
   - Temperature ranges
   - Condition summaries

3. **Flight Options**
   - Multiple itineraries
   - Price ranges
   - Weekday vs weekend options
   - Red-eye flights
   - Flexibility considerations

4. **Hotel Options**
   - Multiple hotel brands
   - Nightly rate ranges
   - Brand loyalty matching
   - Anomalous pricing detection (storm discounts)

5. **Personalized Recommendations**
   - Based on user profile (citizenship, budget, preferences)
   - Budget analysis (soft vs hard limits)
   - Safety considerations
   - Alternative options
   - "Why not" explanations

## Limitations

1. **Mock Data**: Currently uses mock data for weather, flights, and hotels
2. **Origin Airport**: Assumes SFO (San Francisco) as origin
3. **Visa Matrix**: Limited to USA, India, and UK citizens
4. **Airport Codes**: Requires manual mapping for new destinations

## Future Enhancements

1. ✅ Support for 40+ destinations
2. ⏳ Real-time weather API integration
3. ⏳ Real-time flight API integration
4. ⏳ Real-time hotel API integration
5. ⏳ Dynamic origin airport selection
6. ⏳ More citizenship options
7. ⏳ Multi-city itineraries
8. ⏳ One-way flights
9. ⏳ Car rental options
10. ⏳ Activity recommendations

## API Endpoints

### Get Recommendation

```http
POST /api/recommend
Content-Type: application/json

{
  "query": "When should I visit Bangalore?",
  "userId": "default"
}
```

**Response:**

```json
{
  "success": true,
  "query": "When should I visit Bangalore?",
  "userId": "default",
  "recommendation": "Based on your travel preferences...",
  "timestamp": "2024-01-15T12:00:00Z"
}
```

## Documentation

- **Main Guide**: `QUICKSTART.md`
- **Testing**: `TESTING_GUIDE.md`, `TESTS_SUMMARY.md`
- **Visa Feature**: `VISA_FEATURE.md`
- **Frontend**: `FRONTEND_SETUP.md`
- **API**: `CHATGPT_INTERFACE.md`
