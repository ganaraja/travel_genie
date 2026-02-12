import React, { useState } from 'react';
import './TravelQueryForm.css';

function TravelQueryForm({ onSubmit, disabled }) {
  const [query, setQuery] = useState('');
  const [userId, setUserId] = useState('user_123');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !disabled) {
      onSubmit(query.trim(), userId);
    }
  };

  const exampleQueries = [
    "Is it a good time to go to Maui?",
    "When should I visit Paris?",
    "Best time to travel to Tokyo from San Francisco?",
    "Should I go to Bali next month?"
  ];

  const handleExampleClick = (exampleQuery) => {
    if (!disabled) {
      setQuery(exampleQuery);
    }
  };

  const getUserProfileDescription = () => {
    if (userId === 'user_123') {
      return "Comfort traveler, safety-conscious, prefers 75-85°F, budget $600-900 flights, $150-300/night hotels";
    }
    return "Standard traveler, prefers 70-80°F, budget $500-800 flights, $100-250/night hotels";
  };

  return (
    <form className="TravelQueryForm" onSubmit={handleSubmit}>
      <div className="form-header">
        <h3>🗺️ Plan Your Next Adventure</h3>
        <p>Tell us where you want to go, and we'll help you find the perfect time</p>
      </div>

      <div className="form-grid">
        <div className="form-group">
          <label htmlFor="userId">
            👤 Traveler Profile
          </label>
          <select
            id="userId"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            disabled={disabled}
            className="form-select"
          >
            <option value="user_123">Comfort Traveler</option>
            <option value="default">Standard Traveler</option>
          </select>
          <div className="user-profile-info">
            {getUserProfileDescription()}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="query">
            💬 Your Travel Question
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything about your travel plans... For example: 'Is it a good time to go to Maui?' or 'When should I visit Paris?'"
            disabled={disabled}
            className="form-textarea"
            rows="4"
            required
          />
        </div>
      </div>

      <button
        type="submit"
        disabled={disabled || !query.trim()}
        className="submit-button"
      >
        {disabled ? '✨ Getting Your Recommendation...' : '🔍 Get Travel Recommendation'}
      </button>

      <div className="example-queries">
        <h4>💡 Try these example questions:</h4>
        <div className="example-buttons">
          {exampleQueries.map((exampleQuery, index) => (
            <button
              key={index}
              type="button"
              className="example-button"
              onClick={() => handleExampleClick(exampleQuery)}
              disabled={disabled}
            >
              {exampleQuery}
            </button>
          ))}
        </div>
      </div>
    </form>
  );
}

export default TravelQueryForm;
