# Implementation Plan: Travel Genie Improvements

## Overview

This implementation plan breaks down the Travel Genie improvements into discrete coding tasks. The approach follows this sequence:

1. Set up MCP infrastructure (client/server)
2. Enhance core scoring algorithms
3. Update agent coordinator with MCP integration and epistemic reflection
4. Implement frontend components for reasoning display
5. Add comprehensive testing (property-based and unit tests)
6. Update documentation

Each task builds incrementally, ensuring the system remains functional throughout development.

## Tasks

- [ ] 1. Set up MCP client infrastructure
  - [ ] 1.1 Create MCP client module with connection handling
    - Implement `MCPClient` class in `agent/mcp_client.py`
    - Add async methods for `call_tool()`, `list_tools()`, and `close()`
    - Implement connection pooling and retry logic with exponential backoff
    - Add custom exception types: `MCPConnectionError` and `MCPToolError`
    - _Requirements: 2.1, 2.4_

  - [ ]\* 1.2 Write property test for MCP serialization round-trip
    - **Property 1: MCP Protocol Round-Trip**
    - **Validates: Requirements 2.4**
    - Generate random tool requests, serialize to MCP format, deserialize, verify equivalence
    - Test with edge cases (empty arguments, null values, nested objects)

  - [ ]\* 1.3 Write unit tests for MCP client error handling
    - Test connection failures and retry logic
    - Test timeout handling
    - Test malformed response handling
    - _Requirements: 2.1_

- [ ] 2. Enhance MCP server with tool registration
  - [ ] 2.1 Update MCP server to register all tools on startup
    - Modify `tools/server.py` to auto-discover and register all tool functions
    - Add tool metadata (name, description, parameters) to registration
    - Implement `/tools` endpoint to list available tools
    - _Requirements: 2.3_

  - [ ]\* 2.2 Write integration test for tool registration
    - Start MCP server, query `/tools` endpoint
    - Verify all expected tools are registered
    - Verify tool metadata is complete
    - _Requirements: 2.3_

- [ ] 3. Implement unified scoring module
  - [ ] 3.1 Create holistic scoring functions in core/scoring.py
    - Implement `ScoringWeights`, `FactorScore`, and `HolisticScore` dataclasses
    - Implement `score_travel_option()` function that combines all factors
    - Implement individual scoring functions: `score_weather()`, `score_flight()`, `score_hotel()`, `score_schedule()`
    - Ensure all scores are normalized to [0.0, 1.0] range
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ]\* 3.2 Write property test for factor normalization
    - **Property 2: Scoring Factor Normalization**
    - **Validates: Requirements 3.3**
    - Generate random travel options and profiles
    - Verify all factor scores are in [0.0, 1.0] range

  - [ ]\* 3.3 Write property test for scoring monotonicity
    - **Property 3: Scoring Monotonicity with Preference Satisfaction**
    - **Validates: Requirements 3.4**
    - Generate random options, improve one factor, verify score doesn't decrease

  - [ ]\* 3.4 Write property test for weighted trade-offs
    - **Property 4: Weighted Trade-Off Application**
    - **Validates: Requirements 3.2**
    - Generate two options with different strengths, vary weights, verify relative scores change appropriately

- [ ] 4. Checkpoint - Ensure scoring tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement enhanced weather analysis
  - [ ] 5.1 Create weather analysis functions in core/analysis.py
    - Implement `WeatherMatchResult` dataclass
    - Implement `analyze_weather_match()` function
    - Implement `calculate_temperature_score()` with linear decay outside preferred range
    - Implement `calculate_storm_risk_score()` with severity-weighted penalties
    - Implement `identify_optimal_windows()` to find best periods
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [ ]\* 5.2 Write property test for weather scoring monotonicity
    - **Property 5: Weather Scoring Monotonicity**
    - **Validates: Requirements 4.2, 4.3**
    - Generate random forecasts, increase temperature deviation or storm severity, verify score doesn't increase

  - [ ]\* 5.3 Write property test for optimal window identification
    - **Property 6: Optimal Weather Window Identification**
    - **Validates: Requirements 4.4**
    - Generate random forecasts, identify optimal window, verify it has highest score

  - [ ]\* 5.4 Write unit tests for weather analysis edge cases
    - Test with no storm periods
    - Test with all storm periods
    - Test with temperatures far outside preferred range
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 6. Implement advanced flight scoring
  - [ ] 6.1 Create flight scoring functions in core/scoring.py
    - Implement `calculate_flight_price_score()` with soft/hard budget handling
    - Implement `calculate_schedule_flexibility_score()` with weekday/red-eye bonuses
    - Implement `calculate_flight_duration_score()` considering layovers and total time
    - Integrate into `score_flight()` function
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ]\* 6.2 Write property test for flight flexibility reward
    - **Property 7: Flight Flexibility Reward**
    - **Validates: Requirements 5.1**
    - Generate pairs of identical flights (one weekday/red-eye, one not), verify flexible users score weekday/red-eye higher

  - [ ]\* 6.3 Write property test for budget constraint enforcement
    - **Property 8: Flight Budget Constraint Enforcement**
    - **Validates: Requirements 5.2, 5.3, 5.4**
    - Generate flights at various price points, verify score ranges match budget constraints

  - [ ]\* 6.4 Write unit tests for flight scoring edge cases
    - Test with price exactly at soft budget
    - Test with price exactly at hard budget
    - Test with zero flexibility
    - Test with maximum layovers
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 7. Implement nuanced hotel scoring
  - [ ] 7.1 Create hotel scoring functions in core/scoring.py
    - Implement `calculate_hotel_price_score()` with budget range handling
    - Implement `calculate_brand_preference_score()` with preferred brand bonuses
    - Implement `calculate_anomaly_impact()` with safety-conscious weighting
    - Implement `calculate_hotel_rating_score()` for comfort factor
    - Integrate into `score_hotel()` function
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [ ]\* 7.2 Write property test for brand preference reward
    - **Property 9: Hotel Brand Preference Reward**
    - **Validates: Requirements 6.1**
    - Generate pairs of identical hotels (one with preferred brand, one without), verify preferred brand scores higher

  - [ ]\* 7.3 Write property test for anomalous pricing detection
    - **Property 10: Anomalous Pricing Detection and Flagging**
    - **Validates: Requirements 6.2**
    - Generate hotels with anomalous pricing, verify flag and reason are present

  - [ ]\* 7.4 Write property test for safety-conscious anomaly penalty
    - **Property 11: Safety-Conscious Anomaly Penalty**
    - **Validates: Requirements 6.3**
    - Generate hotels with storm-related anomalous pricing, verify safety-conscious users get lower scores

  - [ ]\* 7.5 Write unit tests for hotel scoring edge cases
    - Test with rate below budget minimum
    - Test with rate above budget maximum
    - Test with multiple preferred brands
    - Test with anomalous pricing and non-safety-conscious user
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 8. Checkpoint - Ensure core logic tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Update agent coordinator with MCP integration
  - [ ] 9.1 Refactor coordinator to use MCP client
    - Modify `agent/coordinator.py` to inject `MCPClient` dependency
    - Replace direct tool imports with `mcp_client.call_tool()` calls
    - Implement `call_tool_with_trace()` to record reasoning steps
    - Add `reasoning_trace` list to capture all agent actions
    - _Requirements: 2.1, 2.5_

  - [ ] 9.2 Add epistemic reflection prompts to agent instructions
    - Add `EPISTEMIC_REFLECTION_PROMPT` to agent instructions
    - Update agent instruction to explicitly require reflection before tool calls
    - Add prompts to identify missing information and explain why it's needed
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ] 9.3 Enhance synthesis prompts for nuanced explanations
    - Add `SYNTHESIS_PROMPT` with requirements for factor-by-factor reasoning
    - Update prompts to require alternative options with explanations
    - Update prompts to require rejected periods with reasons
    - Update prompts to require trade-off acknowledgment
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ]\* 9.4 Write integration test for agent-MCP workflow
    - Start MCP server and agent with MCP client
    - Send test query, verify agent calls tools via MCP
    - Verify reasoning trace captures all steps
    - Verify epistemic reflection appears in output
    - _Requirements: 2.1, 1.1_

- [ ] 10. Create enhanced data models
  - [ ] 10.1 Add new dataclasses to core/models.py
    - Implement `MCPToolRequest` and `MCPToolResponse` dataclasses
    - Implement `ReasoningStep` dataclass for reasoning trace
    - Implement `ScoringWeights`, `FactorScore`, `HolisticScore` dataclasses
    - Implement `EnhancedRecommendation`, `RecommendationOption`, `RejectedOption`, `TradeOffExplanation` dataclasses
    - _Requirements: 3.1, 7.1_

  - [ ]\* 10.2 Write property test for data serialization round-trip
    - **Property 14: Data Serialization Round-Trip**
    - **Validates: Requirements 15.1, 15.2, 15.3, 15.4**
    - Generate random instances of all data models
    - Serialize to JSON, deserialize, verify equivalence
    - Test with edge cases (empty lists, None values, boundary values)

- [ ] 11. Implement frontend reasoning display component
  - [ ] 11.1 Create ReasoningDisplay component
    - Create `frontend/src/components/ReasoningDisplay.tsx`
    - Implement timeline view with stages connected by lines
    - Add `ReasoningStepCard` sub-component for each step
    - Implement expandable details for tool calls and responses
    - Add color coding (blue for in-progress, green for complete, gray for pending)
    - Add smooth animations between stages
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

  - [ ]\* 11.2 Write property test for chronological ordering
    - **Property 12: Reasoning Steps Chronological Ordering**
    - **Validates: Requirements 8.3**
    - Generate random reasoning steps with timestamps
    - Render component, verify steps appear in chronological order

  - [ ]\* 11.3 Write unit tests for ReasoningDisplay component
    - Test rendering with empty steps
    - Test rendering with all stage types
    - Test expand/collapse functionality
    - Test active step highlighting
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 12. Implement frontend options display component
  - [ ] 12.1 Create OptionsDisplay component
    - Create `frontend/src/components/OptionsDisplay.tsx`
    - Implement `PrimaryRecommendation` sub-component with prominent styling
    - Implement `AlternativesSection` sub-component for alternatives
    - Implement `RejectedPeriodsSection` sub-component with collapsible list
    - Implement `ComparisonView` modal for side-by-side comparison
    - Add factor-by-factor breakdown for each option
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ]\* 12.2 Write unit tests for OptionsDisplay component
    - Test primary recommendation rendering
    - Test alternatives rendering with explanations
    - Test rejected periods rendering with reasons
    - Test comparison view modal
    - Test expand/collapse for option details
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 13. Implement frontend profile management component
  - [ ] 13.1 Create ProfileManager component
    - Create `frontend/src/components/ProfileManager.tsx`
    - Implement `ProfileDisplay` sub-component for read-only view
    - Implement `ProfileEditForm` sub-component with all profile fields
    - Add form fields: temperature range slider, budget sliders, brand multi-select, trip length input, comfort radio buttons, flexibility slider, safety toggle
    - Implement real-time validation for all fields
    - Add helpful descriptions for each field
    - _Requirements: 10.1, 10.2, 10.5_

  - [ ] 13.2 Implement profile update API integration
    - Add API call to persist profile changes
    - Handle success and error responses
    - Display confirmation message on success
    - Display error messages on failure
    - _Requirements: 10.3, 10.4_

  - [ ]\* 13.3 Write property test for profile form validation
    - **Property 13: Profile Form Validation**
    - **Validates: Requirements 10.2**
    - Generate invalid profile inputs (soft > hard budget, min > max temp, negative values)
    - Verify validation prevents submission and shows errors

  - [ ]\* 13.4 Write unit tests for ProfileManager component
    - Test profile display rendering
    - Test edit mode toggle
    - Test form field rendering
    - Test validation error display
    - Test successful submission flow
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 14. Checkpoint - Ensure frontend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 15. Add comprehensive integration tests
  - [ ]\* 15.1 Write integration test for MCP client-server communication
    - Start MCP server in test mode
    - Create MCP client, call each tool
    - Verify requests are properly serialized
    - Verify responses are properly deserialized
    - Test error handling for connection failures and tool errors
    - _Requirements: 2.1, 2.4_

  - [ ]\* 15.2 Write integration test for agent workflow with MCP
    - Start MCP server and create agent with MCP client
    - Send test query: "Is it a good time to go to Maui?"
    - Verify agent performs epistemic reflection
    - Verify agent calls tools in correct order (profile → weather → flights → hotels)
    - Verify reasoning trace captures all steps
    - Verify final recommendation includes all required elements
    - _Requirements: 1.1, 2.1, 7.1_

  - [ ]\* 15.3 Write end-to-end test for complete recommendation flow
    - Start full system (MCP server, agent, frontend)
    - Submit query through frontend
    - Verify reasoning display shows all stages
    - Verify recommendation includes primary, alternatives, and rejected periods
    - Verify all factor explanations are present
    - _Requirements: 1.1, 7.1, 8.1, 9.1_

- [ ] 16. Update documentation
  - [ ] 16.1 Update README with MCP server setup instructions
    - Add section on starting MCP server separately
    - Add section on configuring MCP client connection
    - Add troubleshooting for common MCP connection issues
    - Update architecture diagram to show MCP integration
    - _Requirements: 14.1, 14.5_

  - [ ] 16.2 Create API integration guide
    - Create `docs/API_INTEGRATION.md` file
    - Add sections for each external API (weather, flights, hotels)
    - Include code examples for replacing mock implementations
    - Add authentication and rate limiting guidance
    - _Requirements: 14.2_

  - [ ] 16.3 Create deployment guide
    - Create `docs/DEPLOYMENT.md` file
    - Add instructions for Docker deployment
    - Add instructions for AWS deployment (Lambda + API Gateway)
    - Add instructions for GCP deployment (Cloud Run)
    - Add instructions for Heroku deployment
    - Include environment variable configuration
    - _Requirements: 14.3_

  - [ ] 16.4 Create troubleshooting guide
    - Create `docs/TROUBLESHOOTING.md` file
    - Add common issues and solutions for MCP connection problems
    - Add debugging tips for agent reasoning issues
    - Add performance optimization tips
    - Add FAQ section
    - _Requirements: 14.4_

- [ ] 17. Final checkpoint - Ensure all tests pass
  - Run full test suite (unit, property, integration, frontend)
  - Verify all property tests run at least 100 iterations
  - Verify test coverage meets goals (core: 90%, tools: 85%, frontend: 80%)
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties with 100+ iterations
- Unit tests validate specific examples and edge cases
- Integration tests validate component interactions
- Frontend tests validate UI components and user interactions
- All property tests must include comment tags referencing design properties
