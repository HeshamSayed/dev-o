/**
 * PricingPage - Comprehensive DEV-O Pricing & Plans
 */

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Logo from '../components/Logo/Logo';
import Footer from '../components/Footer/Footer';
import { PageIcon, PageIconName } from '../components/Icons/PageIcon';
import './PricingPageNew.css';

interface PricingPlan {
  id: string;
  name: string;
  subtitle: string;
  ideal: string[];
  includes: string[];
  bestFor: string;
  icon: PageIconName;
  featured?: boolean;
}

interface TokenBenefit {
  icon: PageIconName;
  title: string;
  description: string;
}

interface ScenarioItem {
  title: string;
  icon: PageIconName;
  description: string;
}

interface EnterpriseFeature {
  icon: PageIconName;
  text: string;
}

interface ComparisonPoint {
  icon: PageIconName;
  text: string;
}

interface ContactCardInfo {
  icon: PageIconName;
  title: string;
  description: string;
  href: string;
}

const PricingPage: React.FC = () => {
  const navigate = useNavigate();
  const [activePlan, setActivePlan] = useState<string>('growth');

  const plans: PricingPlan[] = [
    {
      id: 'starter',
      name: 'Starter',
      subtitle: 'For Early Pilots & Small Teams',
      ideal: [
        'Small engineering teams',
        'First DEV-O pilot in one domain (e.g., incidents or releases)',
        'Exploring AI-native workflows with limited scope'
      ],
      includes: [
        'Access for a limited number of engineering users and stakeholders',
        'Core DEV-O workspace with basic incident & delivery views',
        'A starter monthly token balance for AI assistance and orchestration',
        'Standard support and access to product updates'
      ],
      bestFor: 'Best when you want to prove value quickly in a single area before scaling.',
      icon: 'rocket'
    },
    {
      id: 'growth',
      name: 'Growth',
      subtitle: 'For Multi-Team Engineering Orgs',
      featured: true,
      ideal: [
        'Organizations with multiple squads or teams',
        'Expanding DEV-O beyond a single use case',
        'Coordinating incidents, releases, and onboarding across services'
      ],
      includes: [
        'Higher user limits and more connected services',
        'Extended workflows (incidents, releases, onboarding, command center)',
        'A larger monthly token balance for AI and orchestration',
        'Priority support and onboarding guidance',
        'Access to advanced integrations and more environments'
      ],
      bestFor: 'Best when you want DEV-O to become a core layer in your engineering operations.',
      icon: 'chart'
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      subtitle: 'For Complex, Mission-Critical Environments',
      ideal: [
        'Large, distributed engineering organizations',
        'Regulated industries or mission-critical systems',
        'Deep integration into existing platforms and governance'
      ],
      includes: [
        'Custom user, service, and environment limits',
        'Full access to DEV-O\'s capabilities (knowledge graph, command center, governance, etc.)',
        'Custom monthly token allocations aligned with workload patterns',
        'Enterprise support (SLAs, dedicated contact, success programs)',
        'Security, compliance, and data processing commitments (e.g., DPA, SOC/ISO alignment)',
        'Optional private or region-specific deployment models'
      ],
      bestFor: 'Best when you see DEV-O as your AI-native control plane across many teams, products, or business lines.',
      icon: 'building'
    }
  ];

  const tokenBenefits: TokenBenefit[] = [
    {
      icon: 'chart',
      title: 'Usage is spiky',
      description: 'During a large transformation or migration, you may temporarily need much more AI assistance.'
    },
    {
      icon: 'gear',
      title: 'Workloads are complex',
      description: 'Run deep workflows across many tools and services; tokens let you pay proportionally.'
    },
    {
      icon: 'dial',
      title: 'You want control',
      description: 'Cap, monitor, and adjust token usage based on budget and priorities.'
    }
  ];

  const tokenUseCases = [
    'Running incident analyses that read logs, metrics, and recent changes',
    'Asking DEV-O to summarize complex changes and highlight risk',
    'Performing knowledge graph queries to answer multi-step "how does this work?" questions',
    'Executing automated workflows that coordinate multiple tools and steps',
    'Using multi-agent scenarios where several specialized agents collaborate'
  ];

  const scenarios: ScenarioItem[] = [
    {
      title: 'Pilot with Spiky Incidents',
      icon: 'alert',
      description: 'A team on the Starter plan uses DEV-O mainly for incident response. Most months, they stay within the included token balance. During a period of increased incidents (e.g., a major launch), they temporarily exceed the included usage. They add a one-time token pack to cover the spike, without changing plans.'
    },
    {
      title: 'Growing into Multi-Team Usage',
      icon: 'chart',
      description: 'A company starts with Starter, validates value for incident workflows, then upgrades to Growth as more teams join. The Growth plan includes a larger monthly token balance that covers day-to-day usage across several teams. They keep a small buffer of extra tokens available for busy periods.'
    },
    {
      title: 'Enterprise with Complex Programs',
      icon: 'construction',
      description: 'A large organization on Enterprise uses DEV-O as its AI-native control plane. Together, we size a custom monthly token allocation based on observed patterns and future projects. During a major modernization program, they may temporarily increase token capacity.'
    }
  ];

  const includedFeatures = [
    'Access to the DEV-O web application and core features',
    'User and team management',
    'Base integrations (subject to plan)',
    'Configuring services, teams, and ownership',
    'Standard dashboards and views'
  ];

  const usageBasedFeatures = [
    'AI-driven analysis and reasoning (e.g., incident co-pilot, change risk analysis)',
    'Multi-step orchestration workflows',
    'Complex knowledge queries or multi-agent operations',
    'Optional heavy features that are expensive to run compute-wise'
  ];

  const enterpriseFeatures: EnterpriseFeature[] = [
    { icon: 'users', text: 'Tailored user and service counts' },
    { icon: 'globe', text: 'Dedicated or region-specific infrastructure' },
    { icon: 'clipboard', text: 'Specific SLAs and support options' },
    { icon: 'package', text: 'Pre-committed token bundles' },
    { icon: 'handshake', text: 'Joint planning for large projects' }
  ];

  const comparisonPoints: ComparisonPoint[] = [
    { icon: 'link', text: 'Connects and coordinates many tools across your stack' },
    { icon: 'brain', text: 'Maintains a living engineering knowledge graph' },
    { icon: 'gear', text: 'Orchestrates workflows, not just prompts' },
    { icon: 'users', text: 'Provides shared value across multiple teams and functions' }
  ];

  const contactCards: ContactCardInfo[] = [
    {
      icon: 'briefcase',
      title: 'Sales & Product Exploration',
      description: 'sales@dev-o.ai',
      href: 'mailto:sales@dev-o.ai'
    },
    {
      icon: 'hand',
      title: 'General Inquiries',
      description: 'hello@dev-o.ai',
      href: 'mailto:hello@dev-o.ai'
    }
  ];

  return (
    <div className="pricing-page-new">
      {/* Navigation Header */}
      <header className="pricing-header-nav">
        <div className="pricing-header-container">
          <Link to="/" className="pricing-header-logo">
            <Logo />
          </Link>
          <nav className="pricing-header-links">
            <Link to="/features" className="nav-link">Features</Link>
            <Link to="/pricing" className="nav-link active">Pricing</Link>
            <Link to="/login" className="nav-link">Login</Link>
            <button className="nav-cta" onClick={() => navigate('/login?register=true')}>
              Get Started
            </button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pricing-hero">
        <div className="pricing-hero-content">
          <h1 className="pricing-title">
            Pricing & Plans
          </h1>
          <p className="pricing-subtitle">
            Flexible plans plus token-based usage for AI-native engineering.
            DEV-O is designed to scale with you—from early pilots to full AI-native engineering operations.
          </p>
        </div>
      </section>

      {/* Early Adopter Section */}
      <section className="early-adopter-section">
        <div className="section-container">
          <div className="early-adopter-card">
            <div className="early-adopter-icon">
              <PageIcon name="gift" size={42} />
            </div>
            <h2>Early Adopter Advantages</h2>
            <p>
              Early adopters of DEV-O will receive special benefits, including <strong>preferred pricing</strong>, 
              <strong> closer product collaboration</strong>, and <strong>priority access</strong> to new AI-native capabilities.
            </p>
            <p>
              If you're among the first wave of organizations building AI-native engineering operations with DEV-O, 
              we'll treat you as a <strong>design partner</strong> – shaping the roadmap together, tailoring the model 
              to your needs, and giving you generous token allowances during the early stages.
            </p>
            <div className="early-adopter-cta">
              <a href="mailto:sales@dev-o.ai?subject=Early Adopter Interest" className="cta-button primary">
                Become an Early Adopter
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* How Pricing Works */}
      <section className="how-pricing-works">
        <div className="section-container">
          <h2 className="section-title">How DEV-O Pricing Works</h2>
          <p className="section-description">
            At a high level, DEV-O pricing has two building blocks:
          </p>
          <div className="pricing-blocks">
            <div className="pricing-block">
              <div className="block-number">1</div>
              <h3>Platform Plans</h3>
              <p>Give you access to the DEV-O platform, core capabilities, and a monthly included token balance.</p>
            </div>
            <div className="pricing-block">
              <div className="block-number">2</div>
              <h3>Usage Tokens</h3>
              <p>Cover AI and orchestration workloads beyond what's included in your plan, especially for complex or high-volume projects.</p>
            </div>
          </div>
          <div className="pricing-note">
            <span className="note-icon">
              <PageIcon name="lightbulb" size={20} />
            </span>
            <p>
              You can start with a plan, then add more tokens if your monthly usage spikes, 
              you're running complex projects, or need higher AI and orchestration consumption.
            </p>
          </div>
        </div>
      </section>

      {/* Platform Plans */}
      <section className="plans-section">
        <div className="section-container">
          <h2 className="section-title">Platform Plans</h2>
          <p className="section-description">
            These plan outlines are indicative, not final pricing tiers. Names and limits can change as we refine the offering.
          </p>
          <div className="plans-grid">
            {plans.map((plan) => (
              <div 
                key={plan.id} 
                className={`plan-card ${plan.featured ? 'featured' : ''} ${activePlan === plan.id ? 'active' : ''}`}
                onClick={() => setActivePlan(plan.id)}
              >
                {plan.featured && <div className="featured-badge">Recommended</div>}
                <div className="plan-icon">
                  <PageIcon name={plan.icon} size={36} />
                </div>
                <h3 className="plan-name">{plan.name}</h3>
                <p className="plan-subtitle">{plan.subtitle}</p>
                
                <div className="plan-section">
                  <h4>Ideal for:</h4>
                  <ul>
                    {plan.ideal.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="plan-section">
                  <h4>Includes (conceptually):</h4>
                  <ul>
                    {plan.includes.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>

                <p className="plan-best-for">{plan.bestFor}</p>

                <a 
                  href={`mailto:sales@dev-o.ai?subject=${plan.name} Plan Inquiry`} 
                  className="plan-cta"
                >
                  Contact Sales
                </a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Token-Based Usage */}
      <section className="tokens-section">
        <div className="section-container">
          <h2 className="section-title">Token-Based Usage</h2>
          <p className="section-description">
            In DEV-O, tokens represent the metered usage of AI reasoning, orchestrated workflows, 
            and complex multi-step operations.
          </p>

          <div className="tokens-content">
            <div className="tokens-info">
              <h3>When Token-Based Pricing Helps</h3>
              <div className="token-benefits">
                {tokenBenefits.map((benefit, index) => (
                  <div key={index} className="token-benefit">
                    <span className="benefit-icon">
                      <PageIcon name={benefit.icon} size={20} />
                    </span>
                    <div>
                      <strong>{benefit.title}</strong>
                      <p>{benefit.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="tokens-usage">
              <h3>What Tokens Are Used For</h3>
              <ul className="token-uses">
                {tokenUseCases.map((useCase, index) => (
                  <li key={index}>{useCase}</li>
                ))}
              </ul>
              <p className="tokens-note">
                Some actions are light on token usage (simple queries), others are heavier (deep analysis across many data sources).
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Example Scenarios */}
      <section className="scenarios-section">
        <div className="section-container">
          <h2 className="section-title">Example Scenarios</h2>
          <p className="section-description">
            To illustrate how plans and tokens work together:
          </p>
          <div className="scenarios-grid">
            {scenarios.map((scenario, index) => (
              <div key={index} className="scenario-card">
                <span className="scenario-icon">
                  <PageIcon name={scenario.icon} size={28} />
                </span>
                <h3>{scenario.title}</h3>
                <p>{scenario.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Included vs Usage-Based */}
      <section className="included-section">
        <div className="section-container">
          <h2 className="section-title">What's Included vs. Usage-Based</h2>
          <div className="included-grid">
            <div className="included-card">
              <div className="card-header included">
                <span className="card-icon">
                  <PageIcon name="check" size={20} />
                </span>
                <h3>Included with Platform Plan</h3>
              </div>
              <ul>
                {includedFeatures.map((feature, index) => (
                  <li key={index}>{feature}</li>
                ))}
              </ul>
            </div>
            <div className="included-card">
              <div className="card-header usage">
                <span className="card-icon">
                  <PageIcon name="bolt" size={20} />
                </span>
                <h3>Usage-Based (Tokens)</h3>
              </div>
              <ul>
                {usageBasedFeatures.map((feature, index) => (
                  <li key={index}>{feature}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Enterprise Section */}
      <section className="enterprise-section">
        <div className="section-container">
          <div className="enterprise-card">
            <h2>Enterprise & Custom Arrangements</h2>
            <p>If you have strict security or compliance requirements, highly variable operations, 
            or complex multi-region deployments, we can design custom pricing that matches your reality.</p>
            <div className="enterprise-features">
                {enterpriseFeatures.map((feature, index) => (
                  <div key={index} className="enterprise-feature">
                    <span className="enterprise-feature-icon">
                      <PageIcon name={feature.icon} size={20} />
                    </span>
                    <span>{feature.text}</span>
                  </div>
                ))}
            </div>
            <a href="mailto:sales@dev-o.ai?subject=Enterprise Inquiry" className="enterprise-cta">
              Talk to Sales
            </a>
          </div>
        </div>
      </section>

      {/* Comparison Section */}
      <section className="comparison-section">
        <div className="section-container">
          <h2 className="section-title">Comparing DEV-O to "Just an AI Tool"</h2>
          <div className="comparison-content">
            <p className="comparison-intro">
              DEV-O is an <strong>orchestration layer</strong>, not just a standalone AI assistant.
            </p>
            <div className="comparison-points">
              {comparisonPoints.map((point, index) => (
                <div key={index} className="comparison-point">
                  <span className="point-icon">
                    <PageIcon name={point.icon} size={20} />
                  </span>
                  <p>{point.text}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Next Steps */}
      <section className="next-steps-section">
        <div className="section-container">
          <h2 className="section-title">Next Steps & Getting a Quote</h2>
          <p className="section-description">
            Because every engineering organization looks different, we'll typically:
          </p>
          <div className="steps-list">
            <div className="step">
              <span className="step-number">1</span>
              <p>Discuss your team size, tools, and main use cases</p>
            </div>
            <div className="step">
              <span className="step-number">2</span>
              <p>Estimate a suitable plan tier (Starter, Growth, Enterprise)</p>
            </div>
            <div className="step">
              <span className="step-number">3</span>
              <p>Model an initial token allocation based on expected workflows</p>
            </div>
            <div className="step">
              <span className="step-number">4</span>
              <p>Refine based on pilot results and real usage data</p>
            </div>
          </div>

          <div className="contact-cards">
            {contactCards.map((card, index) => (
              <a key={index} href={card.href} className="contact-card">
                <span className="contact-icon">
                  <PageIcon name={card.icon} size={20} />
                </span>
                <h3>{card.title}</h3>
                <p>{card.description}</p>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Powered By Section */}
      <section className="powered-by-pricing">
        <div className="section-container">
          <div className="powered-by-content">
            <p className="powered-by-label">DEV-O – Digital Engineering Virtual Orchestrator</p>
            <p className="powered-by-company">A project by <strong>Bionicverse Inc. (USA)</strong></p>
            <p className="powered-by-vision">
              Our goal is to give you pricing that is <strong>predictable where it should be</strong>, 
              <strong> flexible where it matters</strong>, and <strong>aligned with the value</strong> DEV-O 
              unlocks in your engineering organization.
            </p>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default PricingPage;
