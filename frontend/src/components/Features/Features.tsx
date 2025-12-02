import React from 'react';
import {
  CheckCircleIcon
} from '../Icons/Icons';
import {
  HexagonStackIcon,
  ShieldLockIcon,
  CrystalIcon,
  CubeMatrixIcon,
  DiamondCircuitIcon,
  OrbitalRingsIcon
} from '../Icons/UniqueIcons';
import './Features.css';

interface Feature {
  icon: React.FC<{ size?: number; className?: string; color?: string }>;
  title: string;
  description: string;
  gradient: string;
  benefits: string[];
}

const features: Feature[] = [
  {
    icon: HexagonStackIcon,
    title: 'Intelligent Agent Orchestration',
    description: 'Multiple specialized AI agents collaborate autonomously to handle complex development tasks.',
    gradient: 'linear-gradient(135deg, #5865F2 0%, #4752C4 100%)',
    benefits: [
      'Self-organizing team dynamics',
      'Context-aware task distribution',
      'Real-time collaboration'
    ]
  },
  {
    icon: ShieldLockIcon,
    title: 'Enterprise Security',
    description: 'Bank-grade security with end-to-end encryption and compliance with industry standards.',
    gradient: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
    benefits: [
      'SOC 2 Type II certified',
      'GDPR & HIPAA compliant',
      'Zero-knowledge architecture'
    ]
  },
  {
    icon: CrystalIcon,
    title: '10x Development Speed',
    description: 'From idea to production in minutes, not months. Accelerate your entire development lifecycle.',
    gradient: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
    benefits: [
      'Instant code generation',
      'Automated testing & QA',
      'One-click deployment'
    ]
  },
  {
    icon: CubeMatrixIcon,
    title: 'Intelligent Memory',
    description: 'Advanced context management ensures consistency across your entire project lifecycle.',
    gradient: 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)',
    benefits: [
      'Vector-based search',
      'Long-term memory retention',
      'Cross-project learning'
    ]
  },
  {
    icon: DiamondCircuitIcon,
    title: 'Production-Ready Code',
    description: 'Generate clean, tested, and documented code that follows industry best practices.',
    gradient: 'linear-gradient(135deg, #EC4899 0%, #DB2777 100%)',
    benefits: [
      'SOLID principles',
      '95%+ test coverage',
      'Self-documenting code'
    ]
  },
  {
    icon: OrbitalRingsIcon,
    title: 'Cloud-Native Architecture',
    description: 'Built for scale with automatic infrastructure provisioning and optimization.',
    gradient: 'linear-gradient(135deg, #06B6D4 0%, #0891B2 100%)',
    benefits: [
      'Auto-scaling infrastructure',
      'Multi-cloud support',
      'Edge deployment ready'
    ]
  }
];

const Features: React.FC = () => {
  return (
    <section className="features" id="features">
      <div className="features-container">
        <div className="features-header">
          <div className="features-badge">Platform Capabilities</div>
          <h2 className="features-title">
            Everything You Need to Build at
            <br />
            <span className="gradient-text">Enterprise Scale</span>
          </h2>
          <p className="features-subtitle">
            Powered by cutting-edge AI technology and designed for teams that ship fast
          </p>
        </div>

        <div className="features-grid">
          {features.map((feature, index) => {
            const IconComponent = feature.icon;
            return (
              <div key={index} className="feature-card">
                <div
                  className="feature-icon"
                  style={{ background: feature.gradient }}
                >
                  <IconComponent size={28} className="feature-svg-icon" color="#ffffff" />
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
                <ul className="feature-benefits">
                  {feature.benefits.map((benefit, idx) => (
                    <li key={idx} className="feature-benefit">
                      <CheckCircleIcon size={16} color="#10B981" className="benefit-icon" />
                      <span>{benefit}</span>
                    </li>
                  ))}
                </ul>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Features;