import React from 'react';
import {
  MultiAgentIcon,
  PrivateLocalIcon,
  ProductionReadyIcon,
  ContextMemoryIcon,
  NaturalLanguageIcon,
  FullStackIcon,
} from '../FeatureIcons/FeatureIcons';
import './Features.css';

interface Feature {
  icon: React.FC<{ size?: number; className?: string }>;
  title: string;
  description: string;
  gradient: string;
}

const features: Feature[] = [
  {
    icon: MultiAgentIcon,
    title: 'Multi-Agent Collaboration',
    description: 'Active agents dynamically hire team members based on project complexity. Scales from solo agents to full development teams automatically.',
    gradient: 'linear-gradient(135deg, #2563EB 0%, #60A5FA 100%)',
  },
  {
    icon: PrivateLocalIcon,
    title: 'Secure & Private',
    description: 'Your code stays secure and private. Complete control over your data and intellectual property. Enterprise-grade security built-in.',
    gradient: 'linear-gradient(135deg, #A855F7 0%, #06B6D4 100%)',
  },
  {
    icon: ProductionReadyIcon,
    title: 'Production Ready Code',
    description: 'Generate professional, tested, and documented code following best practices. Ready for deployment.',
    gradient: 'linear-gradient(135deg, #06B6D4 0%, #2563EB 100%)',
  },
  {
    icon: ContextMemoryIcon,
    title: 'Context-Aware Memory',
    description: 'Advanced context management with vector search. Agents remember decisions, learn from iterations, and maintain project coherence.',
    gradient: 'linear-gradient(135deg, #2563EB 0%, #A855F7 100%)',
  },
  {
    icon: NaturalLanguageIcon,
    title: 'Natural Language Interface',
    description: 'Describe what you want to build in plain English. No need to know the syntax - just explain your vision.',
    gradient: 'linear-gradient(135deg, #60A5FA 0%, #06B6D4 100%)',
  },
  {
    icon: FullStackIcon,
    title: 'Full Stack Capabilities',
    description: 'From databases to APIs to frontends. Build complete applications with backend, frontend, infrastructure, and deployment.',
    gradient: 'linear-gradient(135deg, #A855F7 0%, #60A5FA 100%)',
  },
];

const Features: React.FC = () => {
  return (
    <section className="features" id="features">
      <div className="container">
        <div className="features-header">
          <h2 className="features-title">
            Built for <span className="gradient-text">Developers & Innovators</span>
          </h2>
          <p className="features-subtitle">
            Everything you need to transform ideas into reality with AI-powered development
          </p>
        </div>

        <div className="features-grid">
          {features.map((feature, index) => {
            const IconComponent = feature.icon;
            return (
              <div
                key={index}
                className="feature-card"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div
                  className="feature-icon"
                  style={{ background: feature.gradient }}
                >
                  <IconComponent size={32} className="feature-svg-icon" />
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Features;
