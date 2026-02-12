import React from 'react';
import './ErrorMessage.css';

function ErrorMessage({ message, onRetry }) {
  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <div className="ErrorMessage">
      <div className="error-header">
        <span className="error-icon">⚠️</span>
        <h3 className="error-title">Oops! Something went wrong</h3>
      </div>
      
      <p className="error-message">{message}</p>
      
      <div className="error-actions">
        {onRetry && (
          <button className="error-button primary" onClick={onRetry}>
            🔄 Try Again
          </button>
        )}
        <button className="error-button" onClick={handleRefresh}>
          ↻ Refresh Page
        </button>
      </div>
    </div>
  );
}

export default ErrorMessage;
