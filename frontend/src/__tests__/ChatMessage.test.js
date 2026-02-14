/**
 * Tests for ChatMessage component
 * Displays individual chat messages with formatting
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatMessage from '../components/ChatMessage';

describe('ChatMessage Component', () => {
  describe('User Messages', () => {
    test('renders user message with correct styling', () => {
      const message = {
        id: 1,
        type: 'user',
        content: 'Should I go to Maui?',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(screen.getByText('Should I go to Maui?')).toBeInTheDocument();
      expect(container.querySelector('.user-message')).toBeInTheDocument();
    });
  });

  describe('Assistant Messages', () => {
    test('renders assistant message with correct styling', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: 'Yes, Maui is great this time of year!',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(screen.getByText('Yes, Maui is great this time of year!')).toBeInTheDocument();
      expect(container.querySelector('.assistant-message')).toBeInTheDocument();
    });

    test('parses and displays detailed flight options with Top 3 section', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: `✈️ FLIGHT OPTIONS (10 found)
Price range: $382 - $620
Within soft budget ($600): 9 options

📋 Top 3 Flight Options:

1. Hawaiian - $382 ✓ Within budget
   Departure: 2026-02-23 at 23:45
   Return: 2026-03-02 at 14:20
   Duration: 6.0h, Layovers: 0

2. United - $450 ✓ Within budget
   Departure: 2026-02-23 at 08:30
   Return: 2026-03-02 at 14:20
   Duration: 8.5h, Layovers: 1

🏨 HOTEL OPTIONS (6 found)`,
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      // Check for the section header (not the raw text which is now filtered)
      const topFlightHeader = screen.getByText(/Top Flight Options/i);
      expect(topFlightHeader).toBeInTheDocument();
      
      // Check for flight details in cards
      const hawaiianElements = screen.getAllByText(/Hawaiian/i);
      expect(hawaiianElements.length).toBeGreaterThan(0);
      const durationElements = screen.getAllByText(/6\.0h, Layovers: 0/i);
      expect(durationElements.length).toBeGreaterThan(0);
    });

    test('parses and displays detailed hotel options with Top 3 section', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: `🏨 HOTEL OPTIONS (6 found)
Nightly rate range: $86 - $320
Within your budget: 3 options
Preferred brands available: 0 options

📋 Top 3 Hotel Options:

1. Marriott Bangalore - $86/night ⚠️ Outside budget ⭐ Preferred brand
   Rating: 3.0/5.0
   Total for 7 nights: $598
   💰 Storm discount - reduced rates due to weather forecast

2. Hilton Bangalore - $114/night ⚠️ Outside budget ⭐ Preferred brand
   Rating: 3.4/5.0
   Total for 7 nights: $798

3. Hyatt Bangalore - $200/night ✓ Within budget
   Rating: 3.8/5.0
   Total for 7 nights: $1400

✨ RECOMMENDED TRAVEL WINDOW`,
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      // Check for the section header (not the raw text which is now filtered)
      const topHotelHeader = screen.getByText(/Top Hotel Options/i);
      expect(topHotelHeader).toBeInTheDocument();
      
      // Check for hotel details in cards
      const marriottElements = screen.getAllByText(/Marriott Bangalore/i);
      expect(marriottElements.length).toBeGreaterThan(0);
      const ratingElements = screen.getAllByText(/3\.0\/5\.0/i);
      expect(ratingElements.length).toBeGreaterThan(0);
      const discountElements = screen.getAllByText(/Storm discount/i);
      expect(discountElements.length).toBeGreaterThan(0);
    });
  });

  describe('Error Messages', () => {
    test('renders error message with correct styling', () => {
      const message = {
        id: 1,
        type: 'error',
        content: 'API connection failed',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(screen.getByText(/API connection failed/i)).toBeInTheDocument();
      expect(container.querySelector('.error-message')).toBeInTheDocument();
    });
  });
});
