# Complete Setup Guide

## Quick Start

### Backend Setup

1. **Install uv** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or: pip install uv
```

2. **Install Python dependencies**:
```bash
uv sync
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

4. **Run tests**:
```bash
uv run pytest
```

5. **Run the agent**:
```bash
uv run adk run agent
```

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm start
```

4. **Run tests**:
```bash
npm test
```

## Project Structure

```
travel_genie/
├── core/              # Pure Python business logic
├── tools/             # FastMCP tool wrappers
├── agent/             # Google ADK coordinator
├── tests/             # Pytest test suite
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   └── __tests__/       # Jest + RTL tests
│   └── package.json
├── pyproject.toml     # Python project config (uv)
└── README.md
```

## Testing

### Backend Tests (Pytest)

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_core_models.py
```

### Frontend Tests (Jest + RTL)

```bash
cd frontend

# Run all tests
npm test

# Run in watch mode
npm run test:watch

# Run with coverage
npm test -- --coverage
```

## Development Workflow

1. **Make changes** to code
2. **Run tests** to verify functionality
3. **Test manually** using the frontend or ADK CLI
4. **Commit** changes

## Key Technologies

- **Backend**: Python 3.10+, Google ADK, FastMCP, pytest
- **Frontend**: React 18, Jest, React Testing Library
- **Package Management**: uv (Python), npm (Node.js)

## Troubleshooting

### Backend Issues

- **Import errors**: Make sure you've run `uv sync`
- **ADK not found**: Check that `google-adk` is installed: `uv run pip list | grep adk`
- **Environment variables**: Verify `.env` file exists and has `GOOGLE_API_KEY`

### Frontend Issues

- **Dependencies**: Run `npm install` in the `frontend/` directory
- **Port conflicts**: Change port in `package.json` scripts or use `PORT=3001 npm start`
- **API connection**: Check that backend is running and `REACT_APP_API_URL` is set correctly

## Next Steps

1. ✅ Install dependencies: `uv sync` (backend) and `npm install` (frontend)
2. ✅ Set up `.env` with `GOOGLE_API_KEY`
3. ✅ Run tests: `uv run pytest` and `npm test`
4. ✅ Run agent: `uv run adk run agent`
5. ✅ Start frontend: `cd frontend && npm start`
6. ✅ Test with query: "Is it a good time to go to Maui?"
