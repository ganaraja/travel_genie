import React, { useState, useRef, useEffect } from 'react';
import './ChatInput.css';

function ChatInput({ onSend, disabled, userId }) {
  const [input, setInput] = useState('');
  const textareaRef = useRef(null);

  const exampleQueries = [
    "Is it a good time to go to Maui?",
    "When should I visit Paris?",
    "Should I go to Tokyo next month?",
    "Best time for Bali vacation?",
    "When should I visit Bangalore?",
    "Should I go to Mumbai or Delhi?",
    "What's the weather like in Tokyo in March?",
    "Find me cheap flights to India"
  ];

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [input]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleExampleClick = (query) => {
    if (!disabled) {
      setInput(query);
      textareaRef.current?.focus();
    }
  };

  const getUserProfileInfo = () => {
    if (userId === 'user_123') {
      return {
        name: "Comfort Traveler",
        temp: "75-85°F",
        budget: "$600-900",
        hotels: "$150-300/night",
        safety: "Yes"
      };
    }
    return {
      name: "Standard Traveler",
      temp: "70-80°F",
      budget: "$500-800",
      hotels: "$100-250/night",
      safety: "No"
    };
  };

  const profile = getUserProfileInfo();

  return (
    <div className="chat-input-container">
      <div className="profile-info">
        <div className="profile-badge">
          <span className="profile-icon">👤</span>
          <span className="profile-name">{profile.name}</span>
        </div>
        <div className="profile-details">
          <span title="Temperature Preference">🌡️ {profile.temp}</span>
          <span title="Flight Budget">✈️ {profile.budget}</span>
          <span title="Hotel Budget">🏨 {profile.hotels}</span>
          <span title="Safety Conscious">🛡️ {profile.safety}</span>
        </div>
      </div>

      <div className="example-queries">
        {exampleQueries.map((query, index) => (
          <button
            key={index}
            className="example-chip"
            onClick={() => handleExampleClick(query)}
            disabled={disabled}
          >
            {query}
          </button>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <div className="input-wrapper">
          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask me anything about your travel plans... (Press Enter to send, Shift+Enter for new line)"
            disabled={disabled}
            className="message-input"
            rows="1"
          />
          <button
            type="submit"
            disabled={disabled || !input.trim()}
            className="send-button"
          >
            {disabled ? (
              <span className="button-spinner">⏳</span>
            ) : (
              <span className="button-icon">🚀</span>
            )}
          </button>
        </div>
        <div className="input-hint">
          Press <kbd>Enter</kbd> to send • <kbd>Shift + Enter</kbd> for new line
        </div>
      </form>
    </div>
  );
}

export default ChatInput;
