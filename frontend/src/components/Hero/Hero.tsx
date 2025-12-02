import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../Logo/Logo';
import './Hero.css';

const Hero: React.FC = () => {
  return (
    <section className="hero">
      <div className="hero-background">
        <div className="glow-orb glow-orb-1"></div>
        <div className="glow-orb glow-orb-2"></div>
      </div>

      <div className="container hero-content">
        <div className="hero-text">
          <div className="hero-logo">
            <Logo size={100} showText={false} />
          </div>
          <h1 className="hero-title">
            Where Intelligence Meets
            <span className="gradient-text"> Innovation</span>
          </h1>
          <p className="hero-subtitle">
            <strong className="ai-slogan">"Your Vision. AI Precision. Infinite Possibilities."</strong>
          </p>
          <p className="hero-description">
            DEV-O orchestrates autonomous AI agents that transform ideas into production-ready code.
            Experience the future of software development where natural language commands deploy entire systems.
          </p>
          <div className="hero-cta">
            <Link to="/signup" className="btn btn-primary">
              Get Started
            </Link>
            <Link to="/login" className="btn btn-secondary">
              Sign In
            </Link>
          </div>
          <div className="hero-stats">
            <div className="stat">
              <div className="stat-value">6+</div>
              <div className="stat-label">Active Agents</div>
            </div>
            <div className="stat">
              <div className="stat-value">Auto</div>
              <div className="stat-label">Team Scaling</div>
            </div>
            <div className="stat">
              <div className="stat-value">100%</div>
              <div className="stat-label">Production Ready</div>
            </div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="terminal-window">
            <div className="terminal-header">
              <div className="terminal-buttons">
                <span className="terminal-button red"></span>
                <span className="terminal-button yellow"></span>
                <span className="terminal-button green"></span>
              </div>
              <div className="terminal-title">dev-o</div>
            </div>
            <div className="terminal-body">
              <div className="terminal-line">
                <span className="prompt">$</span>
                <span className="command">dev-o</span>
              </div>
              <div className="terminal-line user-input">
                <span className="prompt-user">You:</span>
                <span className="user-text">Build a REST API for user authentication</span>
              </div>
              <div className="terminal-line agent-line">
                <span className="agent-badge orchestrator">Orchestrator</span>
                <span className="agent-text">Breaking down into tasks...</span>
              </div>
              <div className="terminal-line agent-line">
                <span className="agent-badge architect">Architect</span>
                <span className="agent-text">Designing system architecture...</span>
              </div>
              <div className="terminal-line agent-line">
                <span className="agent-badge backend">Backend Lead</span>
                <span className="agent-text">Implementing API endpoints...</span>
              </div>
              <div className="terminal-line success-line">
                <span className="success-icon">✓</span>
                <span className="success-text">Authentication API ready!</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
