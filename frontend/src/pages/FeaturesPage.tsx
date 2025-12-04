import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Logo from '../components/Logo/Logo';
import Footer from '../components/Footer/Footer';
import './FeaturesPage.css';

interface FeatureSection {
  id: string;
  number: string;
  title: string;
  description: string;
  capabilities: {
    title: string;
    items: string[];
  }[];
  icon: React.ReactNode;
}

const FeaturesPage: React.FC = () => {
  const [activeSection, setActiveSection] = useState<string>('workspace');

  const highLevelValues = [
    {
      icon: '👁️',
      title: 'See',
      description: 'Your entire engineering landscape in one place – services, teams, incidents, deployments, risks, and more.'
    },
    {
      icon: '⚡',
      title: 'Decide',
      description: 'Faster with AI-grounded insights built on a living engineering knowledge graph.'
    },
    {
      icon: '🎯',
      title: 'Act',
      description: 'Through orchestrated workflows where AI agents, automations, and humans work together.'
    },
    {
      icon: '📈',
      title: 'Learn',
      description: 'Continuously as incidents, changes, and decisions enrich the system.'
    }
  ];

  const featureSections: FeatureSection[] = [
    {
      id: 'workspace',
      number: '01',
      title: 'Orchestrated Engineering Workspace',
      description: 'A unified environment where teams don\'t have to jump between ten tools to understand what\'s going on.',
      capabilities: [
        {
          title: 'Unified View of Work',
          items: ['See tickets, incidents, deployments, alerts, and documentation in a single workspace.']
        },
        {
          title: 'Context-Rich Conversations',
          items: ['Ask DEV-O about services, components, releases, or incidents and get answers grounded in code, runbooks, metrics, and ownership.']
        },
        {
          title: 'Role-Aware Views',
          items: ['Tailored dashboards and workspaces for engineering leaders, platform teams, SREs, and product teams.']
        },
        {
          title: 'AI Co-Pilot Everywhere',
          items: ['AI assistance embedded directly into the workspace to summarize, suggest, and coordinate next steps.']
        }
      ],
      icon: <WorkspaceIcon />
    },
    {
      id: 'knowledge-graph',
      number: '02',
      title: 'Engineering Knowledge Graph',
      description: 'At the heart of DEV-O is a living engineering knowledge graph that models how your organization actually works.',
      capabilities: [
        {
          title: 'What It Understands',
          items: [
            'Services, microservices, and components',
            'APIs and dependencies between systems',
            'Environments, pipelines, and deployments',
            'Owners, teams, on-call rotations, and stakeholders',
            'Incidents, alerts, risks, and SLAs',
            'Docs, runbooks, and architecture decisions'
          ]
        },
        {
          title: 'What You Can Do With It',
          items: [
            'Ask impact questions: "What breaks if we change this API?"',
            'Get dependency-aware views of services and systems',
            'Understand who owns what and who should be involved',
            'Accelerate onboarding by giving new engineers a navigable map of your stack'
          ]
        }
      ],
      icon: <KnowledgeGraphIcon />
    },
    {
      id: 'ai-orchestration',
      number: '03',
      title: 'AI Orchestration & Automation Engine',
      description: 'DEV-O coordinates frontier AI models, domain-specific agents, and automations to help work flow from idea to production.',
      capabilities: [
        {
          title: 'Task & Workflow Orchestration',
          items: [
            'Propose workflows for incidents, releases, and changes',
            'Trigger automations and tools with the right context',
            'Hand off to humans when decisions or approvals are required'
          ]
        },
        {
          title: 'Domain-Specific Co-Pilots',
          items: [
            'Incident co-pilot',
            'Delivery and release co-pilot',
            'Architecture assistant',
            'Governance and compliance assistant'
          ]
        },
        {
          title: 'Grounded AI',
          items: [
            'Your code and repositories',
            'Your services and dependencies',
            'Your incidents, runbooks, and policies'
          ]
        },
        {
          title: 'Explainability & Traceability',
          items: ['See what agents did, what tools they used, and why – with logs and traces you can review.']
        }
      ],
      icon: <AIOrchestrationIcon />
    },
    {
      id: 'incident-reliability',
      number: '04',
      title: 'Incident & Reliability Co-Pilot',
      description: 'DEV-O helps your teams respond to, manage, and learn from incidents more effectively.',
      capabilities: [
        {
          title: 'Before & During an Incident',
          items: [
            'Smart Triage: Aggregate alerts, logs, metrics, and recent changes into a single contextual view',
            'Suggested Next Steps: DEV-O proposes likely root causes, diagnostic actions, and relevant runbooks',
            'Stakeholder Coordination: Help coordinate who should be involved, and keep them updated with clear summaries',
            'Live Timeline: Build an automatic timeline of events, actions, and decisions as the incident unfolds'
          ]
        },
        {
          title: 'After an Incident',
          items: [
            'Post-Mortem Drafting: Generate structured incident reports with impact, root cause, timeline, and remediations',
            'Learning & Linking: Link incidents to services, changes, and risks in the knowledge graph for future analysis'
          ]
        }
      ],
      icon: <IncidentIcon />
    },
    {
      id: 'delivery-flow',
      number: '05',
      title: 'Delivery, Change & Flow Orchestration',
      description: 'DEV-O supports the full plan → build → test → deploy → observe → improve loop.',
      capabilities: [
        {
          title: 'Contextual Planning',
          items: ['See roadmap items, tickets, and changes linked to real systems, customers, and usage.']
        },
        {
          title: 'Smart Change Insights',
          items: [
            'Risky areas based on history and dependencies',
            'Services or teams that should be informed',
            'Related incidents or constraints that might be affected'
          ]
        },
        {
          title: 'AI-Assisted Reviews',
          items: [
            'Summarize pull requests in context',
            'Highlight areas that conflict with known patterns or incidents',
            'Suggest reviewers based on ownership and expertise'
          ]
        },
        {
          title: 'Release Monitoring',
          items: ['During and after deployments, DEV-O keeps an eye on metrics and alerts and flags anomalies.']
        }
      ],
      icon: <DeliveryIcon />
    },
    {
      id: 'onboarding-knowledge',
      number: '06',
      title: 'Onboarding, Knowledge & Discovery',
      description: 'Turn your organization\'s tribal knowledge into a discoverable, living asset.',
      capabilities: [
        {
          title: 'Onboarding Guides Powered by Reality',
          items: [
            '"How does this service work?"',
            '"Who owns this?"',
            '"Show me related docs and incidents."'
          ]
        },
        {
          title: 'Automatic Knowledge Linking',
          items: ['DEV-O connects tickets, commits, docs, incidents, and services so teams don\'t have to manually maintain maps.']
        },
        {
          title: 'Search That Understands Context',
          items: ['Search across your engineering universe – and get answers that are grounded, not just keyword based.']
        }
      ],
      icon: <OnboardingIcon />
    },
    {
      id: 'governance',
      number: '07',
      title: 'Governance, Safety & Compliance',
      description: 'DEV-O is built for organizations that care deeply about safety, compliance, and control.',
      capabilities: [
        {
          title: 'Role-Based Access Control',
          items: ['Define who can see and do what across services, data, and automations.']
        },
        {
          title: 'Policy-Aware AI',
          items: [
            'Read-only vs. action permissions',
            'Environment restrictions (e.g., production vs. staging)',
            'Approval flows for sensitive operations'
          ]
        },
        {
          title: 'Audit Trails',
          items: ['Track AI- and automation-assisted actions with detailed logs and explanations.']
        },
        {
          title: 'Data Boundaries & Privacy',
          items: ['Control which repositories, services, and data sources are in scope for AI and which are not.']
        }
      ],
      icon: <GovernanceIcon />
    },
    {
      id: 'integrations',
      number: '08',
      title: 'Integrations & Extensibility',
      description: 'DEV-O is designed to integrate with the tools and environments you already use.',
      capabilities: [
        {
          title: 'Connect To',
          items: [
            'Code hosts and CI/CD tools',
            'Issue trackers and project tools',
            'Observability platforms (logs, metrics, traces)',
            'Incident management and on-call systems',
            'Documentation and knowledge tools',
            'Cloud platforms and infrastructure'
          ]
        },
        {
          title: 'API-First & Extensible',
          items: [
            'Adding custom integrations and data sources',
            'Registering your own automations, scripts, or playbooks',
            'Wiring in your own AI models or providers'
          ]
        },
        {
          title: 'Composable Workflows',
          items: ['Design workflows that span multiple tools and teams, orchestrated by DEV-O.']
        }
      ],
      icon: <IntegrationsIcon />
    },
    {
      id: 'insights',
      number: '09',
      title: 'Insights & Engineering Health',
      description: 'Beyond day-to-day work, DEV-O gives leaders and teams visibility into how engineering is performing.',
      capabilities: [
        {
          title: 'Example Insights',
          items: [
            'Lead time from idea to production',
            'Deployment frequency and stability',
            'Incident patterns by service, team, or domain',
            'Bottlenecks in approvals, reviews, or handoffs',
            'Areas with high operational risk or frequent incidents'
          ]
        }
      ],
      icon: <InsightsIcon />
    },
    {
      id: 'human-in-command',
      number: '10',
      title: 'Human-in-Command by Design',
      description: 'Across all capabilities, DEV-O follows one core principle: Humans stay in command. AI assists.',
      capabilities: [
        {
          title: 'That Means',
          items: [
            'AI and automations propose actions; you decide',
            'Sensitive actions require explicit approvals',
            'Everything is observable and auditable'
          ]
        }
      ],
      icon: <HumanCommandIcon />
    }
  ];

  const useCases = [
    {
      start: 'Incident & Reliability Co-Pilot',
      then: 'Delivery & Change Orchestration',
      icon: '🚨'
    },
    {
      start: 'Command Center for engineering leadership',
      then: 'Onboarding and knowledge tools for teams',
      icon: '📊'
    },
    {
      start: 'AI-assisted workflows in one domain',
      then: 'Gradually add more agents and automations',
      icon: '🤖'
    }
  ];

  const navigate = useNavigate();

  return (
    <div className="features-page">
      {/* Navigation Header */}
      <header className="features-header">
        <div className="features-header-container">
          <Link to="/" className="features-header-logo">
            <Logo />
          </Link>
          <nav className="features-header-nav">
            <Link to="/features" className="nav-link active">Features</Link>
            <Link to="/pricing" className="nav-link">Pricing</Link>
            <Link to="/login" className="nav-link">Login</Link>
            <button className="nav-cta" onClick={() => navigate('/login?register=true')}>
              Get Started
            </button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="features-hero">
        <div className="features-hero-content">
          <div className="features-badge">
            <span className="badge-icon">✨</span>
            <span>Platform Features</span>
          </div>
          <h1 className="features-title">
            The Digital Engineering<br />
            <span className="gradient-text">Virtual Orchestrator</span>
          </h1>
          <p className="features-subtitle">
            DEV-O turns your fragmented tools, data, and teams into one AI-native engineering system.
            Discover what the platform can do for your organization today and how it evolves with you over time.
          </p>
          <div className="features-hero-note">
            <span className="note-icon">💡</span>
            <span>DEV-O doesn't replace your stack – it orchestrates it.</span>
          </div>
        </div>
      </section>

      {/* High-Level Value */}
      <section className="high-level-value">
        <div className="section-container">
          <h2 className="section-title">High-Level Value</h2>
          <p className="section-description">With DEV-O, organizations can:</p>
          <div className="value-grid">
            {highLevelValues.map((value, index) => (
              <div key={index} className="value-card">
                <span className="value-icon">{value.icon}</span>
                <h3 className="value-title">{value.title}</h3>
                <p className="value-description">{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Navigation */}
      <section className="features-nav-section">
        <div className="section-container">
          <div className="features-nav">
            {featureSections.map((section) => (
              <button
                key={section.id}
                className={`nav-item ${activeSection === section.id ? 'active' : ''}`}
                onClick={() => setActiveSection(section.id)}
              >
                <span className="nav-number">{section.number}</span>
                <span className="nav-title">{section.title}</span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Sections */}
      <section className="features-detail">
        <div className="section-container">
          {featureSections.map((section) => (
            <div
              key={section.id}
              id={section.id}
              className={`feature-block ${activeSection === section.id ? 'active' : ''}`}
            >
              <div className="feature-header">
                <div className="feature-icon">{section.icon}</div>
                <div className="feature-meta">
                  <span className="feature-number">{section.number}</span>
                  <h3 className="feature-title">{section.title}</h3>
                </div>
              </div>
              <p className="feature-description">{section.description}</p>
              <div className="capabilities-grid">
                {section.capabilities.map((cap, capIndex) => (
                  <div key={capIndex} className="capability-card">
                    <h4 className="capability-title">{cap.title}</h4>
                    <ul className="capability-list">
                      {cap.items.map((item, itemIndex) => (
                        <li key={itemIndex}>{item}</li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
              {section.id === 'knowledge-graph' && (
                <p className="feature-note">
                  The graph is continuously updated as DEV-O ingests events and metadata from your tools.
                </p>
              )}
              {section.id === 'insights' && (
                <p className="feature-note">
                  These insights are connected to the knowledge graph, so they're always interpreted in the context of your services, teams, and customers.
                </p>
              )}
              {section.id === 'human-in-command' && (
                <p className="feature-note highlight">
                  DEV-O augments your engineering organization without turning it into a black box.
                </p>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* How Organizations Use DEV-O */}
      <section className="use-cases-section">
        <div className="section-container">
          <h2 className="section-title">How Organizations Use DEV-O</h2>
          <p className="section-description">
            Most customers start with one or two high-value capabilities and expand over time:
          </p>
          <div className="use-cases-grid">
            {useCases.map((useCase, index) => (
              <div key={index} className="use-case-card">
                <span className="use-case-icon">{useCase.icon}</span>
                <div className="use-case-flow">
                  <div className="use-case-step">
                    <span className="step-label">Start with</span>
                    <span className="step-text">{useCase.start}</span>
                  </div>
                  <div className="use-case-arrow">→</div>
                  <div className="use-case-step">
                    <span className="step-label">Then add</span>
                    <span className="step-text">{useCase.then}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <p className="use-cases-note">
            DEV-O is built to grow with your organization – from early orchestration experiments to fully AI-native engineering operations.
          </p>
        </div>
      </section>

      {/* Powered By Section */}
      <section className="powered-by-section">
        <div className="section-container">
          <div className="powered-by-card">
            <div className="powered-by-badge">Powered by</div>
            <h3 className="powered-by-title">Bionicverse Inc. (USA)</h3>
            <p className="powered-by-description">
              DEV-O is created and operated by Bionicverse Inc. (USA), bringing together expertise in:
            </p>
            <div className="expertise-tags">
              <span className="expertise-tag">🤖 Robotics and automation</span>
              <span className="expertise-tag">🧠 AI and digital experience</span>
              <span className="expertise-tag">⚙️ Complex, mission-critical systems</span>
            </div>
            <p className="powered-by-vision">
              Together, we're building a platform that helps organizations become truly <strong>bionic</strong> – 
              where human creativity, engineering discipline, and intelligent systems operate as one.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
};

// Icon Components
const WorkspaceIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
    <line x1="3" y1="9" x2="21" y2="9" />
    <line x1="9" y1="21" x2="9" y2="9" />
  </svg>
);

const KnowledgeGraphIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="3" />
    <circle cx="19" cy="5" r="2" />
    <circle cx="5" cy="5" r="2" />
    <circle cx="19" cy="19" r="2" />
    <circle cx="5" cy="19" r="2" />
    <line x1="12" y1="9" x2="12" y2="5" />
    <line x1="14.5" y1="10" x2="17.5" y2="6.5" />
    <line x1="9.5" y1="10" x2="6.5" y2="6.5" />
    <line x1="14.5" y1="14" x2="17.5" y2="17.5" />
    <line x1="9.5" y1="14" x2="6.5" y2="17.5" />
  </svg>
);

const AIOrchestrationIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2L2 7l10 5 10-5-10-5z" />
    <path d="M2 17l10 5 10-5" />
    <path d="M2 12l10 5 10-5" />
  </svg>
);

const IncidentIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
    <line x1="12" y1="9" x2="12" y2="13" />
    <line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
);

const DeliveryIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="16 3 21 3 21 8" />
    <line x1="4" y1="20" x2="21" y2="3" />
    <polyline points="21 16 21 21 16 21" />
    <line x1="15" y1="15" x2="21" y2="21" />
    <line x1="4" y1="4" x2="9" y2="9" />
  </svg>
);

const OnboardingIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
    <line x1="12" y1="6" x2="16" y2="6" />
    <line x1="12" y1="10" x2="16" y2="10" />
    <line x1="8" y1="6" x2="8" y2="6" />
    <line x1="8" y1="10" x2="8" y2="10" />
  </svg>
);

const GovernanceIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    <path d="M9 12l2 2 4-4" />
  </svg>
);

const IntegrationsIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="2" width="6" height="6" rx="1" />
    <rect x="16" y="2" width="6" height="6" rx="1" />
    <rect x="2" y="16" width="6" height="6" rx="1" />
    <rect x="16" y="16" width="6" height="6" rx="1" />
    <path d="M8 5h8" />
    <path d="M8 19h8" />
    <path d="M5 8v8" />
    <path d="M19 8v8" />
  </svg>
);

const InsightsIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="20" x2="18" y2="10" />
    <line x1="12" y1="20" x2="12" y2="4" />
    <line x1="6" y1="20" x2="6" y2="14" />
  </svg>
);

const HumanCommandIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
    <circle cx="12" cy="7" r="4" />
  </svg>
);

export default FeaturesPage;
