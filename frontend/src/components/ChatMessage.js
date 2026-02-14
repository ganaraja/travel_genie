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
      flights: [],
      hotels: [],
      alternativeFlights: [],
      alternativeHotels: [],
      recommendation: text
    };

    // Try to extract visa information
    const visaMatch = text.match(/🛂 VISA[^\n]*\n([^\n]+(?:\n(?!🌤️|✈️|🏨)[^\n]+)*)/i);
    if (visaMatch) {
      sections.visa = visaMatch[1].trim();
    }

    // Try to extract weather information
    const weatherMatch = text.match(/🌤️ WEATHER ANALYSIS\s*\n([^\n]+(?:\n(?!✈️|🏨)[^\n]+)*)/i);
    if (weatherMatch) {
      sections.weather = weatherMatch[1].trim();
    }

    // Parse flight options - extract individual flights from Top 3
    const flightSectionMatch = text.match(/✈️ FLIGHT OPTIONS[^\n]*\n([\s\S]*?)(?=\n🏨 HOTEL OPTIONS|\n✨ RECOMMENDED|$)/i);
    if (flightSectionMatch) {
      const flightSection = flightSectionMatch[1];
      
      // Extract summary info
      const priceRangeMatch = flightSection.match(/Price range: \$(\d+) - \$(\d+)/);
      const withinBudgetMatch = flightSection.match(/Within soft budget[^\n]*: (\d+) options/);
      
      sections.flightSummary = {
        priceRange: priceRangeMatch ? `$${priceRangeMatch[1]} - $${priceRangeMatch[2]}` : null,
        withinBudget: withinBudgetMatch ? withinBudgetMatch[1] : null
      };
      
      // Extract individual flight options
      const flightPattern = /(\d+)\.\s+([^\n]+)\s+-\s+\$(\d+)\s+([^\n]*)\n\s+Departure:\s+([^\n]+)\n\s+Return:\s+([^\n]+)\n\s+Duration:\s+([^\n]+)/g;
      let match;
      while ((match = flightPattern.exec(flightSection)) !== null) {
        sections.flights.push({
          number: match[1],
          airline: match[2].trim(),
          price: match[3],
          badge: match[4].trim(),
          departure: match[5].trim(),
          return: match[6].trim(),
          duration: match[7].trim()
        });
      }
    }

    // Parse hotel options - extract individual hotels from Top 3
    const hotelSectionMatch = text.match(/🏨 HOTEL OPTIONS[^\n]*\n([\s\S]*?)(?=\n✨ RECOMMENDED|🔄 ALTERNATIVE|❌ WHY NOT|$)/i);
    if (hotelSectionMatch) {
      const hotelSection = hotelSectionMatch[1];
      
      // Extract summary info
      const rateRangeMatch = hotelSection.match(/Nightly rate range: \$(\d+) - \$(\d+)/);
      const withinBudgetMatch = hotelSection.match(/Within your budget: (\d+) options/);
      
      sections.hotelSummary = {
        rateRange: rateRangeMatch ? `$${rateRangeMatch[1]} - $${rateRangeMatch[2]}` : null,
        withinBudget: withinBudgetMatch ? withinBudgetMatch[1] : null
      };
      
      // Extract individual hotel options
      const hotelPattern = /(\d+)\.\s+([^\n]+)\s+-\s+\$(\d+)\/night\s+([^\n]*)\n\s+Rating:\s+([^\n]+)\n\s+Total for[^\n]+:\s+\$(\d+)(?:\n\s+💰\s+([^\n]+))?/g;
      let match;
      while ((match = hotelPattern.exec(hotelSection)) !== null) {
        sections.hotels.push({
          number: match[1],
          name: match[2].trim(),
          rate: match[3],
          badges: match[4].trim(),
          rating: match[5].trim(),
          total: match[6],
          special: match[7] ? match[7].trim() : null
        });
      }
    }

    // Parse alternative options
    const altSectionMatch = text.match(/🔄 ALTERNATIVE OPTION\s*\n([\s\S]*?)(?=\n❌ WHY NOT|💬 Feel free|$)/i);
    if (altSectionMatch) {
      const altSection = altSectionMatch[1];
      
      // Parse alternative flight
      const altFlightPattern = /📋 Alternative Flight:\s*\n\s*(\d+)\.\s+([^\n]+)\s+-\s+\$(\d+)\s+([^\n]*)\n\s+Departure:\s+([^\n]+)\n\s+Return:\s+([^\n]+)\n\s+Duration:\s+([^\n]+)\n\s+Reason:\s+([^\n]+)/;
      const altFlightMatch = altSection.match(altFlightPattern);
      if (altFlightMatch) {
        sections.alternativeFlights.push({
          number: altFlightMatch[1],
          airline: altFlightMatch[2].trim(),
          price: altFlightMatch[3],
          badge: altFlightMatch[4].trim(),
          departure: altFlightMatch[5].trim(),
          return: altFlightMatch[6].trim(),
          duration: altFlightMatch[7].trim(),
          reason: altFlightMatch[8].trim()
        });
      }
      
      // Parse alternative hotel
      const altHotelPattern = /📋 Alternative Hotel:\s*\n\s*(\d+)\.\s+([^\n]+)\s+-\s+\$(\d+)\/night\s+([^\n]*)\n\s+Rating:\s+([^\n]+)\n\s+Total for[^\n]+:\s+\$(\d+)(?:\n\s+💰\s+([^\n]+))?/;
      const altHotelMatch = altSection.match(altHotelPattern);
      if (altHotelMatch) {
        sections.alternativeHotels.push({
          number: altHotelMatch[1],
          name: altHotelMatch[2].trim(),
          rate: altHotelMatch[3],
          badges: altHotelMatch[4].trim(),
          rating: altHotelMatch[5].trim(),
          total: altHotelMatch[6],
          special: altHotelMatch[7] ? altHotelMatch[7].trim() : null
        });
      }
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
      <div className="message-avatar assistant-avatar">
        <img src="/travel-icon.svg" alt="Travel" />
      </div>
      <div className="message-content">
        <div className="message-bubble">
          {/* Main recommendation text */}
          <div className="recommendation-text">
            {content.split('\n').map((line, index) => {
              if (!line.trim()) return <br key={index} />;
              
              // Skip flight and hotel sections that are displayed in cards
              if (line.includes('✈️ FLIGHT OPTIONS') || 
                  line.includes('📋 Top 3 Flight Options') ||
                  line.includes('🏨 HOTEL OPTIONS') ||
                  line.includes('📋 Top 3 Hotel Options') ||
                  line.includes('📋 Alternative Flight') ||
                  line.includes('📋 Alternative Hotel')) {
                return null;
              }
              
              // Skip detail lines that are part of flight/hotel cards
              if (line.match(/^\s*\d+\.\s+\w+.*-\s+\$\d+/) || // Flight/hotel option lines
                  line.match(/^\s+Departure:/) ||
                  line.match(/^\s+Return:/) ||
                  line.match(/^\s+Duration:/) ||
                  line.match(/^\s+Rating:/) ||
                  line.match(/^\s+Total for/) ||
                  line.match(/^\s+Reason:/) ||
                  line.match(/^\s+💰/)) {
                return null;
              }
              
              // Skip summary lines that are in the section headers
              if (line.match(/^Price range:/) ||
                  line.match(/^Within soft budget/) ||
                  line.match(/^Nightly rate range:/) ||
                  line.match(/^Within your budget:/) ||
                  line.match(/^Preferred brands available:/)) {
                return null;
              }
              
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
          {(sections?.visa || sections?.weather || sections?.flights?.length > 0 || sections?.hotels?.length > 0) && (
            <div className="info-cards-container">
              {sections.visa && (
                <div className="info-card-row visa-card">
                  <div className="card-icon">🛂</div>
                  <div className="card-content">
                    <div className="card-title">Visa & Entry Requirements</div>
                    <div className="card-text">{sections.visa}</div>
                  </div>
                </div>
              )}
              
              {sections.weather && (
                <div className="info-card-row weather-card">
                  <div className="card-icon">🌤️</div>
                  <div className="card-content">
                    <div className="card-title">Weather Forecast</div>
                    <div className="card-text">{sections.weather}</div>
                  </div>
                </div>
              )}
              
              {sections.flights?.length > 0 && (
                <div className="options-section">
                  <div className="section-header">
                    <span className="section-icon">✈️</span>
                    <h4 className="section-title">Top Flight Options</h4>
                    {sections.flightSummary?.priceRange && (
                      <span className="section-badge">{sections.flightSummary.priceRange}</span>
                    )}
                  </div>
                  <div className="options-grid">
                    {sections.flights.map((flight, idx) => (
                      <div key={idx} className="option-card flight-option">
                        <div className="option-header">
                          <div className="option-number">#{flight.number}</div>
                          <div className="option-main">
                            <div className="option-title">{flight.airline}</div>
                            <div className="option-badges">
                              {flight.badge.includes('✓') && <span className="badge badge-success">Within Budget</span>}
                              {flight.badge.includes('⚠️') && <span className="badge badge-warning">Over Budget</span>}
                            </div>
                          </div>
                          <div className="option-price">${flight.price}</div>
                        </div>
                        <div className="option-details">
                          <div className="detail-row">
                            <span className="detail-label">🛫 Departure:</span>
                            <span className="detail-value">{flight.departure}</span>
                          </div>
                          <div className="detail-row">
                            <span className="detail-label">🛬 Return:</span>
                            <span className="detail-value">{flight.return}</span>
                          </div>
                          <div className="detail-row">
                            <span className="detail-label">⏱️ Duration:</span>
                            <span className="detail-value">{flight.duration}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {sections.hotels?.length > 0 && (
                <div className="options-section">
                  <div className="section-header">
                    <span className="section-icon">🏨</span>
                    <h4 className="section-title">Top Hotel Options</h4>
                    {sections.hotelSummary?.rateRange && (
                      <span className="section-badge">{sections.hotelSummary.rateRange}/night</span>
                    )}
                  </div>
                  <div className="options-grid">
                    {sections.hotels.map((hotel, idx) => (
                      <div key={idx} className="option-card hotel-option">
                        <div className="option-header">
                          <div className="option-number">#{hotel.number}</div>
                          <div className="option-main">
                            <div className="option-title">{hotel.name}</div>
                            <div className="option-badges">
                              {hotel.badges.includes('✓') && <span className="badge badge-success">Within Budget</span>}
                              {hotel.badges.includes('⚠️') && <span className="badge badge-warning">Outside Budget</span>}
                              {hotel.badges.includes('⭐') && <span className="badge badge-star">Preferred</span>}
                            </div>
                          </div>
                          <div className="option-price">${hotel.rate}<span className="price-unit">/night</span></div>
                        </div>
                        <div className="option-details">
                          <div className="detail-row">
                            <span className="detail-label">⭐ Rating:</span>
                            <span className="detail-value">{hotel.rating}</span>
                          </div>
                          <div className="detail-row">
                            <span className="detail-label">💰 Total:</span>
                            <span className="detail-value">${hotel.total}</span>
                          </div>
                          {hotel.special && (
                            <div className="detail-row special">
                              <span className="detail-label">💡</span>
                              <span className="detail-value">{hotel.special}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              
              {(sections.alternativeFlights?.length > 0 || sections.alternativeHotels?.length > 0) && (
                <div className="options-section alternative-section">
                  <div className="section-header">
                    <span className="section-icon">🔄</span>
                    <h4 className="section-title">Alternative Options</h4>
                  </div>
                  
                  {sections.alternativeFlights?.length > 0 && (
                    <div className="options-grid">
                      {sections.alternativeFlights.map((flight, idx) => (
                        <div key={idx} className="option-card flight-option alternative-card">
                          <div className="option-header">
                            <div className="option-number">#{flight.number}</div>
                            <div className="option-main">
                              <div className="option-title">{flight.airline}</div>
                              <div className="option-badges">
                                {flight.badge.includes('✓') && <span className="badge badge-success">Within Budget</span>}
                                {flight.badge.includes('⚠️') && <span className="badge badge-warning">Over Budget</span>}
                              </div>
                            </div>
                            <div className="option-price">${flight.price}</div>
                          </div>
                          <div className="option-details">
                            <div className="detail-row">
                              <span className="detail-label">🛫 Departure:</span>
                              <span className="detail-value">{flight.departure}</span>
                            </div>
                            <div className="detail-row">
                              <span className="detail-label">🛬 Return:</span>
                              <span className="detail-value">{flight.return}</span>
                            </div>
                            <div className="detail-row">
                              <span className="detail-label">⏱️ Duration:</span>
                              <span className="detail-value">{flight.duration}</span>
                            </div>
                            {flight.reason && (
                              <div className="detail-row special">
                                <span className="detail-label">💡 Reason:</span>
                                <span className="detail-value">{flight.reason}</span>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  {sections.alternativeHotels?.length > 0 && (
                    <div className="options-grid">
                      {sections.alternativeHotels.map((hotel, idx) => (
                        <div key={idx} className="option-card hotel-option alternative-card">
                          <div className="option-header">
                            <div className="option-number">#{hotel.number}</div>
                            <div className="option-main">
                              <div className="option-title">{hotel.name}</div>
                              <div className="option-badges">
                                {hotel.badges.includes('✓') && <span className="badge badge-success">Within Budget</span>}
                                {hotel.badges.includes('⚠️') && <span className="badge badge-warning">Outside Budget</span>}
                                {hotel.badges.includes('⭐') && <span className="badge badge-star">Preferred</span>}
                              </div>
                            </div>
                            <div className="option-price">${hotel.rate}<span className="price-unit">/night</span></div>
                          </div>
                          <div className="option-details">
                            <div className="detail-row">
                              <span className="detail-label">⭐ Rating:</span>
                              <span className="detail-value">{hotel.rating}</span>
                            </div>
                            <div className="detail-row">
                              <span className="detail-label">💰 Total:</span>
                              <span className="detail-value">${hotel.total}</span>
                            </div>
                            {hotel.special && (
                              <div className="detail-row special">
                                <span className="detail-label">💡</span>
                                <span className="detail-value">{hotel.special}</span>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
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
