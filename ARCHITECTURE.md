# Architecture Documentation

## Separation of Concerns

This project enforces strict architectural boundaries:

### Core Module (`core/`)
- **Purpose**: Pure Python business logic
- **Dependencies**: Standard library only (dataclasses, datetime, typing, enum)
- **Rule**: MUST NOT import Google ADK, MCP, FastMCP, or any orchestration framework
- **Verification**: Can be imported in a Python REPL without internet access

**Contents**:
- `models.py`: Data models (UserProfile, WeatherForecast, FlightOption, HotelOption, Recommendation)
- `analysis.py`: Analysis logic (weather scoring, flight/hotel filtering)
- `scoring.py`: Recommendation synthesis logic

### Tools Module (`tools/`)
- **Purpose**: FastMCP wrappers around core functions
- **Dependencies**: FastMCP, Pydantic, core module
- **Rule**: Wraps core functions and exposes them as MCP tools
- **Design**: Returns only essential fields, summarizes data, documents outputs clearly

**Contents**:
- `user_profile.py`: User profile retrieval tool
- `weather.py`: Weather forecast tool
- `flights.py`: Flight search tool
- `hotels.py`: Hotel search tool
- `server.py`: Unified MCP server combining all tools

### Agent Module (`agent/`)
- **Purpose**: Google ADK coordinator that orchestrates reasoning and tool use
- **Dependencies**: Google ADK, tools module (via function wrappers)
- **Rule**: Does NOT import core logic directly - only uses tools
- **Design**: Coordinates multi-stage reasoning workflow

**Contents**:
- `coordinator.py`: Main agent with 6-stage workflow
- `agent.py`: ADK entry point

## Data Flow

```
User Query
    ↓
Agent (Google ADK)
    ↓
Tool Functions (wrapped for ADK)
    ↓
MCP Tools (FastMCP)
    ↓
Core Functions (pure Python)
    ↓
Business Logic Results
    ↓
Agent Synthesis
    ↓
Final Recommendation
```

## Tool Design Principles

### 1. Context Budget Discipline
- No tool returns unbounded text or raw JSON dumps
- Each tool returns only fields required for reasoning
- Summaries provided when necessary
- Clear documentation in docstrings

### 2. Idempotency
- Tools that could be retried are idempotent
- Booking actions use `booking_code` for idempotency
- Profile updates are safe to retry
- Search operations are idempotent

### 3. Abstraction, Not Database
- Tools provide abstractions, not raw data dumps
- Agent reasons about tool outputs, not raw API responses
- Tools encapsulate business logic from core module

## Agent Workflow

The coordinator agent follows a strict 6-stage workflow:

1. **Epistemic Reflection**: Recognize underspecification
2. **User Profile Retrieval**: Get user preferences (MUST happen first)
3. **Weather Analysis**: Consult weather forecast
4. **Flight Search**: Search flight options
5. **Hotel Evaluation**: Evaluate lodging options
6. **Synthesis**: Produce personalized recommendation

## Verification

Run `python3 test_structure.py` to verify:
- ✅ Core module imports without ADK/MCP
- ✅ Tools module structure is correct
- ✅ Agent module structure is correct

## Extension Points

### Adding New Tools
1. Create function in `core/` module (pure Python)
2. Create FastMCP wrapper in `tools/` module
3. Add function tool wrapper in `agent/coordinator.py`
4. Register tool with agent

### Integrating Real APIs
1. Replace mock implementations in `tools/*.py`
2. Maintain same response schemas
3. Ensure idempotency for booking operations
4. Document API choices in README

## Testing Strategy

- **Unit Tests**: Test core logic independently
- **Integration Tests**: Test tool wrappers with core functions
- **Agent Tests**: Test agent reasoning and tool orchestration
- **End-to-End Tests**: Test full workflow with mock data
