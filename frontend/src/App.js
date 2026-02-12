import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import { travelAgentService } from './services/travelAgentService';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: "👋 Hi! I'm Travel Genie, your AI travel assistant. I can help you find the perfect time and place for your next trip.\n\nI'll analyze weather patterns, flight options, hotel availability, and your personal preferences to give you personalized recommendations.\n\nWhat destination are you thinking about?",
      timestamp: new Date().toISOString()
    }
  ]);
  const [loading, setLoading] = useState(false);
  const [userId, setUserId] = useState('user_123');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
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
        type: 'assistant',
        content: "Chat cleared! What would you like to know about your next trip?",
        timestamp: new Date().toISOString()
      }
    ]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div className="header-left">
            <h1>🌴 Travel Genie</h1>
            <p>AI-Powered Travel Assistant</p>
          </div>
          <div className="header-right">
            <select
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              className="user-select"
              disabled={loading}
            >
              <option value="user_123">👤 Comfort Traveler</option>
              <option value="default">👤 Standard Traveler</option>
            </select>
            <button 
              onClick={handleClearChat}
              className="clear-button"
              disabled={loading}
            >
              🗑️ Clear Chat
            </button>
          </div>
        </div>
      </header>

      <main className="App-main">
        <div className="chat-container">
          <div className="messages-container">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
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
