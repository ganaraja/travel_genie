import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
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
    expect(screen.getByText(/ai-powered travel recommendation assistant/i)).toBeInTheDocument();
  });

  test('renders travel query form', () => {
    render(<App />);

    expect(screen.getByLabelText(/travel query/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /get recommendation/i })).toBeInTheDocument();
  });

  test('displays loading spinner when loading', async () => {
    travelAgentService.getRecommendation.mockImplementation(
      () => new Promise((resolve) => setTimeout(() => resolve({}), 100))
    );

    render(<App />);

    const textarea = screen.getByLabelText(/travel query/i);
    const submitButton = screen.getByRole('button', { name: /get recommendation/i });

    // Submit form
    textarea.value = 'Is it a good time to go to Maui?';
    submitButton.click();

    // Should show loading spinner
    await waitFor(() => {
      expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
    });
  });

  test('displays error message on service error', async () => {
    const errorMessage = 'Failed to get recommendation';
    travelAgentService.getRecommendation.mockRejectedValue(new Error(errorMessage));

    render(<App />);

    const textarea = screen.getByLabelText(/travel query/i);
    const submitButton = screen.getByRole('button', { name: /get recommendation/i });

    // Submit form
    textarea.value = 'Is it a good time to go to Maui?';
    submitButton.click();

    // Should show error message
    await waitFor(() => {
      expect(screen.getByTestId('error-message')).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  test('displays recommendation when received', async () => {
    const mockRecommendation = {
      recommended_start: '2026-02-09',
      recommended_end: '2026-02-16',
      primary_reasoning: [
        {
          factor: 'weather',
          assessment: 'Perfect temperature',
          positive: true,
        },
      ],
      personalized_summary: 'Great time to visit!',
      alternative_options: [],
      rejected_periods: [],
    };

    travelAgentService.getRecommendation.mockResolvedValue(mockRecommendation);

    render(<App />);

    const textarea = screen.getByLabelText(/travel query/i);
    const submitButton = screen.getByRole('button', { name: /get recommendation/i });

    // Submit form
    textarea.value = 'Is it a good time to go to Maui?';
    submitButton.click();

    // Should show recommendation
    await waitFor(() => {
      expect(screen.getByText(/your personalized recommendation/i)).toBeInTheDocument();
      expect(screen.getByText(/great time to visit/i)).toBeInTheDocument();
    });
  });
});
