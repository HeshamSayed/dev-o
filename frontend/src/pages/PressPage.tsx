import React from 'react';
import { Link } from 'react-router-dom';
import Footer from '../components/Footer/Footer';
import './PressPage.css';

// SVG Icon Components
const FileTextIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14 2 14 8 20 8"/>
    <line x1="16" y1="13" x2="8" y2="13"/>
    <line x1="16" y1="17" x2="8" y2="17"/>
    <polyline points="10 9 9 9 8 9"/>
  </svg>
);

const MessageSquareIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
  </svg>
);

const UsersIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
    <circle cx="9" cy="7" r="4"/>
    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
  </svg>
);

const ImageIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
    <circle cx="8.5" cy="8.5" r="1.5"/>
    <polyline points="21 15 16 10 5 21"/>
  </svg>
);

const LayersIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="12 2 2 7 12 12 22 7 12 2"/>
    <polyline points="2 17 12 22 22 17"/>
    <polyline points="2 12 12 17 22 12"/>
  </svg>
);

const MailIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
    <polyline points="22,6 12,13 2,6"/>
  </svg>
);

const DownloadIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
    <polyline points="7 10 12 15 17 10"/>
    <line x1="12" y1="15" x2="12" y2="3"/>
  </svg>
);

const BuildingIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="4" y="2" width="16" height="20" rx="2" ry="2"/>
    <path d="M9 22v-4h6v4"/>
    <path d="M8 6h.01"/>
    <path d="M16 6h.01"/>
    <path d="M12 6h.01"/>
    <path d="M12 10h.01"/>
    <path d="M12 14h.01"/>
    <path d="M16 10h.01"/>
    <path d="M16 14h.01"/>
    <path d="M8 10h.01"/>
    <path d="M8 14h.01"/>
  </svg>
);

const TargetIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <circle cx="12" cy="12" r="6"/>
    <circle cx="12" cy="12" r="2"/>
  </svg>
);

const AlertCircleIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <line x1="12" y1="8" x2="12" y2="12"/>
    <line x1="12" y1="16" x2="12.01" y2="16"/>
  </svg>
);

const RocketIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/>
    <path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>
    <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>
    <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>
  </svg>
);

const MonitorIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
    <line x1="8" y1="21" x2="16" y2="21"/>
    <line x1="12" y1="17" x2="12" y2="21"/>
  </svg>
);

const BookOpenIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
  </svg>
);

const CopyIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
  </svg>
);

const CheckIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12"/>
  </svg>
);

const MapPinIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
    <circle cx="12" cy="10" r="3"/>
  </svg>
);

const PressPage: React.FC = () => {
  const [copiedIndex, setCopiedIndex] = React.useState<number | null>(null);

  const copyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const boilerplateShort = `DEV-O is a Digital Engineering Virtual Orchestrator that helps organizations build and operate AI-native engineering systems.

Developed by Bionicverse Inc. (USA), DEV-O sits on top of an organization's existing engineering stack—code, tickets, CI/CD, observability, incidents—and orchestrates AI agents, automations, and human workflows across the entire software lifecycle.

The platform connects tools, builds a living engineering knowledge graph, and enables teams to run incidents, releases, and operations with AI assistance while keeping humans firmly in command.`;

  const boilerplateLong = `DEV-O is a Digital Engineering Virtual Orchestrator – an AI-native control layer that connects to an organization's engineering tools, builds a living knowledge graph of services and systems, and orchestrates AI agents plus human teams across the entire software lifecycle.

Instead of replacing the tools companies already use, DEV-O sits on top of the existing stack—code repositories, issue trackers, CI/CD, observability, incident tools—and turns them into one orchestrated system.

DEV-O helps engineering organizations:
• See their real-time engineering landscape in one place, including services, dependencies, incidents, and changes.
• Decide faster using AI-grounded insights, powered by a knowledge graph that captures architecture, ownership, and operational history.
• Act through orchestrated workflows for incidents, releases, onboarding, and governance, with AI and automation doing the heavy lifting.
• Learn continuously as incidents, changes, and decisions enrich the system.

DEV-O is developed by Bionicverse Inc. (USA), a company operating at the intersection of AI, automation, and digital engineering. DEV-O is designed for CTOs, platform teams, SREs, and product organizations that want to move from isolated AI experiments to truly AI-native engineering operations—without compromising security, compliance, or human oversight.`;

  const descriptionOneLine = `DEV-O is a Digital Engineering Virtual Orchestrator that helps organizations orchestrate AI agents, tools, and teams across the software lifecycle.`;

  const description30Word = `DEV-O, built by Bionicverse Inc., is a Digital Engineering Virtual Orchestrator that sits on top of existing tools, builds a knowledge graph of services, and orchestrates AI-assisted workflows for incidents, releases, and operations.`;

  const description80Word = `DEV-O is a Digital Engineering Virtual Orchestrator from Bionicverse Inc. that helps organizations become truly AI-native in how they build and operate software. Instead of replacing tools, DEV-O connects code, tickets, CI/CD, observability, and incident systems into one orchestrated environment. Its knowledge graph and AI agents support faster incident response, safer releases, better visibility for leadership, and human-in-command automation across engineering workflows.`;

  return (
    <div className="press-page">
      {/* Navigation */}
      <nav className="press-nav">
        <Link to="/" className="press-nav-logo">
          <img src="/src/components/Logo/logo+icon.png" alt="DEV-O" className="press-logo-img" />
        </Link>
        <div className="press-nav-links">
          <Link to="/features">Features</Link>
          <Link to="/pricing">Pricing</Link>
          <Link to="/blog">Blog</Link>
          <Link to="/login" className="press-nav-cta">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="press-hero">
        <div className="press-hero-content">
          <h1>Press & Media Kit</h1>
          <p className="press-hero-subtitle">
            Welcome to the DEV-O Press & Media Kit
          </p>
          <p className="press-hero-description">
            Here you'll find ready-to-use information and guidelines for writing about DEV-O, 
            including company overview, key messages, brand assets, and contact details.
          </p>
          <div className="press-hero-badge">
            DEV-O is a project by <strong>Bionicverse Inc. (USA)</strong>
          </div>
        </div>
      </section>

      {/* Quick Links */}
      <section className="press-quick-links">
        <div className="press-quick-links-grid">
          <a href="#boilerplate" className="press-quick-link">
            <FileTextIcon />
            <span>Boilerplate</span>
          </a>
          <a href="#key-messages" className="press-quick-link">
            <MessageSquareIcon />
            <span>Key Messages</span>
          </a>
          <a href="#about-bionicverse" className="press-quick-link">
            <BuildingIcon />
            <span>About Bionicverse</span>
          </a>
          <a href="#use-cases" className="press-quick-link">
            <LayersIcon />
            <span>Use Cases</span>
          </a>
          <a href="#brand-guidelines" className="press-quick-link">
            <ImageIcon />
            <span>Brand Guidelines</span>
          </a>
          <a href="#contact" className="press-quick-link">
            <MailIcon />
            <span>Press Contact</span>
          </a>
        </div>
      </section>

      {/* Boilerplate Section */}
      <section className="press-section" id="boilerplate">
        <div className="press-section-container">
          <h2>DEV-O Boilerplate</h2>
          
          <div className="press-boilerplate">
            <div className="press-boilerplate-card">
              <div className="press-boilerplate-header">
                <h3>Short Version</h3>
                <button 
                  className="press-copy-btn"
                  onClick={() => copyToClipboard(boilerplateShort, 1)}
                >
                  {copiedIndex === 1 ? <CheckIcon /> : <CopyIcon />}
                  {copiedIndex === 1 ? 'Copied!' : 'Copy'}
                </button>
              </div>
              <div className="press-boilerplate-content">
                <p>
                  DEV-O is a Digital Engineering Virtual Orchestrator that helps organizations 
                  build and operate AI-native engineering systems.
                </p>
                <p>
                  Developed by <strong>Bionicverse Inc. (USA)</strong>, DEV-O sits on top of an 
                  organization's existing engineering stack—code, tickets, CI/CD, observability, 
                  incidents—and orchestrates AI agents, automations, and human workflows across 
                  the entire software lifecycle.
                </p>
                <p>
                  The platform connects tools, builds a living engineering knowledge graph, and 
                  enables teams to run incidents, releases, and operations with AI assistance 
                  while keeping humans firmly in command.
                </p>
              </div>
            </div>

            <div className="press-boilerplate-card">
              <div className="press-boilerplate-header">
                <h3>Long Version</h3>
                <button 
                  className="press-copy-btn"
                  onClick={() => copyToClipboard(boilerplateLong, 2)}
                >
                  {copiedIndex === 2 ? <CheckIcon /> : <CopyIcon />}
                  {copiedIndex === 2 ? 'Copied!' : 'Copy'}
                </button>
              </div>
              <div className="press-boilerplate-content">
                <p>
                  DEV-O is a Digital Engineering Virtual Orchestrator – an AI-native control layer 
                  that connects to an organization's engineering tools, builds a living knowledge 
                  graph of services and systems, and orchestrates AI agents plus human teams across 
                  the entire software lifecycle.
                </p>
                <p>
                  Instead of replacing the tools companies already use, DEV-O sits on top of the 
                  existing stack—code repositories, issue trackers, CI/CD, observability, incident 
                  tools—and turns them into one orchestrated system.
                </p>
                <p><strong>DEV-O helps engineering organizations:</strong></p>
                <ul>
                  <li><strong>See</strong> their real-time engineering landscape in one place, including services, dependencies, incidents, and changes.</li>
                  <li><strong>Decide</strong> faster using AI-grounded insights, powered by a knowledge graph that captures architecture, ownership, and operational history.</li>
                  <li><strong>Act</strong> through orchestrated workflows for incidents, releases, onboarding, and governance, with AI and automation doing the heavy lifting.</li>
                  <li><strong>Learn</strong> continuously as incidents, changes, and decisions enrich the system.</li>
                </ul>
                <p>
                  DEV-O is developed by <strong>Bionicverse Inc. (USA)</strong>, a company operating 
                  at the intersection of AI, automation, and digital engineering. DEV-O is designed 
                  for CTOs, platform teams, SREs, and product organizations that want to move from 
                  isolated AI experiments to truly AI-native engineering operations—without 
                  compromising security, compliance, or human oversight.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Messages Section */}
      <section className="press-section press-section-alt" id="key-messages">
        <div className="press-section-container">
          <h2>Key Messages & Positioning</h2>
          <p className="press-section-intro">
            Use or adapt the following key messages when describing DEV-O:
          </p>

          <div className="press-messages-grid">
            <div className="press-message-card">
              <div className="press-message-label">Category</div>
              <p>DEV-O is a <strong>Digital Engineering Virtual Orchestrator</strong> and AI-native control plane for engineering organizations.</p>
            </div>
            <div className="press-message-card">
              <div className="press-message-label">Problem</div>
              <p>Modern teams are overwhelmed by fragmented tools, scattered knowledge, and manual coordination. AI assistants alone are not enough because they lack deep understanding of systems, dependencies, and risk.</p>
            </div>
            <div className="press-message-card">
              <div className="press-message-label">Solution</div>
              <p>DEV-O connects tools, builds a knowledge graph of services and teams, and orchestrates AI agents and workflows across incidents, releases, and engineering operations.</p>
            </div>
            <div className="press-message-card">
              <div className="press-message-label">Differentiator</div>
              <p>DEV-O focuses on <strong>system-level orchestration</strong>, not just chat or isolated assistants. It is built around human-in-command principles, governance, and real-world engineering constraints.</p>
            </div>
            <div className="press-message-card">
              <div className="press-message-label">Outcome</div>
              <p>Organizations get faster incident response, safer releases, better visibility, and a path to becoming truly AI-native in how they build and operate software.</p>
            </div>
          </div>

          <div className="press-tagline-box">
            <div className="press-tagline-label">Suggested Tagline</div>
            <p className="press-tagline">
              DEV-O – The Digital Engineering Virtual Orchestrator for AI-Native Organizations.
            </p>
          </div>
        </div>
      </section>

      {/* About Bionicverse Section */}
      <section className="press-section" id="about-bionicverse">
        <div className="press-section-container">
          <h2>About Bionicverse Inc.</h2>
          <p className="press-section-intro">
            Bionicverse Inc. is the company behind DEV-O.
          </p>

          <div className="press-company-info">
            <div className="press-company-card">
              <h3>Company Details</h3>
              <div className="press-company-detail">
                <strong>Name:</strong> Bionicverse Inc.
              </div>
              <div className="press-company-detail">
                <strong>Registered Address:</strong><br />
                5830 E 2nd St, Ste 7000 #9656<br />
                Casper, Wyoming 82609<br />
                United States
              </div>
            </div>

            <div className="press-company-pillars">
              <h3>Bionicverse builds systems at the intersection of:</h3>
              <div className="press-pillars-grid">
                <div className="press-pillar">
                  <div className="press-pillar-icon"><RocketIcon /></div>
                  <h4>AI & Digital Engineering</h4>
                  <p>Using frontier models in real-world delivery and operations</p>
                </div>
                <div className="press-pillar">
                  <div className="press-pillar-icon"><LayersIcon /></div>
                  <h4>Automation & Robotics</h4>
                  <p>Applying industrial-grade reliability thinking to software systems</p>
                </div>
                <div className="press-pillar">
                  <div className="press-pillar-icon"><MonitorIcon /></div>
                  <h4>Virtual & Spatial Experiences</h4>
                  <p>Preparing organizations for operational environments beyond 2D dashboards</p>
                </div>
              </div>
            </div>

            <div className="press-vision-box">
              <p>
                DEV-O is a flagship platform within this broader vision of helping organizations 
                become truly <strong>bionic</strong>—where humans, AI, and engineered systems operate as one.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Use Cases Section */}
      <section className="press-section press-section-alt" id="use-cases">
        <div className="press-section-container">
          <h2>Product & Use Case Snapshot</h2>
          <p className="press-section-intro">
            When describing DEV-O in stories or materials, you may highlight:
          </p>

          <div className="press-use-cases-grid">
            <div className="press-use-case-card">
              <div className="press-use-case-icon"><AlertCircleIcon /></div>
              <h3>Incident Co-Pilot</h3>
              <p>
                DEV-O helps engineering and SRE teams triage, diagnose, and resolve incidents 
                faster by aggregating alerts, logs, changes, and runbooks into one view with AI assistance.
              </p>
            </div>
            <div className="press-use-case-card">
              <div className="press-use-case-icon"><RocketIcon /></div>
              <h3>Delivery & Release Orchestration</h3>
              <p>
                DEV-O connects roadmaps, tickets, and code changes to services and customer impact, 
                highlighting risks and dependencies before deployments.
              </p>
            </div>
            <div className="press-use-case-card">
              <div className="press-use-case-icon"><MonitorIcon /></div>
              <h3>Engineering Command Center</h3>
              <p>
                DEV-O gives leaders a live overview of system health, incident patterns, 
                delivery flow, and operational risk.
              </p>
            </div>
            <div className="press-use-case-card">
              <div className="press-use-case-icon"><BookOpenIcon /></div>
              <h3>Onboarding & Knowledge Discovery</h3>
              <p>
                New engineers can ask DEV-O how services work, who owns them, and what incidents 
                affected them, using a continuously updated knowledge graph.
              </p>
            </div>
          </div>

          <div className="press-stakeholders">
            <h3>Target Stakeholders</h3>
            <div className="press-stakeholders-list">
              <span className="press-stakeholder-tag">CTOs & Heads of Engineering</span>
              <span className="press-stakeholder-tag">Platform / DevOps / DevEx Leaders</span>
              <span className="press-stakeholder-tag">SRE & Reliability Teams</span>
              <span className="press-stakeholder-tag">Product & Delivery Leaders</span>
            </div>
          </div>
        </div>
      </section>

      {/* Brand Guidelines Section */}
      <section className="press-section" id="brand-guidelines">
        <div className="press-section-container">
          <h2>Brand & Visual Guidelines</h2>
          <p className="press-section-intro">
            For press and external materials, please follow these guidelines:
          </p>

          <div className="press-brand-grid">
            <div className="press-brand-card">
              <h3>Name Usage</h3>
              <ul>
                <li>Use <strong>"DEV-O"</strong> (with hyphen) in all caps when referring to the platform.</li>
                <li>Use <strong>"Bionicverse Inc."</strong> for the company; "Bionicverse" is acceptable in context.</li>
              </ul>
            </div>

            <div className="press-brand-card">
              <h3>Logo Usage</h3>
              <ul>
                <li>Do not alter, stretch, or rotate the DEV-O logo.</li>
                <li>Maintain clear space around the logo equal to at least the height of the "D".</li>
                <li>Use official color or monochrome versions provided in the media kit.</li>
                <li>Avoid placing the logo over busy backgrounds that reduce legibility.</li>
              </ul>
            </div>

            <div className="press-brand-card">
              <h3>Colors & Typography</h3>
              <ul>
                <li>Use DEV-O's primary brand colors and neutrals as defined in the brand guidelines.</li>
                <li>For editorial usage where house styles apply, you may use your own fonts and colors.</li>
                <li>Where DEV-O visuals appear, please avoid recoloring the official logo.</li>
              </ul>
            </div>
          </div>

          <div className="press-brand-note">
            <p>
              For detailed branding guidance, refer to the DEV-O Brand Guidelines document or contact us.
            </p>
          </div>
        </div>
      </section>

      {/* Sample Descriptions Section */}
      <section className="press-section press-section-alt" id="descriptions">
        <div className="press-section-container">
          <h2>Sample Descriptions for Media</h2>
          <p className="press-section-intro">
            Copy and adapt the following short descriptions:
          </p>

          <div className="press-descriptions">
            <div className="press-description-card">
              <div className="press-description-header">
                <h3>One-Line Description</h3>
                <button 
                  className="press-copy-btn"
                  onClick={() => copyToClipboard(descriptionOneLine, 3)}
                >
                  {copiedIndex === 3 ? <CheckIcon /> : <CopyIcon />}
                  {copiedIndex === 3 ? 'Copied!' : 'Copy'}
                </button>
              </div>
              <p>{descriptionOneLine}</p>
            </div>

            <div className="press-description-card">
              <div className="press-description-header">
                <h3>25–30 Word Description</h3>
                <button 
                  className="press-copy-btn"
                  onClick={() => copyToClipboard(description30Word, 4)}
                >
                  {copiedIndex === 4 ? <CheckIcon /> : <CopyIcon />}
                  {copiedIndex === 4 ? 'Copied!' : 'Copy'}
                </button>
              </div>
              <p>{description30Word}</p>
            </div>

            <div className="press-description-card">
              <div className="press-description-header">
                <h3>60–80 Word Description</h3>
                <button 
                  className="press-copy-btn"
                  onClick={() => copyToClipboard(description80Word, 5)}
                >
                  {copiedIndex === 5 ? <CheckIcon /> : <CopyIcon />}
                  {copiedIndex === 5 ? 'Copied!' : 'Copy'}
                </button>
              </div>
              <p>{description80Word}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Story Angles Section */}
      <section className="press-section" id="story-angles">
        <div className="press-section-container">
          <h2>Example Story Angles</h2>
          <p className="press-section-intro">
            For journalists and content creators, DEV-O can fit into broader narratives such as:
          </p>

          <div className="press-angles-grid">
            <div className="press-angle-card">
              <h3>"From DevOps to AI-Native Engineering"</h3>
              <p>How orchestration layers like DEV-O are the next step beyond CI/CD and observability.</p>
            </div>
            <div className="press-angle-card">
              <h3>"AI in Incidents & Reliability"</h3>
              <p>Using AI co-pilots to reduce burnout for on-call engineers while improving response.</p>
            </div>
            <div className="press-angle-card">
              <h3>"Control Planes for AI Agents"</h3>
              <p>Why AI-native control planes are needed to make multi-agent, multi-tool environments safe and practical.</p>
            </div>
            <div className="press-angle-card">
              <h3>"Engineering Knowledge Graphs"</h3>
              <p>How connecting services, incidents, ownership, and changes creates new visibility for engineering leaders.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Media Assets Section */}
      <section className="press-section press-section-alt" id="assets">
        <div className="press-section-container">
          <h2>Media Assets & Downloads</h2>
          <p className="press-section-intro">
            Available assets for press and media use:
          </p>

          <div className="press-assets-grid">
            <div className="press-asset-card">
              <div className="press-asset-icon"><ImageIcon /></div>
              <h3>Logos</h3>
              <p>DEV-O and Bionicverse logos in PNG/SVG for light and dark backgrounds.</p>
              <a href="#" className="press-asset-link">
                <DownloadIcon />
                Request Assets
              </a>
            </div>
            <div className="press-asset-card">
              <div className="press-asset-icon"><MonitorIcon /></div>
              <h3>Product Screenshots</h3>
              <p>Command center, incident workspace, knowledge graph views.</p>
              <a href="#" className="press-asset-link">
                <DownloadIcon />
                Request Assets
              </a>
            </div>
            <div className="press-asset-card">
              <div className="press-asset-icon"><LayersIcon /></div>
              <h3>Illustrations & Diagrams</h3>
              <p>High-level DEV-O architecture and concept visuals.</p>
              <a href="#" className="press-asset-link">
                <DownloadIcon />
                Request Assets
              </a>
            </div>
            <div className="press-asset-card">
              <div className="press-asset-icon"><UsersIcon /></div>
              <h3>Team Photos</h3>
              <p>For articles, interviews, and event promotion.</p>
              <a href="#" className="press-asset-link">
                <DownloadIcon />
                Request Assets
              </a>
            </div>
            <div className="press-asset-card">
              <div className="press-asset-icon"><FileTextIcon /></div>
              <h3>One-Pager / PDF</h3>
              <p>Summary of DEV-O vision, product, and use cases.</p>
              <a href="#" className="press-asset-link">
                <DownloadIcon />
                Request Assets
              </a>
            </div>
          </div>

          <div className="press-assets-note">
            <p>
              If you need specific resolutions, formats, or layered files, contact us and we'll be happy to help.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="press-section press-section-highlight" id="contact">
        <div className="press-section-container">
          <h2>Press & Media Contact</h2>
          <p className="press-section-intro">
            For press inquiries, interviews, speaking requests, or asset access:
          </p>

          <div className="press-contact-grid">
            <div className="press-contact-card">
              <div className="press-contact-icon"><MailIcon /></div>
              <h3>Press & Media</h3>
              <a href="mailto:press@dev-o.ai" className="press-contact-email">press@dev-o.ai</a>
            </div>
            <div className="press-contact-card">
              <div className="press-contact-icon"><MessageSquareIcon /></div>
              <h3>General Inquiries</h3>
                          <a href="mailto:hello@dev-o.ai" className="press-contact-email">hello@dev-o.ai</a>
            </div>
          </div>

          <div className="press-mailing-address">
            <div className="press-address-icon"><MapPinIcon /></div>
            <div className="press-address-content">
              <h4>Mailing Address</h4>
              <p>
                Bionicverse Inc.<br />
                (Attn: Press / DEV-O)<br />
                5830 E 2nd St, Ste 7000 #9656<br />
                Casper, Wyoming 82609<br />
                United States
              </p>
            </div>
          </div>

          <div className="press-closing">
            <p className="press-closing-title">DEV-O – Digital Engineering Virtual Orchestrator</p>
            <p className="press-closing-subtitle">A project by Bionicverse Inc. (USA)</p>
            <p className="press-closing-cta">
              If you're covering AI, engineering, and the future of operations, we'd be glad to collaborate.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default PressPage;
