import React from 'react';
import './RecommendationDisplay.css';

function RecommendationDisplay({ recommendation }) {
  if (!recommendation) {
    return null;
  }

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: 'Travel Genie Recommendation',
        text: recommendation.recommendation,
      }).catch(() => {
        // Fallback to copy
        handleCopy();
      });
    } else {
      handleCopy();
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(recommendation.recommendation);
    alert('Recommendation copied to clipboard!');
  };

  const handleNewSearch = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="RecommendationDisplay">
      <div className="recommendation-header">
        <div className="recommendation-icon">✨</div>
        <div className="recommendation-title">
          <h3>Your Personalized Recommendation</h3>
          <p className="recommendation-query">"{recommendation.query}"</p>
        </div>
      </div>

      <div className="recommendation-content">
        {recommendation.recommendation}
      </div>

      <div className="recommendation-footer">
        <div className="recommendation-timestamp">
          {recommendation.timestamp && (
            <>Generated on {new Date(recommendation.timestamp).toLocaleString()}</>
          )}
        </div>
        <div className="recommendation-actions">
          <button className="action-button" onClick={handleCopy}>
            📋 Copy
          </button>
          <button className="action-button" onClick={handleShare}>
            🔗 Share
          </button>
          <button className="action-button primary" onClick={handleNewSearch}>
            🔍 New Search
          </button>
        </div>
      </div>
    </div>
  );
}

export default RecommendationDisplay;
