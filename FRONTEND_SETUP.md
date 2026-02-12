# Travel Genie Frontend Setup

## Overview

Modern, Expedia-like UI for the Travel Genie AI travel recommendation system.

## Features

- 🎨 Modern gradient design with smooth animations
- 📱 Fully responsive (mobile, tablet, desktop)
- ✨ Real-time AI recommendations
- 🌤️ Weather analysis visualization
- ✈️ Flight and hotel information display
- 👤 User profile selection
- 💡 Example queries for quick start
- 📋 Copy and share recommendations

## Architecture

```
Frontend (React) → API Server (Flask) → Agent (Google ADK) → Tools (FastMCP)
     :3000              :5000              Python              Mock Data
```

## Quick Start

### Option 1: Automated Startup (Recommended)

```bash
./start_travel_genie.sh
```

This will:

1. Install all dependencies
2. Start the API server on port 5000
3. Start the frontend on port 3000
4. Open http://localhost:3000 in your browser

### Option 2: Manual Startup

#### Terminal 1 - Start API Server

```bash
uv pip install -r requirements.txt
uv run python api_server.py
```

#### Terminal 2 - Start Frontend

```bash
cd frontend
npm install
npm start
```

## API Endpoints

### POST /api/recommend

Get travel recommendation from AI agent

```json
{
  "query": "Is it a good time to go to Maui?",
  "userId": "user_123"
}
```

Response:

```json
{
  "success": true,
  "query": "Is it a good time to go to Maui?",
  "userId": "user_123",
  "recommendation": "Based on your preferences...",
  "timestamp": "2026-02-12T12:00:00Z"
}
```

### GET /api/user-profile/:userId

Get user profile information

```json
{
  "userId": "user_123",
  "preferredTempRange": [75, 85],
  "airfareBudgetSoft": 600,
  "airfareBudgetHard": 900,
  ...
}
```

### GET /api/health

Health check endpoint

```json
{
  "status": "healthy",
  "service": "Travel Genie API"
}
```

## User Profiles

### Comfort Traveler (user_123)

- Temperature: 75-85°F
- Flight budget: $600-900
- Hotel budget: $150-300/night
- Preferred brands: Marriott, Hilton
- Safety-conscious: Yes
- Flexibility: 5 days

### Standard Traveler (default)

- Temperature: 70-80°F
- Flight budget: $500-800
- Hotel budget: $100-250/night
- Preferred brands: None
- Safety-conscious: No
- Flexibility: 3 days

## UI Components

### TravelQueryForm

- User profile selector
- Query textarea with examples
- Submit button with loading state
- Example query buttons

### RecommendationDisplay

- Formatted recommendation text
- Copy to clipboard
- Share functionality
- New search button

### LoadingSpinner

- Animated spinner
- Progress steps visualization
- Loading messages

### ErrorMessage

- Error display with icon
- Retry functionality
- Refresh option

## Styling

The UI uses:

- Gradient backgrounds (purple/blue theme)
- Smooth animations and transitions
- Card-based layout
- Responsive grid system
- Modern typography
- Accessibility-friendly colors

## Development

### Run Tests

```bash
cd frontend
npm test
```

### Build for Production

```bash
cd frontend
npm run build
```

### Environment Variables

Create `frontend/.env`:

```
REACT_APP_API_URL=http://localhost:5000
```

## Troubleshooting

### API Connection Error

- Ensure API server is running on port 5000
- Check `api_server.py` logs for errors
- Verify GOOGLE_API_KEY in `.env`

### Frontend Won't Start

- Delete `node_modules` and run `npm install`
- Clear npm cache: `npm cache clean --force`
- Check Node.js version (requires 14+)

### Agent Errors

- Verify agent loads: `uv run python -c "from agent import root_agent; print(root_agent.name)"`
- Check tool functions work: `uv run python verify_system.py`
- Review agent logs in terminal

## Next Steps

1. Test the UI with different queries
2. Customize user profiles in `tools/user_profile.py`
3. Enhance recommendation formatting
4. Add more visualizations (charts, maps)
5. Implement booking integration
6. Add user authentication
7. Deploy to production

## Production Deployment

For production:

1. Build frontend: `cd frontend && npm run build`
2. Serve static files with nginx or similar
3. Run API server with gunicorn: `gunicorn -w 4 api_server:app`
4. Use environment variables for configuration
5. Enable HTTPS
6. Add rate limiting and authentication
