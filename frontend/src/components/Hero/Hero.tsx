import React from 'react';
import { useNavigate } from 'react-router-dom';
import { LightningIcon } from '../Icons/Icons';
import './Hero.css';

const Hero: React.FC = () => {
  const navigate = useNavigate();

  const scrollToDemo = () => {
    const demoSection = document.querySelector('.chat-demo');
    if (demoSection) {
      demoSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <section className="hero">
      <div className="hero-container">
        <div className="hero-content">
          <div className="hero-badge">
            <div className="hero-badge-icon">
              <LightningIcon size={12} color="#fff" />
            </div>
            <span className="hero-badge-text">AI-Powered Development Platform</span>
          </div>

          <h1 className="hero-title">
            Build Software at the
            <br />
            <span className="text-gradient">Speed of Thought</span>
          </h1>

          <p className="hero-description">
            DEV-O transforms your ideas into production-ready applications using
            advanced AI agents that collaborate, code, test, and deploy autonomously.
          </p>

          <div className="hero-actions">
            <button
              className="btn-primary"
              onClick={() => navigate('/login')}
            >
              Start Building Now
            </button>
            <button
              className="btn-outline"
              onClick={scrollToDemo}
            >
              Watch Demo
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;