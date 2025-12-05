import React from 'react';
import { useNavigate } from 'react-router-dom';
import heroImage from './Hero-Section-2.png';
import logoImage from '../Logo/DEV-O_Logo.png';
import './Hero.css';

const Hero: React.FC = () => {
  const navigate = useNavigate();

  return (
    <section className="hero">
      {/* Background graphic */}
      <div className="hero-background">
        <img src={heroImage} alt="DEV-O Meta-Agent Diagram" />
      </div>

      <div className="hero-container">
        {/* Logo row */}
        <div className="hero-logo">
          <img src={logoImage} alt="DEV-O" className="hero-logo-icon" />
        </div>

        <div className="hero-content">
          <h1 className="hero-title">
            ORCHESTRATE<br />
            YOUR<br />
            VIRTUAL<br />
            ENGINEERING<br />
            ORG.
          </h1>

          <p className="hero-description">
            DEV-O, the cloud‑native meta‑agent for AI development teams.
          </p>

          <button
            className="request-access-button"
            onClick={() => navigate('/login')}
          >
            REQUEST ACCESS
          </button>
        </div>

        {/* Status cards grid */}
        <div className="status-grid">
          <div className="status-card warning">
            <div className="status-header">
              <span className="status-icon warning" />
              <span className="status-label">WARNING</span>
            </div>
            <p className="status-text">
              Performance Alert: high latency in node 4, optimizing flow.
            </p>
          </div>
          <div className="status-card info">
            <div className="status-header">
              <span className="status-icon info" />
              <span className="status-label">INFO</span>
            </div>
            <p className="status-text">
              Documentation Agent: API reference updated automatically.
            </p>
          </div>
          <div className="status-card success">
            <div className="status-header">
              <span className="status-icon success" />
              <span className="status-label">SUCCESS</span>
            </div>
            <p className="status-text">
              Deployment Successful: v2.1.0 orchestrated to staging.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
