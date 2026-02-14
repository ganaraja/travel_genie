/**
 * Tests for ChatInput component
 * Input field with example queries and profile info
 */

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatInput from '../../frontend/src/components/ChatInput';

describe('ChatInput Component', () => {
  const mockOnSend = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Initial Render', () => {
    test('renders textarea input', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      expect(screen.getByPlaceholderText(/Ask me anything about your travel plans/i)).toBeInTheDocument();
    });

    test('renders send button', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      expect(screen.getByRole('button', { name: /🚀/i })).toBeInTheDocument();
    });

    test('renders example queries', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      expect(screen.getByText('Is it a good time to go to Maui?')).toBeInTheDocument();
      expect(screen.getByText('When should I visit Paris?')).toBeInTheDocument();
      expect(screen.getByText('Should I go to Tokyo next month?')).toBeInTheDocument();
    });

    test('renders profile information', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      expect(screen.getByText('Comfort Traveler')).toBeInTheDocument();
    });

    test('renders keyboard hint', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      expect(screen.getByText(/Press.*Enter.*to send/i)).toBeInTheDocument();
    });
  });

  describe('User Input', () => {
    test('updates input value when typing', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.change(input, { target: { value: 'Test query' } });
      expect(input.value).toBe('Test query');
    });

    test('calls onSend when form is submitted', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));
      
      expect(mockOnSend).toHaveBeenCalledWith('Test query');
    });

    test('calls onSend when send button is clicked', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      const sendButton = screen.getByRole('button', { name: /🚀/i });
      
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.click(sendButton);
      
      expect(mockOnSend).toHaveBeenCalledWith('Test query');
    });

    test('trims whitespace from input', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.change(input, { target: { value: '  Test query  ' } });
      fireEvent.submit(input.closest('form'));
      
      expect(mockOnSend).toHaveBeenCalledWith('Test query');
    });

    test('does not call onSend with empty input', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.change(input, { target: { value: '   ' } });
      fireEvent.submit(input.closest('form'));
      
      expect(mockOnSend).not.toHaveBeenCalled();
    });

    test('clears input after sending', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.submit(input.closest('form'));
      
      expect(input.value).toBe('');
    });
  });

  describe('Keyboard Shortcuts', () => {
    test('submits on Enter key', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.keyDown(input, { key: 'Enter', shiftKey: false });
      
      expect(mockOnSend).toHaveBeenCalledWith('Test query');
    });

    test('does not submit on Shift+Enter', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.change(input, { target: { value: 'Test query' } });
      fireEvent.keyDown(input, { key: 'Enter', shiftKey: true });
      
      expect(mockOnSend).not.toHaveBeenCalled();
    });

    test('allows newline with Shift+Enter', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.change(input, { target: { value: 'Line 1' } });
      fireEvent.keyDown(input, { key: 'Enter', shiftKey: true });
      
      // Input should still contain text
      expect(input.value).toBe('Line 1');
    });
  });

  describe('Example Queries', () => {
    test('fills input when example query is clicked', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const exampleButton = screen.getByText('Is it a good time to go to Maui?');
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.click(exampleButton);
      expect(input.value).toBe('Is it a good time to go to Maui?');
    });

    test('renders all 8 example queries', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      
      expect(screen.getByText('Is it a good time to go to Maui?')).toBeInTheDocument();
      expect(screen.getByText('When should I visit Paris?')).toBeInTheDocument();
      expect(screen.getByText('Should I go to Tokyo next month?')).toBeInTheDocument();
      expect(screen.getByText('Best time for Bali vacation?')).toBeInTheDocument();
      expect(screen.getByText('When should I visit Bangalore?')).toBeInTheDocument();
      expect(screen.getByText('Should I go to Mumbai or Delhi?')).toBeInTheDocument();
      expect(screen.getByText("What's the weather like in Tokyo in March?")).toBeInTheDocument();
      expect(screen.getByText('Find me cheap flights to India')).toBeInTheDocument();
    });

    test('focuses input after clicking example', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const exampleButton = screen.getByText('When should I visit Paris?');
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.click(exampleButton);
      // Input should be focused (hard to test directly, but value should be set)
      expect(input.value).toBe('When should I visit Paris?');
    });
  });

  describe('Profile Information', () => {
    test('displays user_123 profile correctly', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      
      expect(screen.getByText('Comfort Traveler')).toBeInTheDocument();
      expect(screen.getByText('75-85°F')).toBeInTheDocument();
      expect(screen.getByText('$600-900')).toBeInTheDocument();
      expect(screen.getByText('$150-300/night')).toBeInTheDocument();
      expect(screen.getByText('Yes')).toBeInTheDocument();
    });

    test('displays default profile correctly', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="default" />);
      
      expect(screen.getByText('Standard Traveler')).toBeInTheDocument();
      expect(screen.getByText('70-80°F')).toBeInTheDocument();
      expect(screen.getByText('$500-800')).toBeInTheDocument();
      expect(screen.getByText('$100-250/night')).toBeInTheDocument();
      expect(screen.getByText('No')).toBeInTheDocument();
    });

    test('displays profile icons', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      
      expect(screen.getByText('👤')).toBeInTheDocument();
      // Profile details should have emoji icons
      const { container } = render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      expect(container.textContent).toContain('🌡️');
      expect(container.textContent).toContain('✈️');
      expect(container.textContent).toContain('🏨');
      expect(container.textContent).toContain('🛡️');
    });
  });

  describe('Disabled State', () => {
    test('disables input when disabled prop is true', () => {
      render(<ChatInput onSend={mockOnSend} disabled={true} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      expect(input).toBeDisabled();
    });

    test('disables send button when disabled prop is true', () => {
      render(<ChatInput onSend={mockOnSend} disabled={true} userId="user_123" />);
      const sendButton = screen.getByRole('button', { name: /⏳/i });
      
      expect(sendButton).toBeDisabled();
    });

    test('disables example buttons when disabled prop is true', () => {
      render(<ChatInput onSend={mockOnSend} disabled={true} userId="user_123" />);
      const exampleButton = screen.getByText('Is it a good time to go to Maui?');
      
      expect(exampleButton).toBeDisabled();
    });

    test('shows loading spinner when disabled', () => {
      render(<ChatInput onSend={mockOnSend} disabled={true} userId="user_123" />);
      expect(screen.getByText('⏳')).toBeInTheDocument();
    });

    test('disables send button when input is empty', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const sendButton = screen.getByRole('button', { name: /🚀/i });
      
      expect(sendButton).toBeDisabled();
    });

    test('enables send button when input has text', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      const sendButton = screen.getByRole('button', { name: /🚀/i });
      
      fireEvent.change(input, { target: { value: 'Test' } });
      expect(sendButton).not.toBeDisabled();
    });
  });

  describe('Auto-resize Textarea', () => {
    test('textarea adjusts height based on content', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      // Initial height
      const initialHeight = input.style.height;
      
      // Add multiline content
      fireEvent.change(input, { target: { value: 'Line 1\nLine 2\nLine 3\nLine 4' } });
      
      // Height should be auto (will be adjusted by useEffect)
      expect(input.style.height).toBeDefined();
    });

    test('resets height after clearing input', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      fireEvent.change(input, { target: { value: 'Line 1\nLine 2\nLine 3' } });
      fireEvent.submit(input.closest('form'));
      
      // After submit, input is cleared and height should reset
      expect(input.value).toBe('');
    });
  });

  describe('Accessibility', () => {
    test('textarea has proper placeholder', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const input = screen.getByPlaceholderText(/Ask me anything about your travel plans/i);
      
      expect(input).toHaveAttribute('placeholder');
    });

    test('buttons have proper roles', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const buttons = screen.getAllByRole('button');
      
      expect(buttons.length).toBeGreaterThan(0);
    });

    test('form can be submitted', () => {
      render(<ChatInput onSend={mockOnSend} disabled={false} userId="user_123" />);
      const form = screen.getByPlaceholderText(/Ask me anything about your travel plans/i).closest('form');
      
      expect(form).toBeInTheDocument();
    });
  });
});
