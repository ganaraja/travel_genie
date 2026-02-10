import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="LoadingSpinner" data-testid="loading-spinner">
      <div className="spinner"></div>
      <p>Analyzing your travel query...</p>
    </div>
  );
}

export default LoadingSpinner;
