# Requirements Document

## Introduction

This document specifies requirements for the Travel Genie AI Travel Recommendation System improvements that have been implemented and are planned. The system provides travel recommendations by coordinating user profiles, weather forecasts, flight searches, and hotel searches through a Google ADK agent with a React frontend.

**Status**: This spec has been updated to reflect completed work (Tasks 1-6 from context transfer) and remaining planned improvements.

**Completed Features**:

- Citizenship-based visa checking
- Comprehensive test suite (backend and frontend)
- Support for 40+ destinations including 30+ Indian cities
- Always show top 3 flight and hotel options
- Destination-specific output display

**Planned Improvements** (Hybrid Approach - Option 3):

- Basic multi-factor scoring (without MCP infrastructure)
- Real API integrations (weather, flights, hotels)
- Frontend profile editing
- Property-based tests for critical paths
- Improved error handling and loading states
- Better recommendation quality with enhanced heuristics

## Glossary

- **Agent**: The Google ADK coordinator that orchestrates reasoning and tool calls
- **Tool**: A function that provides data or performs actions (user profile, weather, flights, hotels)
- **Core_Logic**: Pure Python business logic in the core/ module
- **User_Profile**: Structured data containing user preferences and constraints
- **Scoring_Algorithm**: Logic that evaluates and ranks travel options
- **Property_Test**: A test that validates universal properties across many inputs
- **Frontend**: The React-based user interface
- **API_Integration**: Connection to real external APIs (weather, flights, hotels)
- **Heuristic**: A practical rule or algorithm for making decisions
- **MCP_Client**: Client code that calls tools through the MCP protocol
- **Core_Logic**: Pure Python business logic in the core/ module
- **Epistemic_Reflection**: The agent's explicit recognition of what it doesn't know
- **User_Profile**: Structured data containing user preferences and constraints
- **Scoring_Algorithm**: Logic that evaluates and ranks travel options
- **Synthesis**: The process of combining multiple data sources into a recommendation
- **Property_Test**: A test that validates universal properties across many inputs
- **Frontend**: The React-based user interface

## Completed Requirements

### Requirement C1: Citizenship-Based Visa Checking

**User Story:** As a user, I want the system to check visa requirements based on my citizenship before showing flight options, so that I don't book non-refundable flights without proper travel authorization.

**Status**: ✅ COMPLETED

#### Acceptance Criteria

1. ✅ WHEN a user queries about a destination, THE system SHALL retrieve the user's citizenship from their profile
2. ✅ WHEN checking visa requirements, THE system SHALL use citizenship (not booking location) to determine requirements
3. ✅ WHEN a visa is required, THE system SHALL display visa information BEFORE flight and hotel options
4. ✅ WHEN a full visa is required, THE system SHALL recommend obtaining the visa before booking
5. ✅ THE system SHALL support multiple visa types: visa-free, visa waiver, e-visa, visa on arrival, ESTA, and full visa
6. ✅ THE system SHALL provide processing time, cost, and maximum stay information for each visa type

### Requirement C2: Comprehensive Test Coverage

**User Story:** As a developer, I want comprehensive test coverage for all functionality, so that I can confidently make changes without breaking existing features.

**Status**: ✅ COMPLETED

#### Acceptance Criteria

1. ✅ THE system SHALL have separate test folders for backend (Python/Pytest) and frontend (React/Jest)
2. ✅ THE backend tests SHALL cover visa checking, coordinator, API server, and integration scenarios (86+ tests)
3. ✅ THE frontend tests SHALL cover App, ChatMessage, ChatInput, and travelAgentService components (130+ tests)
4. ✅ THE system SHALL include test documentation explaining how to run tests
5. ✅ ALL tests SHALL pass successfully

### Requirement C3: Extensive Destination Support

**User Story:** As a user, I want to ask about many different destinations, so that I can get recommendations for any city I'm interested in visiting.

**Status**: ✅ COMPLETED

#### Acceptance Criteria

1. ✅ THE system SHALL support 40+ destinations worldwide
2. ✅ THE system SHALL include 30+ Indian cities (metros, tourist destinations, and regional cities)
3. ✅ THE system SHALL map destination names to correct airport codes
4. ✅ THE system SHALL display destination-specific information in weather, flights, and hotels
5. ✅ THE frontend SHALL include example queries for major destinations including India

### Requirement C4: Top Options Display

**User Story:** As a user, I want to always see the top 3 flight and hotel options even if they don't match my preferences, so that I can make informed decisions about trade-offs.

**Status**: ✅ COMPLETED

#### Acceptance Criteria

1. ✅ THE system SHALL always display top 3 flight options regardless of budget match
2. ✅ THE system SHALL always display top 3 hotel options regardless of budget match
3. ✅ EACH option SHALL include detailed information: price, dates, duration, layovers, rating
4. ✅ EACH option SHALL include clear budget indicators: ✓ Within budget, ⚠️ Over soft budget, ⚠️ Outside budget
5. ✅ THE system SHALL show special markers: ⭐ Preferred brand, 💰 Special pricing
6. ✅ THE recommendation SHALL include budget considerations and guidance even when over budget

## Planned Requirements (Hybrid Approach)

### Requirement 1: Basic Multi-Factor Scoring

**User Story:** As a user, I want travel options to be scored considering multiple factors, so that recommendations reflect realistic trade-offs.

#### Acceptance Criteria

1. WHEN scoring a travel option, THE Scoring_Algorithm SHALL consider weather, price, and schedule factors
2. WHEN calculating scores, THE Scoring_Algorithm SHALL normalize scores to a common scale (0.0-1.0)
3. WHEN multiple options exist, THE Scoring_Algorithm SHALL rank them by combined score
4. THE Scoring_Algorithm SHALL provide explanation text for each score
5. THE Scoring_Algorithm SHALL be implemented in core/scoring.py without external dependencies

### Requirement 2: Real Weather API Integration

**User Story:** As a user, I want real weather forecasts, so that recommendations are based on actual conditions.

#### Acceptance Criteria

1. WHEN requesting weather data, THE system SHALL call a real weather API (OpenWeatherMap or similar)
2. WHEN the API call fails, THE system SHALL fall back to mock data with a warning message
3. WHEN displaying weather, THE system SHALL show temperature, conditions, and precipitation
4. THE system SHALL cache weather data for 1 hour to reduce API calls
5. THE system SHALL handle API rate limits gracefully

### Requirement 3: Real Flight API Integration

**User Story:** As a user, I want real flight prices and availability, so that I can make actual bookings.

#### Acceptance Criteria

1. WHEN searching flights, THE system SHALL call a real flight API (Amadeus, Skyscanner, or similar)
2. WHEN the API call fails, THE system SHALL fall back to mock data with a warning message
3. WHEN displaying flights, THE system SHALL show actual airlines, prices, and times
4. THE system SHALL cache flight data for 15 minutes to reduce API calls
5. THE system SHALL handle API rate limits and errors gracefully

### Requirement 4: Real Hotel API Integration

**User Story:** As a user, I want real hotel prices and availability, so that I can make actual bookings.

#### Acceptance Criteria

1. WHEN searching hotels, THE system SHALL call a real hotel API (Booking.com, Hotels.com, or similar)
2. WHEN the API call fails, THE system SHALL fall back to mock data with a warning message
3. WHEN displaying hotels, THE system SHALL show actual properties, prices, and ratings
4. THE system SHALL cache hotel data for 1 hour to reduce API calls
5. THE system SHALL handle API rate limits and errors gracefully

### Requirement 5: Frontend Profile Editing

**User Story:** As a user, I want to edit my travel preferences in the UI, so that recommendations are personalized.

#### Acceptance Criteria

1. WHEN accessing the profile page, THE Frontend SHALL display all User_Profile fields in an editable form
2. WHEN updating profile fields, THE Frontend SHALL validate input before submission
3. WHEN profile updates are submitted, THE Frontend SHALL call the API to persist changes
4. WHEN profile updates succeed, THE Frontend SHALL display a confirmation message
5. THE Frontend SHALL provide helpful descriptions for each profile field

### Requirement 6: Enhanced Error Handling

**User Story:** As a user, I want clear error messages, so that I understand what went wrong and how to fix it.

#### Acceptance Criteria

1. WHEN an API call fails, THE system SHALL display a user-friendly error message
2. WHEN validation fails, THE system SHALL show specific field-level errors
3. WHEN the system is loading, THE Frontend SHALL show loading indicators
4. WHEN errors occur, THE system SHALL log detailed information for debugging
5. THE system SHALL provide retry options for transient failures

### Requirement 7: Property-Based Tests for Critical Paths

**User Story:** As a developer, I want property-based tests for critical functionality, so that edge cases are caught.

#### Acceptance Criteria

1. WHEN testing visa checking, THE Property_Test SHALL validate all citizenship/destination combinations
2. WHEN testing scoring, THE Property_Test SHALL validate score normalization (0.0-1.0 range)
3. WHEN testing data serialization, THE Property_Test SHALL validate round-trip equivalence
4. WHEN testing budget constraints, THE Property_Test SHALL validate soft/hard budget enforcement
5. THE Property_Test SHALL run at least 100 iterations per property

### Requirement 8: Improved Recommendation Quality

**User Story:** As a user, I want better recommendations, so that suggestions match my preferences more closely.

#### Acceptance Criteria

1. WHEN analyzing weather, THE system SHALL compare temperatures against user preferences
2. WHEN scoring flights, THE system SHALL reward weekday and red-eye options for flexible users
3. WHEN scoring hotels, THE system SHALL reward preferred brands
4. WHEN synthesizing recommendations, THE system SHALL explain trade-offs clearly
5. THE system SHALL provide 2-3 alternative options with explanations

### Requirement 9: API Configuration Management

**User Story:** As a developer, I want easy API configuration, so that I can switch between mock and real APIs.

#### Acceptance Criteria

1. WHEN configuring APIs, THE system SHALL use environment variables for API keys
2. WHEN an API key is missing, THE system SHALL fall back to mock data automatically
3. WHEN in development mode, THE system SHALL allow using mock data explicitly
4. THE system SHALL provide clear documentation for API setup
5. THE system SHALL validate API keys on startup and warn if invalid

### Requirement 10: Performance Optimization

**User Story:** As a user, I want fast responses, so that I can get recommendations quickly.

#### Acceptance Criteria

1. WHEN making API calls, THE system SHALL use caching to reduce redundant requests
2. WHEN multiple APIs are needed, THE system SHALL call them in parallel where possible
3. WHEN displaying results, THE Frontend SHALL show partial results as they arrive
4. THE system SHALL complete most queries in under 5 seconds
5. THE system SHALL provide progress indicators for long-running operations
