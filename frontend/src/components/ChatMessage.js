import React from 'react';
import './ChatMessage.css';

function ChatMessage({ message }) {
  const { type, content, timestamp } = message;
  
  const formatTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  };

  const parseContent = (text) => {
    // Parse the content to extract structured information
    const sections = {
      visa: null,
      weather: null,
      flights: null,
      hotels: null,
      recommendation: text
    };

    // Try to extract visa information
    const visaMatch = text.match(/🛂 VISA REQUIREMENTS\s*\n([^\n]+(?:\n(?!🌤️|✈️|🏨)[^\n]+)*)/i);
    if (visaMatch) {
      sections.visa = visaMatch[1].trim();
    }

    // Try to extract weather information
    const weatherMatch = text.match(/🌤️ WEATHER ANALYSIS\s*\n([^\n]+(?:\n(?!✈️|🏨)[^\n]+)*)/i);
    if (weatherMatch) {
      sections.weather = weatherMatch[1].trim();
    }

    // Try to extract flight information
    const flightMatch = text.match(/✈️ FLIGHT OPTIONS[^\n]*\n([^\n]+(?:\n(?!🏨|✨)[^\n]+)*)/i);
    if (flightMatch) {
      sections.flights = flightMatch[1].trim();
    }

    // Try to extract hotel information
    const hotelMatch = text.match(/🏨 HOTEL OPTIONS[^\n]*\n([^\n]+(?:\n(?!✨|🔄)[^\n]+)*)/i);
    if (hotelMatch) {
      sections.hotels = hotelMatch[1].trim();
    }

    return sections;
  };

  const sections = type === 'assistant' ? parseContent(content) : null;

  if (type === 'user') {
    return (
      <div className="message user-message">
        <div className="message-content">
          <div className="message-bubble">
            {content}
          </div>
          <div className="message-time">{formatTime(timestamp)}</div>
        </div>
        <div className="message-avatar user-avatar">👤</div>
      </div>
    );
  }

  if (type === 'error') {
    return (
      <div className="message assistant-message error-message">
        <div className="message-avatar assistant-avatar">⚠️</div>
        <div className="message-content">
          <div className="message-bubble error-bubble">
            <strong>Error:</strong> {content}
          </div>
          <div className="message-time">{formatTime(timestamp)}</div>
        </div>
      </div>
    );
  }

  // Assistant message with potential structured data
  return (
    <div className="message assistant-message">
      <div className="message-avatar assistant-avatar">🌴</div>
      <div className="message-content">
        <div className="message-bubble">
          {/* Main recommendation text */}
          <div className="recommendation-text">
            {content.split('\n').map((line, index) => {
              if (!line.trim()) return <br key={index} />;
              
              // Highlight important sections
              if (line.includes('Recommended') || line.includes('RECOMMENDED')) {
                return <p key={index} className="highlight-primary">{line}</p>;
              }
              if (line.includes('Alternative') || line.includes('ALTERNATIVE')) {
                return <p key={index} className="highlight-secondary">{line}</p>;
              }
              if (line.includes('Why not') || line.includes('WHY NOT')) {
                return <p key={index} className="highlight-warning">{line}</p>;
              }
              
              return <p key={index}>{line}</p>;
            })}
          </div>

          {/* Info cards for structured data */}
          {(sections?.visa || sections?.weather || sections?.flights || sections?.hotels) && (
            <div className="info-cards">
              {sections.visa && (
                <div className="info-card visa-card">
                  <div className="card-icon">🛂</div>
                  <div className="card-content">
                    <div className="card-title">Visa Requirements</div>
                    <div className="card-text">{sections.visa}</div>
                  </div>
                </div>
              )}
              {sections.weather && (
                <div className="info-card weather-card">
                  <div className="card-icon">🌤️</div>
                  <div className="card-content">
                    <div className="card-title">Weather</div>
                    <div className="card-text">{sections.weather}</div>
                  </div>
                </div>
              )}
              {sections.flights && (
                <div className="info-card flight-card">
                  <div className="card-icon">✈️</div>
                  <div className="card-content">
                    <div className="card-title">Flights</div>
                    <div className="card-text">{sections.flights}</div>
                  </div>
                </div>
              )}
              {sections.hotels && (
                <div className="info-card hotel-card">
                  <div className="card-icon">🏨</div>
                  <div className="card-content">
                    <div className="card-title">Hotels</div>
                    <div className="card-text">{sections.hotels}</div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
        <div className="message-time">{formatTime(timestamp)}</div>
      </div>
    </div>
  );
}

export default ChatMessage;
