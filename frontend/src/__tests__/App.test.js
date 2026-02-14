import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../App';
import { travelAgentService } from '../services/travelAgentService';

// Mock the travel agent service
jest.mock('../services/travelAgentService');

describe('App', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders app header', () => {
    render(<App />);

    expect(screen.getByText(/travel genie/i)).toBeInTheDocument();
    expect(screen.getByText(/ai-powered travel planning/i)).toBeInTheDocument();
  });

  test('renders travel query form', () => {
    const { container } = render(<App />);

    expect(screen.getByPlaceholderText(/ask me anything about your travel plans/i)).toBeInTheDocument();
    const submitButton = container.querySelector('button[type="submit"]');
    expect(submitButton).toBeInTheDocument();
  });

  test('displays loading spinner when loading', async () => {
    let resolvePromise;
    travelAgentService.getRecommendation.mockImplementation(
      () => new Promise((resolve) => {
        resolvePromise = resolve;
      })
    );

    const { container } = render(<App />);

    const textarea = screen.getByPlaceholderText(/ask me anything about your travel plans/i);
    const submitButton = container.querySelector('button[type="submit"]');

    // Submit form
    fireEvent.change(textarea, { target: { value: 'Is it a good time to go to Maui?' } });
    fireEvent.click(submitButton);

    // Should show loading state (button disabled or loading text)
    await waitFor(() => {
      const button = container.querySelector('button[type="submit"]');
      expect(button).toBeDisabled();
    });

    // Resolve the promise to clean up
    resolvePromise({
      success: true,
      recommendation: 'Test recommendation',
      query: 'Is it a good time to go to Maui?',
      userId: 'user_123'
    });
  });

  test('displays error message on service error', async () => {
    const errorMessage = 'Failed to get recommendation';
    travelAgentService.getRecommendation.mockRejectedValue(new Error(errorMessage));

    const { container } = render(<App />);

    const textarea = screen.getByPlaceholderText(/ask me anything about your travel plans/i);
    const submitButton = container.querySelector('button[type="submit"]');

    // Submit form
    fireEvent.change(textarea, { target: { value: 'Is it a good time to go to Maui?' } });
    fireEvent.click(submitButton);

    // Should show error message
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  test('displays recommendation when received', async () => {
    const mockRecommendation = {
      success: true,
      recommendation: 'Great time to visit Maui!',
      query: 'Is it a good time to go to Maui?',
      userId: 'user_123'
    };

    travelAgentService.getRecommendation.mockResolvedValue(mockRecommendation);

    const { container } = render(<App />);

    const textarea = screen.getByPlaceholderText(/ask me anything about your travel plans/i);
    const submitButton = container.querySelector('button[type="submit"]');

    // Submit form
    fireEvent.change(textarea, { target: { value: 'Is it a good time to go to Maui?' } });
    fireEvent.click(submitButton);

    // Should show recommendation
    await waitFor(() => {
      expect(screen.getByText(/great time to visit maui/i)).toBeInTheDocument();
    });
  });
});
