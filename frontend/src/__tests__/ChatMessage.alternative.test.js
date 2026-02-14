/**
 * Tests for ChatMessage component - Alternative Options
 * Tests the parsing and display of alternative flight and hotel options
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatMessage from '../components/ChatMessage';

describe('ChatMessage Component - Alternative Options', () => {
  test('parses and displays alternative flight and hotel options', () => {
    const message = {
      id: 1,
      type: 'assistant',
      content: `Based on your travel preferences, here's my analysis:

✈️ FLIGHT OPTIONS (10 found)
Price range: $382 - $620
Within soft budget ($600): 9 options

📋 Top 3 Flight Options:

1. Hawaiian - $382 ✓ Within budget
   Departure: 2026-02-23 at 23:45
   Return: 2026-03-02 at 14:20
   Duration: 6.0h, Layovers: 0

🏨 HOTEL OPTIONS (6 found)
Nightly rate range: $86 - $320
Within your budget: 3 options

📋 Top 3 Hotel Options:

1. Marriott Bangalore - $86/night ⚠️ Outside budget ⭐ Preferred brand
   Rating: 3.0/5.0
   Total for 7 nights: $598

🔄 ALTERNATIVE OPTION

📋 Alternative Flight:

1. United - $450 ✓ Within budget
   Departure: 2026-02-24 at 08:30
   Return: 2026-03-03 at 14:20
   Duration: 8.5h, Layovers: 1
   Reason: Different dates for flexibility

📋 Alternative Hotel:

1. Hilton Bangalore - $114/night ⚠️ Outside budget ⭐ Preferred brand
   Rating: 3.4/5.0
   Total for 7 nights: $798

💬 Feel free to ask follow-up questions`,
      timestamp: new Date().toISOString()
    };

    render(<ChatMessage message={message} />);
    
    // Check for alternative section header
    const altHeader = screen.getByText(/Alternative Options/i);
    expect(altHeader).toBeInTheDocument();
    
    // Check for alternative flight details in card
    const unitedElements = screen.getAllByText(/United/i);
    expect(unitedElements.length).toBeGreaterThan(0);
    
    // Check for alternative hotel details in card
    const hiltonElements = screen.getAllByText(/Hilton Bangalore/i);
    expect(hiltonElements.length).toBeGreaterThan(0);
    
    // Check for reason field
    const reasonElements = screen.getAllByText(/Different dates for flexibility/i);
    expect(reasonElements.length).toBeGreaterThan(0);
  });

  test('does not display alternative section when no alternatives exist', () => {
    const message = {
      id: 1,
      type: 'assistant',
      content: `Based on your travel preferences:

✈️ FLIGHT OPTIONS (10 found)
Price range: $382 - $620

📋 Top 3 Flight Options:

1. Hawaiian - $382 ✓ Within budget
   Departure: 2026-02-23 at 23:45
   Return: 2026-03-02 at 14:20
   Duration: 6.0h, Layovers: 0

💬 Feel free to ask follow-up questions`,
      timestamp: new Date().toISOString()
    };

    render(<ChatMessage message={message} />);
    
    // Alternative section should not exist
    const altHeaders = screen.queryAllByText(/Alternative Options/i);
    expect(altHeaders.length).toBe(0);
  });
});
