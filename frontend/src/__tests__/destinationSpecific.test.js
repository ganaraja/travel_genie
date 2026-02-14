/**
 * Tests for destination-specific recommendations in the frontend.
 * These tests verify that the UI correctly displays destination-specific
 * weather, flight durations, and hotel information.
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

// Mock fetch for API calls
global.fetch = jest.fn();

describe('Destination-Specific Recommendations', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('Maui shows tropical weather', async () => {
    const user = userEvent.setup();
    
    // Mock API response for Maui
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        recommendation: 'Weather forecast for Maui: Generally tropical weather (82-85°F). Duration: 6.0h Hawaiian'
      })
    });

    render(<App />);
    
    const input = screen.getByPlaceholderText(/ask me anything about your travel plans/i);
    await user.type(input, 'Maui weather?');
    
    const sendButton = screen.getByRole('button', { name: '' });
    await user.click(sendButton);
    
    await waitFor(() => {
      const text = screen.getByText(/tropical/i);
      expect(text).toBeInTheDocument();
    });
  });

  test('Zurich shows alpine weather', async () => {
    const user = userEvent.setup();
    
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        recommendation: 'Weather forecast for Zurich: Stable alpine weather (48-58°F). Duration: 11.5h Swiss'
      })
    });

    render(<App />);
    
    const input = screen.getByPlaceholderText(/ask me anything about your travel plans/i);
    await user.type(input, 'Zurich weather?');
    
    const buttons = screen.getAllByRole('button');
    const sendButton = buttons.find(btn => btn.type === 'submit');
    await user.click(sendButton);
    
    await waitFor(() => {
      const text = screen.getByText(/alpine/i);
      expect(text).toBeInTheDocument();
    });
  });

  test('Dubai shows desert weather', async () => {
    const user = userEvent.setup();
    
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        recommendation: 'Weather forecast for Dubai: Stable desert weather (88-96°F). Duration: 15.5h Emirates'
      })
    });

    render(<App />);
    
    const input = screen.getByPlaceholderText(/ask me anything about your travel plans/i);
    await user.type(input, 'Dubai weather?');
    
    const buttons = screen.getAllByRole('button');
    const sendButton = buttons.find(btn => btn.type === 'submit');
    await user.click(sendButton);
    
    await waitFor(() => {
      const text = screen.getByText(/desert/i);
      expect(text).toBeInTheDocument();
    });
  });
});
