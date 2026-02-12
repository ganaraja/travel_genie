import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="LoadingSpinner">
      <div className="spinner"></div>
      <p className="loading-text">Analyzing your travel options...</p>
      <p className="loading-subtext">
        Our AI is checking weather patterns, flight availability, and hotel options to give you the best recommendation
      </p>
      
      <div className="loading-steps">
        <div className="loading-step">
          <span className="loading-step-icon">👤</span>
          <span>Retrieving your travel preferences</span>
        </div>
        <div className="loading-step">
          <span className="loading-step-icon">🌤️</span>
          <span>Analyzing weather forecasts</span>
        </div>
        <div className="loading-step">
          <span className="loading-step-icon">✈️</span>
          <span>Searching flight options</span>
        </div>
        <div className="loading-step">
          <span className="loading-step-icon">🏨</span>
          <span>Finding hotel matches</span>
        </div>
      </div>
    </div>
  );
}

export default LoadingSpinner;
