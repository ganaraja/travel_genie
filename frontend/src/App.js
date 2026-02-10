import React, { useState } from 'react';
import './App.css';
import TravelQueryForm from './components/TravelQueryForm';
import RecommendationDisplay from './components/RecommendationDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { travelAgentService } from './services/travelAgentService';

function App() {
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleQuery = async (query, userId) => {
    setLoading(true);
    setError(null);
    setRecommendation(null);

    try {
      const result = await travelAgentService.getRecommendation(query, userId);
      setRecommendation(result);
    } catch (err) {
      setError(err.message || 'An error occurred while getting your recommendation.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌴 Travel Genie</h1>
        <p>Your AI-powered travel recommendation assistant</p>
      </header>

      <main className="App-main">
        <TravelQueryForm onSubmit={handleQuery} disabled={loading} />

        {loading && <LoadingSpinner />}

        {error && <ErrorMessage message={error} />}

        {recommendation && !loading && (
          <RecommendationDisplay recommendation={recommendation} />
        )}
      </main>
    </div>
  );
}

export default App;
