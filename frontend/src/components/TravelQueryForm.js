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

  return (
    <form className="TravelQueryForm" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="userId">User ID:</label>
        <select
          id="userId"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          disabled={disabled}
          className="form-select"
        >
          <option value="user_123">User 123 (Comfort, Safety-conscious)</option>
          <option value="default">Default User (Standard)</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="query">Travel Query:</label>
        <textarea
          id="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., Is it a good time to go to Maui?"
          disabled={disabled}
          className="form-textarea"
          rows="3"
          required
        />
      </div>

      <button
        type="submit"
        disabled={disabled || !query.trim()}
        className="submit-button"
      >
        {disabled ? 'Getting Recommendation...' : 'Get Recommendation'}
      </button>
    </form>
  );
}

export default TravelQueryForm;
