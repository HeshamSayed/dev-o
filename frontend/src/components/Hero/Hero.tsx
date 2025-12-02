import React from 'react';
import { Link } from 'react-router-dom';
import './Hero.css';

const Hero: React.FC = () => {
  const scrollToChat = () => {
    const chatSection = document.querySelector('.chat-demo');
    if (chatSection) {
      chatSection.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section className="hero">
      <div className="hero-background">
        <div className="glow-orb glow-orb-1"></div>
        <div className="glow-orb glow-orb-2"></div>
      </div>

      <div className="container hero-content">
        <div className="hero-text">
          <div className="hero-badge">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            <span>AI-Powered Development Platform</span>
          </div>

          <h1 className="hero-title">
            Build Software with
            <span className="gradient-text"> AI Agents</span>
          </h1>

          <p className="hero-subtitle">
            Transform your ideas into production-ready code through natural language.
            DEV-O orchestrates intelligent agents that collaborate to build, test, and deploy your applications.
          </p>

          <div className="hero-buttons">
            <button onClick={scrollToChat} className="btn btn-primary">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Try Demo
            </button>
            <Link to="/login" className="btn btn-secondary">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M15 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <polyline points="10 17 15 12 10 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                <line x1="15" y1="12" x2="3" y2="12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Get Started
            </Link>
          </div>

          <div className="hero-stats">
            <div className="stat">
              <div className="stat-value">10x</div>
              <div className="stat-label">Faster Development</div>
            </div>
            <div className="stat">
              <div className="stat-value">6+</div>
              <div className="stat-label">AI Agents</div>
            </div>
            <div className="stat">
              <div className="stat-value">24/7</div>
              <div className="stat-label">Available</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;