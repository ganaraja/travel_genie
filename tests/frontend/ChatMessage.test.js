/**
 * Tests for ChatMessage component
 * Displays individual chat messages with formatting
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatMessage from '../../frontend/src/components/ChatMessage';

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

    test('displays user avatar', () => {
      const message = {
        id: 1,
        type: 'user',
        content: 'Test message',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.user-avatar')).toBeInTheDocument();
      expect(screen.getByText('👤')).toBeInTheDocument();
    });

    test('formats timestamp correctly', () => {
      const timestamp = new Date('2024-01-15T14:30:00').toISOString();
      const message = {
        id: 1,
        type: 'user',
        content: 'Test message',
        timestamp
      };

      render(<ChatMessage message={message} />);
      // Should display time in format like "2:30 PM"
      expect(screen.getByText(/\d{1,2}:\d{2}\s*(AM|PM)/i)).toBeInTheDocument();
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

    test('displays assistant avatar', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: 'Test response',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.assistant-avatar')).toBeInTheDocument();
      expect(screen.getByText('🌴')).toBeInTheDocument();
    });

    test('parses and displays visa information', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: `🛂 VISA REQUIREMENTS
No visa required for USA citizens
        
🌤️ WEATHER ANALYSIS
Perfect weather conditions`,
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/No visa required for USA citizens/i)).toBeInTheDocument();
    });

    test('parses and displays weather information', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: `🌤️ WEATHER ANALYSIS
Temperature: 75-85°F
Sunny conditions expected`,
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/Temperature: 75-85°F/i)).toBeInTheDocument();
    });

    test('parses and displays flight information', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: `✈️ FLIGHT OPTIONS (5 found)
Price range: $550 - $800
Best option: United - $580`,
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/Price range: \$550 - \$800/i)).toBeInTheDocument();
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

3. Hawaiian - $459 ✓ Within budget
   Departure: 2026-02-24 at 23:45
   Return: 2026-03-03 at 14:20
   Duration: 6.0h, Layovers: 0

🏨 HOTEL OPTIONS (6 found)`,
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      // Should capture the full flight section including Top 3
      expect(screen.getByText(/📋 Top 3 Flight Options:/i)).toBeInTheDocument();
      expect(screen.getByText(/Hawaiian - \$382/i)).toBeInTheDocument();
      expect(screen.getByText(/Duration: 6\.0h, Layovers: 0/i)).toBeInTheDocument();
    });

    test('parses and displays hotel information', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: `🏨 HOTEL OPTIONS (6 found)
Nightly rate range: $150 - $300
Best match: Marriott Maui - $220/night`,
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/Nightly rate range: \$150 - \$300/i)).toBeInTheDocument();
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
      // Should capture the full hotel section including Top 3
      expect(screen.getByText(/📋 Top 3 Hotel Options:/i)).toBeInTheDocument();
      expect(screen.getByText(/Marriott Bangalore - \$86\/night/i)).toBeInTheDocument();
      expect(screen.getByText(/Rating: 3\.0\/5\.0/i)).toBeInTheDocument();
      expect(screen.getByText(/Storm discount/i)).toBeInTheDocument();
    });

    test('highlights recommended sections', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: 'RECOMMENDED TRAVEL WINDOW\nDates: March 15-22',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.highlight-primary')).toBeInTheDocument();
    });

    test('highlights alternative sections', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: 'ALTERNATIVE OPTION\nDates: March 20-27',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.highlight-secondary')).toBeInTheDocument();
    });

    test('highlights warning sections', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: 'WHY NOT other periods:\nStorm risk detected',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.highlight-warning')).toBeInTheDocument();
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

    test('displays error icon', () => {
      const message = {
        id: 1,
        type: 'error',
        content: 'Error occurred',
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText('⚠️')).toBeInTheDocument();
    });

    test('displays "Error:" prefix', () => {
      const message = {
        id: 1,
        type: 'error',
        content: 'Something went wrong',
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/Error:/i)).toBeInTheDocument();
    });
  });

  describe('Content Parsing', () => {
    test('handles multiline content', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: 'Line 1\nLine 2\nLine 3',
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/Line 1/i)).toBeInTheDocument();
      expect(screen.getByText(/Line 2/i)).toBeInTheDocument();
      expect(screen.getByText(/Line 3/i)).toBeInTheDocument();
    });

    test('handles empty lines', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: 'Line 1\n\nLine 3',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      const brs = container.querySelectorAll('br');
      expect(brs.length).toBeGreaterThan(0);
    });

    test('handles special characters', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: 'Price: $500 • Temperature: 75°F • Rating: ⭐⭐⭐⭐⭐',
        timestamp: new Date().toISOString()
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/\$500/i)).toBeInTheDocument();
      expect(screen.getByText(/75°F/i)).toBeInTheDocument();
    });
  });

  describe('Info Cards', () => {
    test('renders visa info card when visa section present', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: '🛂 VISA REQUIREMENTS\nNo visa required',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.visa-card')).toBeInTheDocument();
    });

    test('renders weather info card when weather section present', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: '🌤️ WEATHER ANALYSIS\nSunny weather',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.weather-card')).toBeInTheDocument();
    });

    test('renders flight info card when flight section present', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: '✈️ FLIGHT OPTIONS\nMultiple flights available',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.flight-card')).toBeInTheDocument();
    });

    test('renders hotel info card when hotel section present', () => {
      const message = {
        id: 1,
        type: 'assistant',
        content: '🏨 HOTEL OPTIONS\nMany hotels available',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.hotel-card')).toBeInTheDocument();
    });

    test('does not render info cards for user messages', () => {
      const message = {
        id: 1,
        type: 'user',
        content: '🛂 VISA REQUIREMENTS\nTest',
        timestamp: new Date().toISOString()
      };

      const { container } = render(<ChatMessage message={message} />);
      expect(container.querySelector('.info-card')).not.toBeInTheDocument();
    });
  });

  describe('Timestamp Formatting', () => {
    test('formats morning time correctly', () => {
      const timestamp = new Date('2024-01-15T09:30:00').toISOString();
      const message = {
        id: 1,
        type: 'user',
        content: 'Test',
        timestamp
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/9:30\s*AM/i)).toBeInTheDocument();
    });

    test('formats afternoon time correctly', () => {
      const timestamp = new Date('2024-01-15T14:30:00').toISOString();
      const message = {
        id: 1,
        type: 'user',
        content: 'Test',
        timestamp
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/2:30\s*PM/i)).toBeInTheDocument();
    });

    test('formats midnight correctly', () => {
      const timestamp = new Date('2024-01-15T00:00:00').toISOString();
      const message = {
        id: 1,
        type: 'user',
        content: 'Test',
        timestamp
      };

      render(<ChatMessage message={message} />);
      expect(screen.getByText(/12:00\s*AM/i)).toBeInTheDocument();
    });
  });
});
