import React from 'react';
import './Features.css';

// Import Feature SVG icons
import AgentOrchestrationIcon from '../Icons/agent-orchestration.svg';
import EnterpriseSecurityIcon from '../Icons/enterprise-security.svg';
import DevelopmentSpeedIcon from '../Icons/development-speed.svg';
import IntelligentMemoryIcon from '../Icons/intelligent-memory.svg';
import ProductionCodeIcon from '../Icons/production-code.svg';
import CloudNativeIcon from '../Icons/cloud-native.svg';

// Import Benefit SVG icons - Agent Orchestration
import SelfOrganizingIcon from '../Icons/self-organizing.svg';
import ContextAwareIcon from '../Icons/context-aware.svg';
import RealTimeCollabIcon from '../Icons/realtime-collab.svg';

// Import Benefit SVG icons - Enterprise Security
import SOC2Icon from '../Icons/soc2-certified.svg';
import GDPRIcon from '../Icons/gdpr-hipaa.svg';
import ZeroKnowledgeIcon from '../Icons/zero-knowledge.svg';

// Import Benefit SVG icons - Development Speed
import InstantCodeGenIcon from '../Icons/instant-codegen.svg';
import AutomatedTestingIcon from '../Icons/automated-testing.svg';
import OneClickDeployIcon from '../Icons/one-click-deploy.svg';

// Import Benefit SVG icons - Intelligent Memory
import VectorSearchIcon from '../Icons/vector-search.svg';
import LongTermMemoryIcon from '../Icons/long-term-memory.svg';
import CrossProjectIcon from '../Icons/cross-project.svg';

// Import Benefit SVG icons - Production-Ready Code
import SOLIDIcon from '../Icons/solid-principles.svg';
import TestCoverageIcon from '../Icons/test-coverage.svg';
import SelfDocumentingIcon from '../Icons/self-documenting.svg';

// Import Benefit SVG icons - Cloud-Native
import AutoScalingIcon from '../Icons/auto-scaling.svg';
import MultiCloudIcon from '../Icons/multi-cloud.svg';
import EdgeDeployIcon from '../Icons/edge-deploy.svg';

interface Benefit {
  text: string;
  icon: string;
}

interface Feature {
  icon: string;
  title: string;
  description: string;
  gradient: string;
  benefits: Benefit[];
}

const features: Feature[] = [
  {
    icon: AgentOrchestrationIcon,
    title: 'Intelligent Agent Orchestration',
    description: 'Multiple specialized AI agents collaborate autonomously to handle complex development tasks.',
    gradient: 'linear-gradient(135deg, #5865F2 0%, #4752C4 100%)',
    benefits: [
      { text: 'Self-organizing team dynamics', icon: SelfOrganizingIcon },
      { text: 'Context-aware task distribution', icon: ContextAwareIcon },
      { text: 'Real-time collaboration', icon: RealTimeCollabIcon }
    ]
  },
  {
    icon: EnterpriseSecurityIcon,
    title: 'Enterprise Security',
    description: 'Bank-grade security with end-to-end encryption and compliance with industry standards.',
    gradient: 'linear-gradient(135deg, #10B981 0%, #059669 100%)',
    benefits: [
      { text: 'SOC 2 Type II certified', icon: SOC2Icon },
      { text: 'GDPR & HIPAA compliant', icon: GDPRIcon },
      { text: 'Zero-knowledge architecture', icon: ZeroKnowledgeIcon }
    ]
  },
  {
    icon: DevelopmentSpeedIcon,
    title: '10x Development Speed',
    description: 'From idea to production in minutes, not months. Accelerate your entire development lifecycle.',
    gradient: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
    benefits: [
      { text: 'Instant code generation', icon: InstantCodeGenIcon },
      { text: 'Automated testing & QA', icon: AutomatedTestingIcon },
      { text: 'One-click deployment', icon: OneClickDeployIcon }
    ]
  },
  {
    icon: IntelligentMemoryIcon,
    title: 'Intelligent Memory',
    description: 'Advanced context management ensures consistency across your entire project lifecycle.',
    gradient: 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)',
    benefits: [
      { text: 'Vector-based search', icon: VectorSearchIcon },
      { text: 'Long-term memory retention', icon: LongTermMemoryIcon },
      { text: 'Cross-project learning', icon: CrossProjectIcon }
    ]
  },
  {
    icon: ProductionCodeIcon,
    title: 'Production-Ready Code',
    description: 'Generate clean, tested, and documented code that follows industry best practices.',
    gradient: 'linear-gradient(135deg, #EC4899 0%, #DB2777 100%)',
    benefits: [
      { text: 'SOLID principles', icon: SOLIDIcon },
      { text: '95%+ test coverage', icon: TestCoverageIcon },
      { text: 'Self-documenting code', icon: SelfDocumentingIcon }
    ]
  },
  {
    icon: CloudNativeIcon,
    title: 'Cloud-Native Architecture',
    description: 'Built for scale with automatic infrastructure provisioning and optimization.',
    gradient: 'linear-gradient(135deg, #06B6D4 0%, #0891B2 100%)',
    benefits: [
      { text: 'Auto-scaling infrastructure', icon: AutoScalingIcon },
      { text: 'Multi-cloud support', icon: MultiCloudIcon },
      { text: 'Edge deployment ready', icon: EdgeDeployIcon }
    ]
  }
];

const Features: React.FC = () => {
  return (
    <section className="features" id="features">
      <div className="features-container">
        

        <div className="features-grid">
          {features.map((feature, index) => {
            return (
              <div key={index} className="feature-card">
                <div
                  className="feature-icon"
                  style={{ background: feature.gradient }}
                >
                  <img src={feature.icon} alt={feature.title} className="feature-svg-icon" />
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
                <ul className="feature-benefits">
                  {feature.benefits.map((benefit, idx) => (
                    <li key={idx} className="feature-benefit">
                      <img src={benefit.icon} alt="" className="benefit-icon" />
                      <span>{benefit.text}</span>
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