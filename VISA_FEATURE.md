# 🛂 Visa Requirement Checking Feature

## Overview

Travel Genie now checks visa requirements BEFORE searching for flights, ensuring users don't waste time looking at travel options they can't actually book.

## How It Works

### 1. Epistemic Reflection

When you ask about a destination, the system:

1. Gets your user profile
2. **Checks visa requirements for the destination country**
3. Only proceeds to search flights/hotels if visa is not required OR you have the visa

### 2. Early Warning System

If a visa is required and you don't have it, the system:

- **Stops immediately** before searching flights
- Explains why a visa is needed
- Provides visa information (processing time, cost)
- Suggests next steps
- Offers to suggest visa-free alternatives

## Example Conversations

### Scenario 1: Visa Required (Tokyo/Japan)

**You**: "Should I go to Tokyo?"

**Travel Genie**:

```
⚠️ IMPORTANT: Visa Required for Tokyo

Before I search for flights and hotels, I need to inform you
that travel to Japan requires a visa.

📋 VISA INFORMATION
Status: Required
Processing time: 5-10 business days
Estimated cost: $30-60
User profile indicates: Visa NOT obtained

❌ I cannot recommend booking flights until you have obtained
the necessary visa.

NEXT STEPS:
1. Apply for Japan visa (allow 5-10 business days)
2. Once approved, ask me again and I'll find the best travel options
3. Or ask about visa-free destinations: "Where can I travel without a visa?"

Would you like me to suggest alternative destinations that don't
require a visa?
```

### Scenario 2: No Visa Required (Maui/USA)

**You**: "Should I go to Maui?"

**Travel Genie**:

```
Based on your travel preferences and current conditions,
here's my analysis for Maui:

👤 YOUR PROFILE
Temperature preference: 75°F - 85°F
Flight budget: $600 (soft) / $900 (hard)
...

🛂 VISA REQUIREMENTS
Status: ✅ No visa required for USA

🌤️ WEATHER ANALYSIS
...

✈️ FLIGHT OPTIONS
...

🏨 HOTEL OPTIONS
...
```

### Scenario 3: Visa Required But User Has It

If your profile indicates you have the visa:

```
🛂 VISA REQUIREMENTS
Status: ✅ Required for Japan
Your status: ✅ Visa obtained
Processing time: 5-10 business days
Cost: $30-60

[Continues with flight and hotel search...]
```

## Supported Countries

### Visa Required

- **Japan**: 5-10 business days, $30-60
- **Indonesia** (Bali): 3-7 business days, $35
- **China**: 4-10 business days, $140
- **India**: 2-4 business days (e-Visa), $25-100

### No Visa Required

- **USA** (Hawaii, etc.): No visa needed
- **France** (Paris): No visa (Schengen)

## User Profile Integration

The system checks the `visa_required` field in your user profile:

```python
# In tools/user_profile.py
UserProfile(
    user_id="user_123",
    ...
    visa_required=False,  # ← This field
)
```

To indicate you have a visa for a destination, set this to `True`.

## Frontend Display

The visa information appears in the chat as:

1. **Warning Message** (if visa required and not obtained):
   - Red/orange highlighted box
   - Clear warning icon ⚠️
   - Actionable next steps

2. **Info Section** (in full recommendations):
   - 🛂 Visa Requirements section
   - Status indicator (✅ or ⚠️)
   - Processing time and cost
   - Your current status

## Benefits

### For Users

- **No wasted time** searching for flights you can't book
- **Clear guidance** on visa requirements
- **Realistic planning** with visa processing time
- **Cost transparency** including visa fees

### For Travel Planning

- **Proper sequence**: Visa → Flights → Hotels
- **Realistic timelines**: Account for visa processing
- **Budget accuracy**: Include visa costs in total
- **Compliance**: Ensure legal travel requirements met

## API Integration

### Request

```json
POST /api/recommend
{
  "query": "Should I go to Tokyo?",
  "userId": "user_123"
}
```

### Response (Visa Required)

```json
{
  "success": true,
  "query": "Should I go to Tokyo?",
  "userId": "user_123",
  "recommendation": "⚠️ IMPORTANT: Visa Required...",
  "timestamp": null
}
```

## Customization

### Add More Countries

Edit `api_server.py`:

```python
def check_visa_requirements(country, profile):
    visa_requirements = {
        "USA": {"required": False, ...},
        "Japan": {"required": True, ...},
        # Add your country here:
        "Brazil": {
            "required": True,
            "processing_time": "10-15 business days",
            "cost": "$160"
        },
    }
```

### Update User Visa Status

Edit `tools/user_profile.py`:

```python
_MOCK_PROFILES = {
    "user_123": UserProfile(
        ...
        visa_required=True,  # User has visa
    )
}
```

## Testing

### Test Visa Required

```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I go to Tokyo?", "userId": "user_123"}'
```

### Test No Visa Required

```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I go to Maui?", "userId": "user_123"}'
```

### Run Test Script

```bash
# Start API server first
uv run python api_server.py

# In another terminal
uv run python test_visa_api.py
```

## Future Enhancements

1. **Real Visa API Integration**
   - Connect to actual visa requirement databases
   - Real-time visa status checking
   - Country-specific requirements

2. **Visa Application Assistance**
   - Links to visa application portals
   - Required documents checklist
   - Appointment booking

3. **Multi-Country Trips**
   - Check visa for each country in itinerary
   - Transit visa requirements
   - Schengen area handling

4. **Visa Expiry Tracking**
   - Store visa expiry dates
   - Renewal reminders
   - Multiple visa management

5. **Passport Validity**
   - Check 6-month validity rule
   - Passport expiry warnings
   - Renewal recommendations

## Why This Matters

### Real-World Scenario

Without visa checking:

1. User asks about Tokyo
2. System shows great flights for $500
3. User gets excited and tries to book
4. **Realizes they need a visa** (5-10 days processing)
5. Flights are now sold out or more expensive
6. User is frustrated

With visa checking:

1. User asks about Tokyo
2. System immediately says "You need a visa first"
3. User applies for visa (5-10 days)
4. User asks again after visa approval
5. System finds available flights
6. User books with confidence

## Compliance

This feature helps ensure:

- **Legal compliance**: Users don't attempt illegal entry
- **Realistic planning**: Account for all requirements
- **Better experience**: No surprises at the airport
- **Cost accuracy**: Include all travel costs

## Summary

The visa checking feature demonstrates **epistemic reflection** - the system recognizes what information is needed (visa status) before proceeding with recommendations. This prevents wasted effort and ensures realistic, actionable travel plans.

🛂 Visa checking is now a core part of the Travel Genie workflow!
