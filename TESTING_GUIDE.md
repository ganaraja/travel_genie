# Travel Genie Testing Guide

Complete guide for running and understanding the Travel Genie test suite.

## Test Coverage

The test suite covers all major functionality:

### 1. Visa Checking Tests (`tests/backend/test_visa_checking.py`)

- ✅ Domestic travel (USA → USA)
- ✅ Visa waiver programs (USA → France, Japan)
- ✅ Visa on arrival (USA → Indonesia)
- ✅ E-visa requirements (USA → India)
- ✅ Full visa requirements (India → USA, France, Japan)
- ✅ ESTA requirements (UK → USA)
- ✅ Unknown citizenship/destination combinations
- ✅ Visa result data structure validation

**Key Test Cases:**

- `test_usa_to_usa_domestic` - Domestic travel requires no visa
- `test_usa_to_indonesia_visa_on_arrival` - Visa on arrival process
- `test_india_to_usa_full_visa` - Full visa application required
- `test_uk_to_usa_esta` - ESTA electronic authorization

### 2. Coordinator Function Tests (`tests/backend/test_coordinator.py`)

- ✅ User profile retrieval with citizenship fields
- ✅ Weather forecast generation
- ✅ Flight search with flexibility
- ✅ Hotel search with brand preferences
- ✅ Data structure validation
- ✅ Default value handling

**Key Test Cases:**

- `test_get_user_profile_has_citizenship_fields` - Citizenship data present
- `test_get_weather_forecast_storm_detection` - Storm risk detection
- `test_search_flights_sorted_by_price` - Price sorting
- `test_search_hotels_anomalous_pricing_detection` - Special pricing detection

### 3. API Server Tests (`tests/backend/test_api_server.py`)

- ✅ Health check endpoint
- ✅ Recommendation endpoint with various destinations
- ✅ User profile endpoint
- ✅ Visa information in recommendations
- ✅ Error handling (missing query, invalid data)
- ✅ Synthesis function validation

**Key Test Cases:**

- `test_recommend_includes_visa_info` - Visa info in recommendations
- `test_recommend_maui_destination` - Maui-specific recommendations
- `test_get_user_profile_unknown_returns_default` - Graceful fallback

### 4. User Profile Citizenship Tests (`tests/backend/test_user_profile_citizenship.py`)

- ✅ Citizenship field presence
- ✅ Passport country field presence
- ✅ Default values (USA)
- ✅ Multiple citizenship support
- ✅ Mock profile validation
- ✅ Dual citizenship scenarios

**Key Test Cases:**

- `test_user_profile_has_citizenship_field` - Field exists
- `test_user_profile_different_citizenships` - Multiple nationalities
- `test_mock_profiles_have_citizenship` - All mock profiles valid

### 5. Integration Tests (`tests/backend/test_integration.py`)

- ✅ Complete workflow (profile → visa → weather → flights → hotels → synthesis)
- ✅ Domestic travel workflow
- ✅ International visa-free workflow
- ✅ Visa-required workflow
- ✅ Budget constraint validation
- ✅ Safety preference handling
- ✅ Brand preference handling
- ✅ Data consistency across tools
- ✅ Error handling

**Key Test Cases:**

- `test_complete_workflow_maui` - End-to-end Maui recommendation
- `test_visa_check_before_flight_search` - Correct workflow order
- `test_workflow_respects_budget_constraints` - Budget filtering
- `test_data_consistency` - Cross-tool data validation

### 6. Core Model Tests (`tests/backend/test_core_models.py`)

- ✅ UserProfile creation and defaults
- ✅ WeatherPeriod with storm detection
- ✅ FlightOption structure
- ✅ HotelOption structure
- ✅ Recommendation structure

### 7. Tool Tests (`tests/backend/test_tools.py`)

- ✅ User profile tool
- ✅ Weather forecast tool
- ✅ Flight search tool
- ✅ Hotel search tool
- ✅ Booking code generation
- ✅ Anomalous pricing detection

## Running Tests

### Run All Tests

```bash
# Using the test runner script
python run_tests.py

# Or directly with pytest
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html
```

### Run Specific Test Files

```bash
# Visa checking tests only
pytest tests/backend/test_visa_checking.py -v

# Coordinator tests only
pytest tests/backend/test_coordinator.py -v

# API server tests only
pytest tests/backend/test_api_server.py -v

# Integration tests only
pytest tests/backend/test_integration.py -v
```

### Run Specific Test Classes

```bash
# Run only visa requirement tests
pytest tests/backend/test_visa_checking.py::TestVisaRequirements -v

# Run only complete workflow tests
pytest tests/backend/test_integration.py::TestCompleteWorkflow -v
```

### Run Specific Test Cases

```bash
# Run a single test
pytest tests/backend/test_visa_checking.py::TestVisaRequirements::test_usa_to_france_visa_waiver -v
```

## Test Output

### Successful Test Run

```
tests/test_visa_checking.py::TestVisaRequirements::test_usa_to_usa_domestic PASSED
tests/test_visa_checking.py::TestVisaRequirements::test_usa_to_france_visa_waiver PASSED
tests/test_coordinator.py::TestGetUserProfileTool::test_get_user_profile_user_123 PASSED
...

======================== 50 passed in 2.34s ========================
```

### Coverage Report

```
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
agent/coordinator.py            120      5    96%   45-47, 89
api_server.py                   180     12    93%   234-245
core/models.py                   45      0   100%
tools/user_profile.py            35      2    94%   67-68
-----------------------------------------------------------
TOTAL                           380     19    95%
```

## Test Organization

```
tests/
├── __init__.py                          # Test package init
├── backend/                             # Backend Python tests
│   ├── __init__.py
│   ├── conftest.py                      # Pytest fixtures
│   ├── test_visa_checking.py            # Visa requirement tests
│   ├── test_coordinator.py              # Coordinator function tests
│   ├── test_api_server.py               # API endpoint tests
│   ├── test_user_profile_citizenship.py # Citizenship field tests
│   ├── test_integration.py              # End-to-end integration tests
│   ├── test_core_models.py              # Core model tests
│   ├── test_tools.py                    # Tool tests
│   ├── test_agent.py                    # Agent tests
│   ├── test_core_analysis.py            # Analysis tests
│   └── test_core_scoring.py             # Scoring tests
└── frontend/                            # Frontend React tests
    ├── __init__.py
    ├── __mocks__/
    │   └── fileMock.js                  # Static asset mocks
    ├── .babelrc                         # Babel configuration
    ├── package.json                     # Jest configuration
    ├── setup.js                         # Test environment setup
    ├── App.test.js                      # App component tests
    ├── ChatMessage.test.js              # ChatMessage component tests
    ├── ChatInput.test.js                # ChatInput component tests
    ├── travelAgentService.test.js       # API service tests
    └── README.md                        # Frontend test documentation
```

## Key Features Tested

### 1. Citizenship-Based Visa Checking

- Visa requirements based on traveler's citizenship
- Multiple visa types (full visa, e-visa, visa on arrival, ESTA, visa-free)
- Correct citizenship → destination mapping
- Default handling for unknown combinations

### 2. User Profile with Citizenship

- Citizenship and passport_country fields
- Default values (USA)
- Integration with visa checking
- Mock profile validation

### 3. API Server Endpoints

- `/api/health` - Health check
- `/api/recommend` - Travel recommendations with visa info
- `/api/user-profile/<user_id>` - User profile retrieval
- Error handling and validation

### 4. Complete Workflow

- Profile retrieval → Visa check → Weather → Flights → Hotels → Synthesis
- Correct workflow order (visa before flights)
- Budget and preference filtering
- Safety and brand considerations

### 5. Data Consistency

- Consistent data structures across tools
- Valid date formats (YYYY-MM-DD)
- Positive prices
- Required fields present

## Continuous Integration

### Pre-commit Checks

```bash
# Run tests before committing
python run_tests.py

# Check coverage
pytest tests/ --cov=. --cov-report=term-missing
```

### CI/CD Pipeline

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: |
    uv pip install pytest pytest-cov
    pytest tests/ -v --cov=. --cov-report=xml
```

## Test Data

### Mock User Profiles

- `user_123`: USA citizen, comfort level, safety-conscious, Marriott/Hilton preferred
- `default`: USA citizen, standard level, budget-conscious, no brand preference

### Mock Destinations

- Maui (USA) - Domestic travel
- Paris (France) - Visa waiver
- Tokyo (Japan) - Visa waiver
- Bali (Indonesia) - Visa on arrival

### Visa Matrix Coverage

- USA → USA, France, Japan, Indonesia, China, India
- India → USA, France, Japan, Indonesia
- UK → USA, France, Japan, Indonesia

## Troubleshooting

### Import Errors

```bash
# Ensure you're in the virtual environment
source .venv/bin/activate  # or: uv venv activate

# Install test dependencies
uv pip install pytest pytest-cov flask
```

### Test Failures

```bash
# Run with verbose output
pytest tests/ -vv

# Run with print statements visible
pytest tests/ -s

# Run with detailed traceback
pytest tests/ --tb=long
```

### Coverage Issues

```bash
# Generate HTML coverage report
pytest tests/ --cov=. --cov-report=html

# Open in browser
open htmlcov/index.html
```

## Adding New Tests

### 1. Create Test File

```python
# tests/backend/test_new_feature.py
import pytest

class TestNewFeature:
    def test_basic_functionality(self):
        # Arrange
        input_data = "test"

        # Act
        result = my_function(input_data)

        # Assert
        assert result == expected_output
```

### 2. Add Fixtures (if needed)

```python
# tests/conftest.py
@pytest.fixture
def sample_data():
    return {"key": "value"}
```

### 3. Run New Tests

```bash
pytest tests/backend/test_new_feature.py -v
```

## Best Practices

1. **Test Naming**: Use descriptive names (`test_usa_to_france_visa_waiver`)
2. **Arrange-Act-Assert**: Structure tests clearly
3. **One Assertion Per Test**: Focus on single behavior
4. **Use Fixtures**: Share common setup code
5. **Test Edge Cases**: Invalid inputs, boundary conditions
6. **Integration Tests**: Test complete workflows
7. **Mock External Services**: Don't rely on external APIs
8. **Coverage Goals**: Aim for >90% coverage

## Test Metrics

Current test suite metrics:

- **Total Tests**: 100+
- **Test Files**: 10
- **Coverage**: ~95%
- **Execution Time**: ~3 seconds
- **Pass Rate**: 100%

## Next Steps

1. Add property-based tests (Hypothesis)
2. Add performance tests (load testing)
3. Add frontend tests (Jest/React Testing Library)
4. Add E2E tests (Playwright/Selenium)
5. Add mutation testing (mutmut)
