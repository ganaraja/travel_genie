# Testing Guide

This document describes the testing strategy and how to run tests for both the Python backend and React frontend.

## Python Backend Tests

### Test Structure

Tests are organized in the `tests/` directory:

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── test_core_models.py      # Tests for core data models
├── test_core_analysis.py    # Tests for analysis logic
├── test_core_scoring.py     # Tests for recommendation synthesis
├── test_tools.py            # Tests for MCP tools
└── test_agent.py            # Tests for agent module
```

### Running Tests

Using `uv`:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_core_models.py

# Run specific test
uv run pytest tests/test_core_models.py::TestUserProfile::test_user_profile_creation

# Run with verbose output
uv run pytest -v
```

### Test Coverage

The test suite aims for comprehensive coverage:

- **Core Models**: Tests for all data models (UserProfile, WeatherForecast, FlightOption, HotelOption, Recommendation)
- **Core Analysis**: Tests for weather analysis, flight filtering/scoring, hotel filtering/scoring, date overlap logic
- **Core Scoring**: Tests for recommendation synthesis with various scenarios
- **Tools**: Tests for all MCP tool wrappers (user profile, weather, flights, hotels)
- **Agent**: Tests for agent structure and tool wrapper functions

### Fixtures

Common test fixtures are defined in `conftest.py`:

- `sample_user_profile`: Sample user profile for testing
- `sample_weather_forecast`: Sample weather forecast with multiple periods
- `sample_flight_options`: Sample flight options (affordable and over-budget)
- `sample_hotel_options`: Sample hotel options (affordable and over-budget)

### Example Test

```python
def test_analyze_weather_perfect_match(sample_user_profile, sample_weather_forecast):
    """Test weather analysis with perfect temperature match."""
    results = analyze_weather_for_user(sample_weather_forecast, sample_user_profile)
    
    period, score, reason = results[0]
    assert score > 0.8
    assert "matches preference" in reason.lower()
```

## React Frontend Tests

### Test Structure

Tests are organized using Jest and React Testing Library:

```
frontend/src/
├── __tests__/
│   ├── components/
│   │   ├── TravelQueryForm.test.js
│   │   ├── RecommendationDisplay.test.js
│   │   ├── LoadingSpinner.test.js
│   │   └── ErrorMessage.test.js
│   ├── services/
│   │   └── travelAgentService.test.js
│   └── App.test.js
```

### Running Tests

```bash
cd frontend

# Run all tests once
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm test -- --coverage
```

### Test Utilities

- **Jest**: Test runner
- **React Testing Library (RTL)**: Testing utilities for React components
- **@testing-library/jest-dom**: Custom Jest matchers for DOM assertions
- **@testing-library/user-event**: User interaction simulation

### Component Testing

Each component has comprehensive tests covering:

1. **Rendering**: Components render correctly
2. **User Interactions**: Form inputs, button clicks, etc.
3. **Props**: Components handle props correctly
4. **State Changes**: Components update state appropriately
5. **Edge Cases**: Empty data, error states, loading states

### Example Test

```javascript
test('calls onSubmit with query and userId when form is submitted', () => {
  const mockOnSubmit = jest.fn();
  render(<TravelQueryForm onSubmit={mockOnSubmit} disabled={false} />);

  const textarea = screen.getByLabelText(/travel query/i);
  const submitButton = screen.getByRole('button', { name: /get recommendation/i });

  fireEvent.change(textarea, { target: { value: 'Is it a good time to go to Maui?' } });
  fireEvent.click(submitButton);

  expect(mockOnSubmit).toHaveBeenCalledWith('Is it a good time to go to Maui?', 'user_123');
});
```

### Service Testing

The `travelAgentService` is tested with mocked axios calls to verify:

- Correct API endpoints are called
- Request parameters are correct
- Responses are handled properly
- Errors are handled gracefully

## Continuous Integration

### Running All Tests

To run both backend and frontend tests:

```bash
# Backend tests
uv run pytest

# Frontend tests
cd frontend && npm test
```

### Coverage Goals

- **Backend**: Aim for >80% coverage of core logic
- **Frontend**: Aim for >80% coverage of components and services

## Writing New Tests

### Backend Tests

1. Create test file in `tests/` directory
2. Use fixtures from `conftest.py` when possible
3. Follow naming convention: `test_*.py` for files, `test_*` for functions
4. Use descriptive test names that explain what is being tested

### Frontend Tests

1. Create test file next to component or in `__tests__/` directory
2. Use React Testing Library queries (getByRole, getByLabelText, etc.)
3. Test user interactions, not implementation details
4. Mock external dependencies (API calls, etc.)

## Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Test names should clearly describe what is being tested
3. **Coverage**: Test happy paths, error cases, and edge cases
4. **Maintainability**: Use fixtures and helpers to reduce duplication
5. **Speed**: Keep tests fast - mock slow operations
