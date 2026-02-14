# Frontend Tests

Comprehensive test suite for Travel Genie React frontend.

## Test Coverage

### Components

- **App.test.js** - Main application component
  - Initial render and UI elements
  - User profile selection
  - Message handling and display
  - Loading states
  - Error handling
  - Clear chat functionality
  - Auto-scroll behavior
  - Accessibility

- **ChatMessage.test.js** - Message display component
  - User messages
  - Assistant messages
  - Error messages
  - Content parsing (visa, weather, flights, hotels)
  - Highlighting (recommendations, alternatives, warnings)
  - Info cards
  - Timestamp formatting

- **ChatInput.test.js** - Input component
  - User input handling
  - Keyboard shortcuts (Enter, Shift+Enter)
  - Example queries
  - Profile information display
  - Disabled states
  - Auto-resize textarea
  - Accessibility

### Services

- **travelAgentService.test.js** - API service
  - getRecommendation()
  - getUserProfile()
  - checkHealth()
  - Error handling
  - Timeout configuration
  - API base URL

## Running Tests

### Install Dependencies

```bash
cd tests/frontend
npm install
```

### Run All Tests

```bash
npm test
```

### Run Tests in Watch Mode

```bash
npm run test:watch
```

### Run Tests with Coverage

```bash
npm run test:coverage
```

### Run Specific Test File

```bash
npm test App.test.js
npm test ChatMessage.test.js
npm test ChatInput.test.js
npm test travelAgentService.test.js
```

### Run Tests with Verbose Output

```bash
npm run test:verbose
```

## Test Structure

```
tests/frontend/
├── __mocks__/
│   └── fileMock.js              # Mock for static assets
├── .babelrc                     # Babel configuration
├── package.json                 # Dependencies and scripts
├── setup.js                     # Test environment setup
├── App.test.js                  # App component tests
├── ChatMessage.test.js          # ChatMessage component tests
├── ChatInput.test.js            # ChatInput component tests
├── travelAgentService.test.js   # API service tests
└── README.md                    # This file
```

## Test Technologies

- **Jest** - Test framework
- **React Testing Library** - React component testing
- **@testing-library/jest-dom** - Custom matchers
- **@testing-library/user-event** - User interaction simulation
- **babel-jest** - Babel transformation
- **jsdom** - DOM implementation

## Writing New Tests

### Component Test Template

```javascript
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import MyComponent from "../../frontend/src/components/MyComponent";

describe("MyComponent", () => {
  test("renders correctly", () => {
    render(<MyComponent />);
    expect(screen.getByText("Expected Text")).toBeInTheDocument();
  });

  test("handles user interaction", () => {
    render(<MyComponent />);
    const button = screen.getByRole("button");
    fireEvent.click(button);
    expect(screen.getByText("Result")).toBeInTheDocument();
  });
});
```

### Service Test Template

```javascript
import axios from "axios";
import { myService } from "../../frontend/src/services/myService";

jest.mock("axios");

describe("MyService", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("makes API call", async () => {
    const mockResponse = { data: { result: "success" } };
    axios.get.mockResolvedValue(mockResponse);

    const result = await myService.getData();

    expect(axios.get).toHaveBeenCalledWith("/api/endpoint");
    expect(result).toEqual({ result: "success" });
  });
});
```

## Coverage Goals

- **Statements**: 70%+
- **Branches**: 70%+
- **Functions**: 70%+
- **Lines**: 70%+

## Common Testing Patterns

### Testing User Input

```javascript
const input = screen.getByPlaceholderText("Enter text");
fireEvent.change(input, { target: { value: "Test" } });
expect(input.value).toBe("Test");
```

### Testing Button Clicks

```javascript
const button = screen.getByRole("button", { name: /Submit/i });
fireEvent.click(button);
expect(mockFunction).toHaveBeenCalled();
```

### Testing Async Operations

```javascript
await waitFor(() => {
  expect(screen.getByText("Loaded")).toBeInTheDocument();
});
```

### Testing Error States

```javascript
mockService.mockRejectedValue(new Error("Failed"));
await expect(myFunction()).rejects.toThrow("Failed");
```

## Debugging Tests

### Run Single Test

```bash
npm test -- -t "test name"
```

### Debug with Node Inspector

```bash
node --inspect-brk node_modules/.bin/jest --runInBand
```

### View Console Output

```bash
npm test -- --verbose
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run frontend tests
  run: |
    cd tests/frontend
    npm install
    npm test -- --coverage
```

## Troubleshooting

### Module Not Found

```bash
npm install
```

### Transform Errors

Check `.babelrc` configuration

### DOM Errors

Ensure `testEnvironment: "jsdom"` in package.json

### Mock Errors

Clear mocks in `beforeEach`:

```javascript
beforeEach(() => {
  jest.clearAllMocks();
});
```

## Best Practices

1. **Test User Behavior** - Test what users see and do
2. **Avoid Implementation Details** - Don't test internal state
3. **Use Semantic Queries** - Prefer `getByRole`, `getByLabelText`
4. **Test Accessibility** - Ensure components are accessible
5. **Mock External Dependencies** - Mock API calls, services
6. **Clean Up** - Clear mocks and timers in `beforeEach`/`afterEach`
7. **Descriptive Names** - Use clear test descriptions
8. **One Assertion Per Test** - Focus on single behavior

## Resources

- [React Testing Library Docs](https://testing-library.com/react)
- [Jest Documentation](https://jestjs.io/)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
