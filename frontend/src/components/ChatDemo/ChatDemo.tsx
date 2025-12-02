import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserIcon } from '../Icons/Icons';
import { BrainNetworkIcon, PulseWaveIcon } from '../Icons/UniqueIcons';
import './ChatDemo.css';

const ChatDemo: React.FC = () => {
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [showRedirect, setShowRedirect] = useState(false);
  const [showTyping, setShowTyping] = useState(false);
  const [showUserMessage, setShowUserMessage] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      setShowUserMessage(true);
      setShowTyping(true);

      setTimeout(() => {
        setShowTyping(false);
        setShowRedirect(true);
        setTimeout(() => {
          navigate('/login');
        }, 1500);
      }, 1000);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setMessage(suggestion);
    // Auto-submit after a brief delay
    setTimeout(() => {
      const form = document.querySelector('.chat-input-form') as HTMLFormElement;
      if (form) {
        form.requestSubmit();
      }
    }, 100);
  };

  const suggestions = [
    "Build a SaaS dashboard",
    "Create an e-commerce API",
    "Deploy a React app",
    "Fix production bugs"
  ];

  return (
    <section className="chat-demo">
      <div className="chat-demo-container">
        <div className="chat-interface">
          {/* Professional Header */}
          <div className="chat-header">
            <div className="chat-header-left">
              <div className="chat-status"></div>
              <span className="chat-header-title">DEV-O Assistant</span>
              <span className="chat-header-subtitle">AI Development Agent</span>
            </div>
          </div>

          {/* Messages */}
          <div className="chat-messages">
            <div className="message assistant-message">
              <div className="message-avatar">
                <BrainNetworkIcon size={24} color="#5865F2" />
              </div>
              <div className="message-bubble">
                <div className="message-sender">DEV-O</div>
                <p className="message-text">
                  Hello! I'm DEV-O, your AI development partner. I can help you build
                  production-ready applications, architect systems, write tests, and deploy
                  to the cloud. What would you like to create today?
                </p>
              </div>
            </div>

            {showUserMessage && (
              <div className="message user-message">
                <div className="message-bubble">
                  <div className="message-sender">You</div>
                  <p className="message-text">{message}</p>
                </div>
                <div className="message-avatar">
                  <UserIcon size={24} color="#A855F7" />
                </div>
              </div>
            )}

            {showTyping && (
              <div className="typing-indicator">
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
                <span className="typing-dot"></span>
              </div>
            )}

            {showRedirect && (
              <div className="redirect-notice">
                <p>
                  <PulseWaveIcon size={16} color="#5865F2" />
                  Redirecting to your workspace...
                </p>
              </div>
            )}
          </div>

          {/* Suggestions */}
          <div className="chat-suggestions">
            <span className="suggestions-label">Quick Actions</span>
            <div className="suggestions-list">
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  className="suggestion-chip"
                  onClick={() => handleSuggestionClick(suggestion)}
                  disabled={showUserMessage}
                >
                  {suggestion}
                </button>
              ))}</div>
          </div>

          {/* Input Area */}
          <div className="chat-input-container">
            <form className="chat-input-form" onSubmit={handleSubmit}>
              <div className="chat-input-wrapper">
                <input
                  type="text"
                  className="chat-input"
                  placeholder="Describe what you want to build..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  disabled={showUserMessage}
                />
                <div className="input-actions">
                  <button
                    type="submit"
                    className="chat-send"
                    disabled={!message.trim() || showUserMessage}
                  >
                    Send
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ChatDemo;