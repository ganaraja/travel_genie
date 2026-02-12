# 🌴 Run Travel Genie - Complete Guide

## What You'll Get

A beautiful, modern travel website (like Expedia) powered by AI that gives personalized travel recommendations.

## Quick Start (3 Steps)

### Step 1: Start the API Server

Open a terminal and run:

```bash
uv run python api_server.py
```

You should see:

```
Starting Travel Genie API server on port 5000...
Frontend should connect to: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

✅ Keep this terminal open!

### Step 2: Start the Frontend

Open a NEW terminal and run:

```bash
cd frontend
npm install  # Only needed first time
npm start
```

You should see:

```
Compiled successfully!
You can now view travel-genie-frontend in the browser.
  Local:            http://localhost:3000
```

✅ Your browser should automatically open to http://localhost:3000

### Step 3: Use Travel Genie!

1. Select a traveler profile (Comfort or Standard)
2. Type your travel question or click an example
3. Click "Get Travel Recommendation"
4. Wait 10-30 seconds for AI analysis
5. Get your personalized recommendation!

## Example Questions to Try

- "Is it a good time to go to Maui?"
- "When should I visit Paris?"
- "Best time to travel to Tokyo from San Francisco?"
- "Should I go to Bali next month?"
- "Is Hawaii good in March?"
- "When's the best time for a beach vacation?"

## What the AI Analyzes

1. **Your Profile** 👤
   - Temperature preferences
   - Budget constraints
   - Hotel brand preferences
   - Safety concerns
   - Travel flexibility

2. **Weather** 🌤️
   - 30-day forecast
   - Storm tracking
   - Temperature matching
   - Seasonal patterns

3. **Flights** ✈️
   - Price ranges
   - Schedule options
   - Red-eye availability
   - Weekday vs weekend

4. **Hotels** 🏨
   - Nightly rates
   - Brand matches
   - Anomalous pricing
   - Availability

## Troubleshooting

### "Unable to connect to the Travel Genie service"

- Make sure the API server is running (Step 1)
- Check that you see "Running on http://0.0.0.0:5000" in the API terminal
- Try: `curl http://localhost:5000/api/health`

### API Server Won't Start

```bash
# Install dependencies
uv pip install -r requirements.txt

# Check if agent loads
uv run python -c "from agent import root_agent; print('✅ Agent OK')"

# Check if port 5000 is in use
lsof -i :5000
```

### Frontend Won't Start

```bash
cd frontend

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install

# Try again
npm start
```

### "Agent takes too long"

- First query can take 20-30 seconds (AI is thinking!)
- Subsequent queries are usually faster
- Check API terminal for errors
- Verify GOOGLE_API_KEY in `.env` file

## Architecture

```
┌─────────────────┐
│   Browser       │  You interact here
│  localhost:3000 │  Modern UI
└────────┬────────┘
         │
         │ HTTP requests
         ▼
┌─────────────────┐
│  Flask API      │  Handles requests
│  localhost:5000 │  Connects frontend to agent
└────────┬────────┘
         │
         │ Python calls
         ▼
┌─────────────────┐
│  Google ADK     │  AI Agent
│  Agent          │  Orchestrates reasoning
└────────┬────────┘
         │
         │ Tool calls
         ▼
┌─────────────────┐
│  Tools          │  Data sources
│  (Mock Data)    │  Weather, Flights, Hotels
└─────────────────┘
```

## Features

### Modern UI

- ✨ Gradient design with smooth animations
- 📱 Fully responsive (works on phone, tablet, desktop)
- 🎨 Expedia-like professional look
- 💡 Example queries for quick start
- 📋 Copy and share recommendations

### Smart AI

- 🧠 Multi-step reasoning process
- 🎯 Personalized to your preferences
- 📊 Analyzes multiple data sources
- 💬 Natural language understanding
- ⚡ Powered by Google Gemini 2.5

### User Profiles

- **Comfort Traveler**: Higher budget, safety-conscious, prefers 75-85°F
- **Standard Traveler**: Moderate budget, flexible, prefers 70-80°F

## Stopping the Services

### Stop API Server

In the API terminal, press `Ctrl+C`

### Stop Frontend

In the frontend terminal, press `Ctrl+C`

## Next Steps

1. ✅ Try different travel questions
2. ✅ Switch between user profiles
3. ✅ Share recommendations with friends
4. 📝 Customize user profiles in `tools/user_profile.py`
5. 🎨 Modify UI colors in `frontend/src/App.css`
6. 🚀 Deploy to production (see FRONTEND_SETUP.md)

## Production Ready?

For production deployment:

1. Build frontend: `cd frontend && npm run build`
2. Use production server: `gunicorn -w 4 api_server:app`
3. Add authentication and rate limiting
4. Use real APIs instead of mock data
5. Enable HTTPS
6. Add monitoring and logging

## Need Help?

Check these files:

- `FRONTEND_SETUP.md` - Detailed frontend documentation
- `QUICKSTART.md` - System overview
- `AGENT_FIXED.md` - Agent architecture
- `verify_system.py` - System health check

Run verification:

```bash
uv run python verify_system.py
```

## Enjoy! 🎉

You now have a fully functional AI-powered travel recommendation system with a beautiful modern UI!
