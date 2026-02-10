# Travel Genie - AI Travel Recommendation System

A sophisticated travel recommendation system built with Google Agent Development Kit (ADK) that orchestrates reasoning, tool use, and personalized recommendations.

## Architecture

This project follows strict separation of concerns:

```
travel_genie/
├── core/           # Pure Python business logic (NO ADK/MCP imports)
│   ├── models.py   # Data models (UserProfile, WeatherForecast, FlightOption, HotelOption, Recommendation)
│   ├── analysis.py # Analysis logic (weather, flight, hotel scoring)
│   └── scoring.py  # Recommendation synthesis logic
├── tools/          # FastMCP wrappers around core functions
│   ├── user_profile.py  # User profile retrieval tool
│   ├── weather.py       # Weather forecast tool
│   ├── flights.py       # Flight search tool
│   ├── hotels.py        # Hotel search tool
│   └── server.py        # Unified MCP server
└── agent/          # Google ADK coordinator
    └── coordinator.py   # Main agent that orchestrates reasoning and tool calls
```

### Architectural Principles

1. **Core Logic Independence**: The `core/` module contains pure Python logic that can be imported in a Python REPL without internet access. It has NO dependencies on Google ADK, MCP, or any orchestration framework.

2. **Tool Abstraction**: The `tools/` module wraps core functions with FastMCP, exposing them as MCP tools. Tools return only essential fields required for reasoning - no raw API dumps.

3. **Agent Orchestration**: The `agent/` module uses Google ADK to coordinate reasoning, decide which tools to call, and synthesize final recommendations.

## Functional Requirements

The system handles the query: **"Is it a good time to go to Maui?"**

### Stage 1: Epistemic Reflection
The agent recognizes the question is underspecified and identifies missing dimensions:
- User preferences (temperature, budget, comfort level)
- Travel constraints (flexibility, trip duration)
- Safety considerations
- Brand preferences

**Critical**: The agent decides to retrieve user profile BEFORE consulting external data sources.

### Stage 2: User Profile Retrieval
- Tool: `get_user_profile`
- Returns structured fields: temperature preferences, budget constraints, brand preferences, trip length, safety preferences
- All subsequent reasoning is conditioned on this profile

### Stage 3: Weather Analysis
- Tool: `get_weather_forecast`
- Provides 30-day forward-looking forecast
- Storm periods explicitly flagged with severity
- Summarized data (not raw dumps)
- Agent reasons about weather relative to user preferences

### Stage 4: Flight Search
- Tool: `search_flights`
- Considers multiple candidate itineraries
- Compares prices against user affordability thresholds
- Exploits schedule flexibility (weekday, red-eye, etc.)
- Agent explains why options are good or rejected

### Stage 5: Hotel Evaluation
- Tool: `search_hotels`
- Checks nightly rates against preferences
- Considers brand loyalty
- Surfaces anomalous pricing (e.g., storm discounts)
- Recognizes trade-offs between price, comfort, and environmental risk

### Stage 6: Synthesis and Recommendation
Final output includes:
- Recommended time window (start and end dates)
- 1-2 alternative options
- Personalized explanation
- "Why not" explanation for rejected periods

## Tooling Requirements

### Technologies
- **Google Agent Development Kit (ADK)**: For agent orchestration
- **FastMCP**: For tool definition and serving
- **External APIs**: Currently mocked (weather, flights, hotels)

### Tool Design Principles

1. **Context Budget Discipline**: No tool returns unbounded text or raw JSON dumps. Each tool:
   - Returns only fields required for reasoning
   - Summarizes when necessary
   - Documents output clearly in docstrings

2. **Idempotency**: Tools that could be retried are idempotent:
   - Booking actions use `booking_code` for idempotency
   - Profile updates are safe to retry
   - Search operations are idempotent

## Setup

### Prerequisites
- Python 3.10 or later
- Google API key for Gemini (get from [Google AI Studio](https://aistudio.google.com/app/apikey))

### Installation

1. Install `uv` (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or using pip: pip install uv
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. Set up environment variables:
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
echo "GOOGLE_API_MODEL=gemini-2.0-flash-exp" >> .env
```

**Note**: `uv` automatically manages virtual environments. You can activate it with `source .venv/bin/activate` after running `uv sync`, or use `uv run` to run commands directly.

## Usage

### Running the Agent

The agent can be run using Google ADK's CLI:

```bash
uv run adk run agent
```

Or using the web interface:

```bash
uv run adk web --port 8000
```

### Running the MCP Server (Optional)

To run the FastMCP server separately:

```bash
uv run python -m tools.server
```

### Running Tests

Run Python tests with pytest:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov
```

### Running the Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Run frontend tests:
```bash
npm test
```

## Example Interaction

**User**: "Is it a good time to go to Maui?"

**Agent Workflow**:
1. Recognizes question is underspecified
2. Calls `get_user_profile_tool(user_id="user_123")`
3. Calls `get_weather_forecast_tool(destination="Maui", days_ahead=30)`
4. Calls `search_flights_tool(origin="SFO", destination="OGG", ...)`
5. Calls `search_hotels_tool(destination="Maui", ...)`
6. Synthesizes recommendation based on user profile and all data

**Output**: Personalized recommendation with:
- Recommended dates: March 15-22, 2026
- Weather: Warm (78-82°F), no storms
- Flight: $620 weekday option available
- Hotel: Marriott at $220/night (matches brand preference)
- Alternative: March 8-15 (slightly cooler, $580 flight)
- Rejected: March 22-29 (moderate storm risk, safety concern)

## External API Integration

Currently, the tools use mocked data. To integrate real APIs:

1. **Weather**: Replace mock in `tools/weather.py` with OpenWeatherMap, WeatherAPI, or similar
2. **Flights**: Replace mock in `tools/flights.py` with Google Flights API, Amadeus, or similar
3. **Hotels**: Replace mock in `tools/hotels.py` with Booking.com API, Expedia API, or similar

All APIs should be justified in this README when integrated.

## Evaluation Criteria

This project is evaluated on:
- ✅ Correctness of agent decisions (epistemic reflection, tool ordering)
- ✅ Quality of tool contracts (names, docstrings, schemas)
- ✅ Architectural cleanliness (separation of concerns)
- ✅ Quality of synthesis and explanation
- ✅ Handling of ambiguity and trade-offs

## Common Failure Modes Avoided

- ❌ Answering immediately without profiling
- ❌ Treating tools as databases instead of abstractions
- ❌ Dumping raw API responses into agent context
- ❌ Overusing prompts to compensate for bad tool design

## License

MIT License
