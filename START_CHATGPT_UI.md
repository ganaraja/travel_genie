# 🚀 Start Travel Genie ChatGPT Interface

## Quick Start (2 Steps!)

### Step 1: Start the API Server

```bash
uv run python api_server.py
```

Wait for: `Running on http://0.0.0.0:5000`

### Step 2: Start the Frontend

```bash
cd frontend
npm install  # Only first time
npm start
```

Browser opens automatically to http://localhost:3000

## What You'll See

### 🎨 ChatGPT-Style Interface

- Clean, modern chat interface
- Message bubbles (you on right, AI on left)
- Smooth animations
- Auto-scrolling conversation

### 👤 User Profile

- Select traveler type in header
- See your preferences (temperature, budget, etc.)
- Switch profiles anytime

### 💬 Conversation Flow

1. AI greets you
2. You ask a travel question
3. AI analyzes (10-30 seconds)
4. Get detailed recommendation with:
   - Weather analysis 🌤️
   - Flight options ✈️
   - Hotel matches 🏨
   - Personalized reasoning
5. Ask follow-up questions
6. Continue natural conversation

### 💡 Example Questions (Click to Use!)

- "Is it a good time to go to Maui?"
- "When should I visit Paris?"
- "Best time for a beach vacation in Hawaii?"
- "Should I go to Bali next month?"
- "What's the weather like in Tokyo in March?"
- "Find me cheap flights to Europe"

## Features

### ✨ Highlighted Recommendations

- **Blue boxes**: Recommended options
- **Pink boxes**: Alternative options
- **Orange boxes**: Why not (periods to avoid)

### 📊 Info Cards

Weather, flights, and hotels shown in colorful cards with icons

### ⌨️ Smart Input

- Type naturally
- Press `Enter` to send
- `Shift + Enter` for new line
- Auto-resizing textarea

### 🔄 Chat Controls

- **Clear Chat**: Start fresh conversation
- **Profile Selector**: Change traveler type
- **Scroll**: Auto-scrolls to latest message

## Sample Conversation

**You**: Is it a good time to go to Maui?

**Travel Genie**: Let me analyze your Maui trip...

_[Shows detailed analysis with weather, flights, hotels]_

**Recommended**: March 15-22

- Perfect weather (82°F)
- Flights $580 (within budget)
- Marriott $225/night
- No storms

**Alternative**: March 8-15 with storm discount

- Save 25% on hotels
- Moderate storm risk

**Why Not**: March 22-29

- Weekend flights too expensive
- Temperatures too high

**You**: What about the storm discount?

**Travel Genie**: Good question! Here's the trade-off...

_[Explains pros/cons of storm discount option]_

## Tips

1. **Be Specific**: "When should I visit Paris in spring?" vs "Paris?"
2. **Ask Follow-ups**: "What about next month?" "Cheaper options?"
3. **Use Examples**: Click example questions to get started
4. **Switch Profiles**: Try both Comfort and Standard travelers
5. **Clear Chat**: Start fresh if conversation gets long

## Traveler Profiles

### 👤 Comfort Traveler

- Temperature: 75-85°F
- Flights: $600-900
- Hotels: $150-300/night
- Safety-conscious: Yes
- Flexibility: 5 days

### 👤 Standard Traveler

- Temperature: 70-80°F
- Flights: $500-800
- Hotels: $100-250/night
- Safety-conscious: No
- Flexibility: 3 days

## Troubleshooting

### "Unable to connect"

→ Make sure API server is running (Step 1)

### Slow responses

→ First query takes 20-30 seconds (AI thinking!)
→ Subsequent queries are faster

### Frontend won't start

```bash
cd frontend
rm -rf node_modules
npm install
npm start
```

## What Makes This Different?

### vs. Traditional Travel Sites

- ❌ Traditional: Fill forms, filter results, compare manually
- ✅ Travel Genie: Ask naturally, get personalized analysis

### vs. Simple Chatbots

- ❌ Simple bots: Canned responses, no reasoning
- ✅ Travel Genie: Real AI analysis with weather, flights, hotels

### vs. Generic AI

- ❌ Generic AI: General knowledge, no real data
- ✅ Travel Genie: Specialized for travel with mock data sources

## Architecture

```
You type question
    ↓
Frontend (React)
    ↓
API Server (Flask)
    ↓
AI Agent (Google ADK)
    ↓
Tools (Weather, Flights, Hotels)
    ↓
AI synthesizes recommendation
    ↓
You see detailed analysis
```

## Next Steps

1. ✅ Try different questions
2. ✅ Switch between profiles
3. ✅ Ask follow-up questions
4. ✅ Test mobile view (resize browser)
5. 📝 Customize profiles in `tools/user_profile.py`
6. 🎨 Change colors in `frontend/src/App.css`
7. 🚀 Deploy to production

## Need Help?

- Check `CHATGPT_INTERFACE.md` for detailed documentation
- Check `FRONTEND_SETUP.md` for technical details
- Run `uv run python verify_system.py` to check system health
- Check browser console for errors (F12)
- Check API terminal for logs

## Enjoy! 🎉

You now have a fully functional ChatGPT-style AI travel assistant!
