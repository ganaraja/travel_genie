import React from 'react';
import './ErrorMessage.css';

function ErrorMessage({ message }) {
  return (
    <div className="ErrorMessage" data-testid="error-message">
      <div className="error-icon">⚠️</div>
      <div className="error-content">
        <h3>Error</h3>
        <p>{message}</p>
      </div>
    </div>
  );
}

export default ErrorMessage;
