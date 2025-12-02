import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ChatDemo.css';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

const ChatDemo: React.FC = () => {
  const navigate = useNavigate();
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m DEV-O, your AI development assistant. I can help you build software, debug code, and manage your projects. Try asking me something!',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault();

    if (inputValue.trim()) {
      // Add user message to show interaction
      const userMessage: Message = {
        id: messages.length + 1,
        type: 'user',
        content: inputValue,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages([...messages, userMessage]);
      setInputValue('');
      setIsTyping(true);

      // After a brief delay, redirect to login
      setTimeout(() => {
        navigate('/login');
      }, 800);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend(e as any);
    }
  };

  const exampleQuestions = [
    "Build a React component",
    "Debug my Python code",
    "Create an API endpoint",
    "Deploy to production"
  ];

  const handleExampleClick = (question: string) => {
    setInputValue(question);
    inputRef.current?.focus();
  };

  return (
    <section className="chat-demo">
      <div className="container">
        <div className="chat-demo-header">
          <h2 className="chat-demo-title">Experience DEV-O in Action</h2>
          <p className="chat-demo-subtitle">
            See how our AI agents can help you build software faster. Try it yourself!
          </p>
        </div>

        <div className="chat-window">
          <div className="chat-window-header">
            <div className="chat-header-left">
              <div className="status-indicator online"></div>
              <span className="chat-header-title">DEV-O Chat</span>
            </div>
            <div className="chat-header-right">
              <span className="chat-header-badge">AI Powered</span>
            </div>
          </div>

          <div className="chat-messages">
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.type}`}>
                <div className="message-avatar">
                  {message.type === 'assistant' ? (
                    <div className="avatar-ai">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                        <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </div>
                  ) : (
                    <div className="avatar-user">U</div>
                  )}
                </div>
                <div className="message-content">
                  <div className="message-header">
                    <span className="message-sender">
                      {message.type === 'assistant' ? 'DEV-O Assistant' : 'You'}
                    </span>
                    <span className="message-time">{message.timestamp}</span>
                  </div>
                  <div className="message-text">{message.content}</div>
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="message assistant">
                <div className="message-avatar">
                  <div className="avatar-ai">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-section">
            <div className="example-questions">
              <span className="example-label">Try:</span>
              {exampleQuestions.map((question, index) => (
                <button
                  key={index}
                  className="example-chip"
                  onClick={() => handleExampleClick(question)}
                >
                  {question}
                </button>
              ))}
            </div>

            <form className="chat-input-form" onSubmit={handleSend}>
              <input
                ref={inputRef}
                type="text"
                className="chat-input"
                placeholder="Ask DEV-O anything about development..."
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
              />
              <button type="submit" className="chat-send-button">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                  <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </button>
            </form>

            <div className="chat-footer">
              <p className="chat-cta">
                <span className="cta-icon">🔒</span>
                Sign up to unlock full AI capabilities and start building!
              </p>
            </div>
          </div>
        </div>

        <div className="chat-demo-features">
          <div className="feature-pill">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <span>Multi-Agent Collaboration</span>
          </div>
          <div className="feature-pill">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M21 16V8C20.9996 7.64927 20.9071 7.30481 20.7315 7.00116C20.556 6.69751 20.3037 6.44536 20 6.27L13 2.27C12.696 2.09446 12.3511 2.00205 12 2.00205C11.6489 2.00205 11.304 2.09446 11 2.27L4 6.27C3.69626 6.44536 3.44398 6.69751 3.26846 7.00116C3.09294 7.30481 3.00036 7.64927 3 8V16C3.00036 16.3507 3.09294 16.6952 3.26846 16.9988C3.44398 17.3025 3.69626 17.5546 4 17.73L11 21.73C11.304 21.9055 11.6489 21.9979 12 21.9979C12.3511 21.9979 12.696 21.9055 13 21.73L20 17.73C20.3037 17.5546 20.556 17.3025 20.7315 16.9988C20.9071 16.6952 20.9996 16.3507 21 16Z" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <span>Production-Ready Code</span>
          </div>
          <div className="feature-pill">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" stroke="currentColor" strokeWidth="2"/>
            </svg>
            <span>Lightning Fast</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ChatDemo;