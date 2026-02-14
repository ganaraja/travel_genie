import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import { travelAgentService } from './services/travelAgentService';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'welcome',
      content: "Welcome to Travel Genie",
      timestamp: new Date().toISOString()
    }
  ]);
  const [loading, setLoading] = useState(false);
  const [userId, setUserId] = useState('user_123');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    if (messagesEndRef.current && typeof messagesEndRef.current.scrollIntoView === 'function') {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (query) => {
    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: query,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const result = await travelAgentService.getRecommendation(query, userId);
      
      // Add assistant response
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: result.recommendation,
        timestamp: result.timestamp || new Date().toISOString(),
        query: query
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: 'error',
        content: err.message || 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: 1,
        type: 'welcome',
        content: "Welcome to Travel Genie",
        timestamp: new Date().toISOString()
      }
    ]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div className="header-left">
            <div className="logo-container">
              <div className="logo-icon">
                <img src="/travel-icon.svg" alt="Travel Genie" />
              </div>
              <div className="logo-text">
                <h1>Travel Genie</h1>
                <p>AI-Powered Travel Planning</p>
              </div>
            </div>
          </div>
          <div className="header-right">
            <select
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="user-select"
              disabled={loading}
            >
              <option value="user_123">👤 Comfort Traveler (USA)</option>
              <option value="default">👤 Standard Traveler (USA)</option>
            </select>
            <button 
              onClick={handleClearChat}
              className="clear-button"
              disabled={loading}
            >
              <span>🗑️</span> Clear Chat
            </button>
          </div>
        </div>
      </header>

      <main className="App-main">
        <div className="chat-container">
          <div className="messages-container">
            {messages.map((message) => (
              message.type === 'welcome' ? (
                <div key={message.id} className="welcome-banner">
                  <h2>🌍 Plan Your Perfect Trip with AI</h2>
                  <p>
                    Get personalized travel recommendations in seconds. I'll analyze weather, 
                    flights, hotels, and visa requirements based on your preferences.
                  </p>
                  <div className="features-grid">
                    <div className="feature-item">
                      <div className="feature-item-icon">🛂</div>
                      <div className="feature-item-text">Visa Checking</div>
                    </div>
                    <div className="feature-item">
                      <div className="feature-item-icon">🌤️</div>
                      <div className="feature-item-text">Weather Analysis</div>
                    </div>
                    <div className="feature-item">
                      <div className="feature-item-icon">✈️</div>
                      <div className="feature-item-text">Flight Deals</div>
                    </div>
                    <div className="feature-item">
                      <div className="feature-item-icon">🏨</div>
                      <div className="feature-item-text">Hotel Matches</div>
                    </div>
                  </div>
                </div>
              ) : (
                <ChatMessage key={message.id} message={message} />
              )
            ))}
            {loading && (
              <div className="loading-message">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <p>Analyzing your travel options...</p>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <ChatInput 
            onSend={handleSendMessage} 
            disabled={loading}
            userId={userId}
          />
        </div>
      </main>
    </div>
  );
}

export default App;
