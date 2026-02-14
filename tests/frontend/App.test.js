/**
 * Tests for App component
 * Main application component with chat interface
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../../frontend/src/App';
import { travelAgentService } from '../../frontend/src/services/travelAgentService';

// Mock the travel agent service
jest.mock('../../frontend/src/services/travelAgentService');

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Initial Render', () => {
    test('renders Travel Genie header', () => {
      render(<App />);
      expect(screen.getByText('Travel Genie')).toBeInTheDocument();
    });

    test('renders AI-Powered Travel Planning subtitle', () => {
      render(<App />);
      expect(screen.getByText('AI-Powered Travel Planning')).toBeInTheDocument();
    });

    test('renders welcome banner', () => {
      render(<App />);
      expect(screen.getByText(/Plan Your Perfect Trip with AI/i)).toBeInTheDocument();
    });

    test('renders feature grid with 4 features', () => {
      render(<App />);
      expect(screen.getByText('Visa Checking')).toBeInTheDocument();
      expect(screen.getByText('Weather Analysis')).toBeInTheDocument();
      expect(screen.getByText('Flight Deals')).toBeInTheDocument();
      expect(screen.getByText('Hotel Matches')).toBeInTheDocument();
    });

    test('renders user profile selector', () => {
      render(<App />);
      expect(screen.getByRole('combobox')).toBeInTheDocument();
    });

    test('renders clear chat button', () => {
      render(<App />);
      expect(screen.getByText(/Clear Chat/i)).toBeInTheDocument();
    });

    test('renders chat input component', () => {
      render(<App />);
      expect(screen.getByPlaceholderText(/Ask me anything about your travel plans/i)).toBeInTheDocument();
    });
  });

  describe('User Profile Selection', () => {
    test('defaults to user_123 profile', () => {
      render(<App />);
      const select = screen.getByRole('combobox');
      expect(select.value).toBe('user_123');
    });

    test('can switch to default profile', () => {
      render(<App />);
      const select = screen.getByRole('combobox');
      
      fireEvent.change(select, { target: { value: 'default' } });
      expect(select.value).toBe('default');
    });

    test('displays correct profile name for user_123', () => {
      render(<App />);
      expect(screen.getByText(/Comfort Traveler \(USA\)/i)).toBeInTheDocument();
    });

    test('displays correct profile name for default', () => {
      render(<App />);
      expect(screen.getByText(/Standard Traveler \(USA\)/i)).toBeInTheDocument();
    });
  });

  describe('Message Handling', () => {
    test('sends message when user submits query', async () => {
      const mockRecommendation = {
        query: 'Should I go to Maui?',
        userId: 'user_123',
        recommendation: 'Yes, Maui is great this time of year!',
        timestamp: new Date().toISOString()
      };

      travelAgentService.getRecommendation.mockResolvedValue(mockRecommendation);

      render(<App />);
      
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      const sendButton = screen.getByRole('button', { name: /🚀/i });

      fireEvent.change(input, { target: { value: 'Should I go to Maui?' } });
      fireEvent.click(sendButton);

      await waitFor(() => {
        expect(travelAgentService.getRecommendation).toHaveBeenCalledWith(
          'Should I go to Maui?',
          'user_123'
        );
      });
    });

    test('displays user message after sending', async () => {
      const mockRecommendation = {
        query: 'Test query',
        userId: 'user_123',
        recommendation: 'Test response',
        timestamp: new Date().toISOString()
      };

      travelAgentService.getRecommendation.mockResolvedValue(mockRecommendation);

      render(<App />);
      
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));

      await waitFor(() => {
        expect(screen.getByText('Test query')).toBeInTheDocument();
      });
    });

    test('displays assistant response after API call', async () => {
      const mockRecommendation = {
        query: 'Test query',
        userId: 'user_123',
        recommendation: 'Test response from AI',
        timestamp: new Date().toISOString()
      };

      travelAgentService.getRecommendation.mockResolvedValue(mockRecommendation);

      render(<App />);
      
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));

      await waitFor(() => {
        expect(screen.getByText('Test response from AI')).toBeInTheDocument();
      });
    });

    test('shows loading indicator while processing', async () => {
      const mockRecommendation = {
        query: 'Test query',
        userId: 'user_123',
        recommendation: 'Test response',
        timestamp: new Date().toISOString()
      };

      travelAgentService.getRecommendation.mockImplementation(
        () => new Promise(resolve => setTimeout(() => resolve(mockRecommendation), 100))
      );

      render(<App />);
      
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));

      expect(screen.getByText(/Analyzing your travel options/i)).toBeInTheDocument();

      await waitFor(() => {
        expect(screen.queryByText(/Analyzing your travel options/i)).not.toBeInTheDocument();
      });
    });

    test('displays error message on API failure', async () => {
      travelAgentService.getRecommendation.mockRejectedValue(
        new Error('API connection failed')
      );

      render(<App />);
      
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));

      await waitFor(() => {
        expect(screen.getByText(/API connection failed/i)).toBeInTheDocument();
      });
    });

    test('clears input after sending message', async () => {
      const mockRecommendation = {
        query: 'Test query',
        userId: 'user_123',
        recommendation: 'Test response',
        timestamp: new Date().toISOString()
      };

      travelAgentService.getRecommendation.mockResolvedValue(mockRecommendation);

      render(<App />);
      
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));

      await waitFor(() => {
        expect(input.value).toBe('');
      });
    });
  });

  describe('Clear Chat Functionality', () => {
    test('clears all messages except welcome banner', async () => {
      const mockRecommendation = {
        query: 'Test query',
        userId: 'user_123',
        recommendation: 'Test response',
        timestamp: new Date().toISOString()
      };

      travelAgentService.getRecommendation.mockResolvedValue(mockRecommendation);

      render(<App />);
      
      // Send a message
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));

      await waitFor(() => {
        expect(screen.getByText('Test query')).toBeInTheDocument();
      });

      // Clear chat
      const clearButton = screen.getByText(/Clear Chat/i);
      fireEvent.click(clearButton);

      // Welcome banner should still be there
      expect(screen.getByText(/Plan Your Perfect Trip with AI/i)).toBeInTheDocument();
      
      // User message should be gone
      expect(screen.queryByText('Test query')).not.toBeInTheDocument();
    });

    test('disables clear button while loading', async () => {
      const mockRecommendation = {
        query: 'Test query',
        userId: 'user_123',
        recommendation: 'Test response',
        timestamp: new Date().toISOString()
      };

      travelAgentService.getRecommendation.mockImplementation(
        () => new Promise(resolve => setTimeout(() => resolve(mockRecommendation), 100))
      );

      render(<App />);
      
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));

      const clearButton = screen.getByText(/Clear Chat/i).closest('button');
      expect(clearButton).toBeDisabled();

      await waitFor(() => {
        expect(clearButton).not.toBeDisabled();
      });
    });
  });

  describe('Auto-scroll Behavior', () => {
    test('scrolls to bottom when new message is added', async () => {
      const mockRecommendation = {
        query: 'Test query',
        userId: 'user_123',
        recommendation: 'Test response',
        timestamp: new Date().toISOString()
      };

      travelAgentService.getRecommendation.mockResolvedValue(mockRecommendation);

      const scrollIntoViewMock = jest.fn();
      Element.prototype.scrollIntoView = scrollIntoViewMock;

      render(<App />);
      
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));

      await waitFor(() => {
        expect(scrollIntoViewMock).toHaveBeenCalled();
      });
    });
  });

  describe('Accessibility', () => {
    test('has proper ARIA labels', () => {
      render(<App />);
      
      const select = screen.getByRole('combobox');
      expect(select).toBeInTheDocument();
      
      const buttons = screen.getAllByRole('button');
      expect(buttons.length).toBeGreaterThan(0);
    });

    test('keyboard navigation works', () => {
      render(<App />);
      
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      input.focus();
      expect(document.activeElement).toBe(input);
    });
  });
});
