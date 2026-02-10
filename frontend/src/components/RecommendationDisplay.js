import React from 'react';
import './RecommendationDisplay.css';

function RecommendationDisplay({ recommendation }) {
  if (!recommendation) {
    return null;
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="RecommendationDisplay">
      <div className="recommendation-header">
        <h2>✨ Your Personalized Recommendation</h2>
        <div className="recommended-dates">
          <span className="date-label">Recommended Travel Dates:</span>
          <span className="date-range">
            {formatDate(recommendation.recommended_start)} - {formatDate(recommendation.recommended_end)}
          </span>
        </div>
      </div>

      <div className="recommendation-content">
        <section className="reasoning-section">
          <h3>Why This Recommendation Fits You</h3>
          {recommendation.primary_reasoning && recommendation.primary_reasoning.length > 0 ? (
            <ul className="reasoning-list">
              {recommendation.primary_reasoning.map((reason, index) => (
                <li key={index} className={`reason-item ${reason.positive ? 'positive' : 'negative'}`}>
                  <strong>{reason.factor}:</strong> {reason.assessment}
                </li>
              ))}
            </ul>
          ) : (
            <p>No specific reasoning provided.</p>
          )}
        </section>

        <section className="summary-section">
          <h3>Summary</h3>
          <p className="summary-text">{recommendation.personalized_summary}</p>
        </section>

        {recommendation.alternative_options && recommendation.alternative_options.length > 0 && (
          <section className="alternatives-section">
            <h3>Alternative Options</h3>
            <ul className="alternatives-list">
              {recommendation.alternative_options.map((alt, index) => (
                <li key={index} className="alternative-item">
                  <span className="alt-dates">
                    {formatDate(alt[0])} - {formatDate(alt[1])}
                  </span>
                  <span className="alt-reason">{alt[2]}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {recommendation.rejected_periods && recommendation.rejected_periods.length > 0 && (
          <section className="rejected-section">
            <h3>Why Other Periods Were Rejected</h3>
            <ul className="rejected-list">
              {recommendation.rejected_periods.map((rejected, index) => (
                <li key={index} className="rejected-item">
                  <span className="rejected-dates">
                    {formatDate(rejected[0])} - {formatDate(rejected[1])}
                  </span>
                  <span className="rejected-reason">{rejected[2]}</span>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </div>
  );
}

export default RecommendationDisplay;
