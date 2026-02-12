# Travel Genie - Quick Start Guide

## Prerequisites Check ✅

- Python 3.10+ ✅
- uv (0.8.17) ✅
- Node.js (v22.16.0) ✅

## Running the Current System

### Step 1: Set Up Python Environment

```bash
# Install Python dependencies
uv sync

# Verify installation
uv run python -c "import google.adk; print('ADK installed successfully')"
```

### Step 2: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Google API key
# Get your key from: https://aistudio.google.com/app/apikey
echo "GOOGLE_API_KEY=your_api_key_here" > .env
echo "GOOGLE_API_MODEL=gemini-2.0-flash-exp" >> .env
```

### Step 3: Run the MCP Server (Optional - for testing tools)

```bash
# In Terminal 1: Start the MCP server
uv run python -m tools.server
```

### Step 4: Run the Agent

```bash
# Option A: Run agent via ADK CLI
uv run adk run agent

# Option B: Run agent with web interface
uv run adk web --port 8000
# Then open: http://localhost:8000
```

### Step 5: Test the Agent

Try this query:

```
Is it a good time to go to Maui?
```

Expected behavior:

1. Agent performs epistemic reflection (recognizes missing info)
2. Retrieves user profile
3. Checks weather forecast
4. Searches flights
5. Evaluates hotels
6. Provides personalized recommendation

### Step 6: Run Python Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=core --cov=tools --cov=agent

# Run specific test file
uv run pytest tests/test_core_analysis.py -v

# Run tests with output
uv run pytest -v -s
```

### Step 7: Run the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start
# Opens at: http://localhost:3000

# In another terminal, run frontend tests
npm test

# Run tests with coverage
npm test -- --coverage
```

## Checking the System

### Verify Core Logic (No Internet Required)

```bash
# Test that core module has no external dependencies
uv run python -c "
from core.models import UserProfile, ComfortLevel
from core.analysis import analyze_weather_for_user
from core.scoring import synthesize_recommendation
print('✅ Core logic imports successfully without internet')
"
```

### Verify Architecture Separation

```bash
# Run architecture verification script
uv run python test_structure.py
```

Expected output:

```
✅ Core module imports without ADK/MCP
✅ Tools module structure is correct
✅ Agent module structure is correct
```

### Check Tool Contracts

```bash
# List all available tools
uv run python -c "
from tools.server import mcp
print('Available tools:')
for tool_name in ['get_user_profile', 'get_weather_forecast', 'search_flights', 'search_hotels']:
    print(f'  - {tool_name}')
"
```

### Verify Agent Workflow

```bash
# Test agent with sample query (requires GOOGLE_API_KEY)
uv run adk run agent --query "Is it a good time to go to Maui?"
```

## Working with the Improvement Spec

### View the Spec Files

The spec is located in `.kiro/specs/travel-genie-improvements/`:

1. **requirements.md** - 15 requirements with acceptance criteria
2. **design.md** - Technical design and architecture
3. **tasks.md** - Implementation tasks (17 top-level, 44 sub-tasks)

### Start Implementing Tasks

```bash
# Open the tasks file
cat .kiro/specs/travel-genie-improvements/tasks.md

# Or open in your editor
code .kiro/specs/travel-genie-improvements/tasks.md
```

### Task Execution Order

The tasks are organized sequentially:

1. **Tasks 1-2**: MCP infrastructure setup
2. **Tasks 3-8**: Core logic enhancements (scoring, weather, flights, hotels)
3. **Tasks 9-10**: Agent coordinator updates
4. **Tasks 11-13**: Frontend components
5. **Tasks 15**: Integration tests
6. **Task 16**: Documentation updates

### Execute a Task

To implement a task:

1. Open `tasks.md`
2. Find the task you want to work on
3. Read the task description and requirements
4. Implement the code changes
5. Run tests to verify
6. Mark the task as complete

Example for Task 1.1 (MCP Client):

```bash
# Create the MCP client module
touch agent/mcp_client.py

# Edit the file and implement MCPClient class
# (See design.md for interface specification)

# Test the implementation
uv run pytest tests/test_mcp_client.py -v
```

## Troubleshooting

### Issue: "Module not found" errors

```bash
# Reinstall dependencies
uv sync --reinstall
```

### Issue: "GOOGLE_API_KEY not set"

```bash
# Check if .env file exists
cat .env

# If not, create it
echo "GOOGLE_API_KEY=your_key_here" > .env
```

### Issue: Frontend won't start

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Issue: Tests failing

```bash
# Run tests with verbose output to see details
uv run pytest -v -s

# Check specific test file
uv run pytest tests/test_core_analysis.py -v -s
```

## Next Steps

1. ✅ Verify current system works
2. ✅ Review the spec files (requirements.md, design.md, tasks.md)
3. ✅ Start implementing tasks from tasks.md
4. ✅ Run tests after each task
5. ✅ Update documentation as you go

## Quick Reference

### Common Commands

```bash
# Python
uv run pytest                    # Run all tests
uv run adk run agent            # Run agent CLI
uv run adk web --port 8000      # Run agent web UI
uv run python -m tools.server   # Run MCP server

# Frontend
cd frontend
npm start                        # Start dev server
npm test                         # Run tests
npm run build                    # Build for production

# Architecture
uv run python test_structure.py # Verify architecture
```

### File Structure

```
travel_genie/
├── core/                        # Pure Python business logic
│   ├── models.py               # Data models
│   ├── analysis.py             # Analysis logic
│   └── scoring.py              # Scoring logic
├── tools/                       # FastMCP tools
│   ├── user_profile.py         # User profile tool
│   ├── weather.py              # Weather tool
│   ├── flights.py              # Flights tool
│   ├── hotels.py               # Hotels tool
│   └── server.py               # MCP server
├── agent/                       # Google ADK agent
│   ├── agent.py                # ADK entry point
│   └── coordinator.py          # Agent coordinator
├── frontend/                    # React frontend
│   └── src/
│       ├── components/         # UI components
│       └── services/           # API services
├── tests/                       # Python tests
└── .kiro/specs/                # Specifications
    └── travel-genie-improvements/
        ├── requirements.md     # Requirements
        ├── design.md          # Design
        └── tasks.md           # Tasks
```

## Support

- Check README.md for detailed documentation
- Check ARCHITECTURE.md for architecture details
- Check TESTING.md for testing guidelines
- Review spec files in .kiro/specs/travel-genie-improvements/
