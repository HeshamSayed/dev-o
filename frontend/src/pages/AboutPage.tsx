import { Link } from 'react-router-dom';
import './AboutPage.css';

// SVG Icon Components
const RocketIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/>
    <path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>
    <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>
    <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>
  </svg>
);

const TargetIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <circle cx="12" cy="12" r="6"/>
    <circle cx="12" cy="12" r="2"/>
  </svg>
);

const LayersIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="12,2 2,7 12,12 22,7"/>
    <polyline points="2,17 12,22 22,17"/>
    <polyline points="2,12 12,17 22,12"/>
  </svg>
);

const CpuIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="4" y="4" width="16" height="16" rx="2" ry="2"/>
    <rect x="9" y="9" width="6" height="6"/>
    <line x1="9" y1="1" x2="9" y2="4"/>
    <line x1="15" y1="1" x2="15" y2="4"/>
    <line x1="9" y1="20" x2="9" y2="23"/>
    <line x1="15" y1="20" x2="15" y2="23"/>
    <line x1="20" y1="9" x2="23" y2="9"/>
    <line x1="20" y1="14" x2="23" y2="14"/>
    <line x1="1" y1="9" x2="4" y2="9"/>
    <line x1="1" y1="14" x2="4" y2="14"/>
  </svg>
);

const NetworkIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="9" y="2" width="6" height="6"/>
    <rect x="16" y="16" width="6" height="6"/>
    <rect x="2" y="16" width="6" height="6"/>
    <path d="M5 16v-4h14v4"/>
    <line x1="12" y1="12" x2="12" y2="8"/>
  </svg>
);

const ShieldIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
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

const BrainIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.98-3A2.5 2.5 0 0 1 9.5 2Z"/>
    <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.98-3A2.5 2.5 0 0 0 14.5 2Z"/>
  </svg>
);

const GearIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="3"/>
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
  </svg>
);

const CheckCircleIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
    <polyline points="22,4 12,14.01 9,11.01"/>
  </svg>
);

const ArrowRightIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="5" y1="12" x2="19" y2="12"/>
    <polyline points="12,5 19,12 12,19"/>
  </svg>
);

const TrendingUpIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23,6 13.5,15.5 8.5,10.5 1,18"/>
    <polyline points="17,6 23,6 23,12"/>
  </svg>
);

const AboutPage = () => {
  return (
    <div className="about-page wavy-scroll">
      {/* Navigation */}
      <nav className="about-nav">
        <div className="about-nav-container">
          <Link to="/" className="about-logo">
            <img src="/src/components/Logo/DEV-O_Logo.png" alt="DEV-O" className="about-logo-image" />
          </Link>
          <div className="about-nav-links">
            <Link to="/features">Features</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/partners">Partners</Link>
            <Link to="/blog">Blog</Link>
          </div>
          <Link to="/login" className="about-nav-cta">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="about-hero">
        <div className="about-hero-content">
          <div className="about-hero-badge">
            <RocketIcon />
            <span>About DEV-O</span>
          </div>
          <h1>Digital Engineering Virtual Orchestrator</h1>
          <p className="about-hero-tagline">
            An AI-native layer that connects people, code, and systems so teams can 
            build and run software smarter, faster, and safer.
          </p>
          <p className="about-hero-subtitle">
            DEV-O is a flagship project of <strong>Bionicverse Inc. (USA)</strong>, designed for 
            organizations that want to move beyond isolated AI experiments and create a truly 
            AI-native engineering culture.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main className="about-main">
        {/* Why DEV-O Exists */}
        <section className="about-section why-section">
          <div className="section-header">
            <TargetIcon />
            <h2>Why DEV-O Exists</h2>
          </div>
          <p className="section-intro">
            Most companies are already using AI somewhere in their stack – a code assistant here, 
            a chatbot there, a few scripts glued together by advanced people inside the company. 
            But at scale, this approach hits hard limits:
          </p>
          <div className="pain-points">
            <div className="pain-point">
              <span className="pain-icon">⚠️</span>
              <p>Teams lose time context-switching between tools.</p>
            </div>
            <div className="pain-point">
              <span className="pain-icon">⚠️</span>
              <p>Knowledge is scattered across tickets, docs, chats, and repos.</p>
            </div>
            <div className="pain-point">
              <span className="pain-icon">⚠️</span>
              <p>There is no single "brain" that understands how the business, systems, and workflows connect.</p>
            </div>
            <div className="pain-point">
              <span className="pain-icon">⚠️</span>
              <p>AI experiments stay experiments – they rarely become reliable, governed, production-grade capabilities.</p>
            </div>
          </div>
          <div className="solution-box">
            <h3>DEV-O was created to solve this.</h3>
            <p>
              We believe the next generation of organizations will be <strong>engineered around AI</strong>, 
              not just augmented by it. DEV-O is built to help you:
            </p>
            <ul>
              <li><CheckCircleIcon /> Turn fragmented tools into one orchestrated engineering environment.</li>
              <li><CheckCircleIcon /> Turn tribal knowledge into structured, queryable, living knowledge.</li>
              <li><CheckCircleIcon /> Turn ad-hoc AI prompts into repeatable, safe, governed workflows.</li>
            </ul>
          </div>
        </section>

        {/* What DEV-O Is */}
        <section className="about-section what-section">
          <div className="section-header">
            <LayersIcon />
            <h2>What DEV-O Is</h2>
          </div>
          <p className="section-intro">
            DEV-O is a <strong>Digital Engineering Virtual Orchestrator</strong> – a platform that:
          </p>
          <div className="what-grid">
            <div className="what-card">
              <span className="what-number">1</span>
              <h3>Connects to your systems</h3>
              <p>Code repositories, task managers, knowledge bases, observability tools, CI/CD, cloud, data sources.</p>
            </div>
            <div className="what-card">
              <span className="what-number">2</span>
              <h3>Understands your landscape</h3>
              <p>Services, components, owners, runbooks, SLAs, dependencies, risks.</p>
            </div>
            <div className="what-card">
              <span className="what-number">3</span>
              <h3>Coordinates everything</h3>
              <p>AI agents, human teams, and automations across this landscape so work actually gets done – not just suggested.</p>
            </div>
          </div>
          <div className="control-plane-box">
            <h3>Think of DEV-O as a control plane for AI-native engineering:</h3>
            <ul>
              <li>A place where frontier AI models are grounded in your real systems and guardrails.</li>
              <li>A layer that treats tickets, incidents, specs, PRs, services, dashboards, and runbooks as part of one shared graph.</li>
              <li>An environment where humans stay in command, but AI and automation do the heavy lifting.</li>
            </ul>
          </div>
        </section>

        {/* Key Capabilities */}
        <section className="about-section capabilities-section">
          <div className="section-header">
            <CpuIcon />
            <h2>Key Capabilities</h2>
          </div>

          <div className="capability-block">
            <div className="capability-header">
              <BrainIcon />
              <h3>1. AI-Native Engineering Workspace</h3>
            </div>
            <p>DEV-O gives product and engineering teams a shared workspace where:</p>
            <ul>
              <li>AI agents can read, write, and reason over code, docs, tickets, and metrics.</li>
              <li>Context is persistent – every interaction enriches the system's understanding of your organization.</li>
              <li>Collaboration is multi-modal: text, voice, dashboards, and eventually 3D and immersive environments.</li>
            </ul>
          </div>

          <div className="capability-block">
            <div className="capability-header">
              <GearIcon />
              <h3>2. Orchestration, Not Just Automation</h3>
            </div>
            <p>DEV-O doesn't just trigger scripts. It orchestrates workflows end to end:</p>
            <ul>
              <li>Plan → Build → Test → Deploy → Observe → Improve loops.</li>
              <li>Incident response and post-mortems.</li>
              <li>Change management and rollout coordination.</li>
            </ul>
            <div className="automation-features">
              <p>Automations in DEV-O are:</p>
              <div className="feature-tags">
                <span className="feature-tag"><strong>AI-aware</strong> – agents can decide which tools to call and when.</span>
                <span className="feature-tag"><strong>Context-aware</strong> – they know who owns which service, which runbook to follow, and what the current state is.</span>
                <span className="feature-tag"><strong>Governed</strong> – actions follow policies, approvals, and audit trails.</span>
              </div>
            </div>
          </div>

          <div className="capability-block">
            <div className="capability-header">
              <NetworkIcon />
              <h3>3. Living Engineering Knowledge Graph</h3>
            </div>
            <p>Inside DEV-O, your organization's engineering reality becomes a living graph:</p>
            <div className="graph-items">
              <span>Services & microservices</span>
              <span>Pipelines & deployments</span>
              <span>Owners & teams</span>
              <span>SLAs, risks, incidents & dependencies</span>
            </div>
            <p>This graph powers:</p>
            <ul>
              <li>Precise answers to questions like: "What breaks if we change this API?"</li>
              <li>Faster onboarding: "Show me how this service works and who to talk to."</li>
              <li>Safer changes: "Does this rollout violate any existing constraints?"</li>
            </ul>
          </div>

          <div className="capability-block">
            <div className="capability-header">
              <ShieldIcon />
              <h3>4. Safety, Compliance & Guardrails</h3>
            </div>
            <p>Because DEV-O is built for serious engineering work, trust and governance are first-class features:</p>
            <ul>
              <li>Role-based access and fine-grained permissions.</li>
              <li>Policy-aware AI behaviors (what agents can and cannot do).</li>
              <li>Full traceability of automated or AI-assisted changes.</li>
              <li>Configurable data boundaries for sensitive code, infrastructure, and customer data.</li>
            </ul>
          </div>
        </section>

        {/* Built by Bionicverse */}
        <section className="about-section bionicverse-section">
          <div className="section-header">
            <RocketIcon />
            <h2>Built by Bionicverse Inc.</h2>
          </div>
          <p className="section-intro">
            DEV-O is developed by <strong>Bionicverse Inc.</strong>, a US-based company building systems 
            at the intersection of:
          </p>
          <div className="expertise-grid">
            <div className="expertise-card">
              <h3>Robotics & Automation</h3>
              <p>Industrial-grade reliability and safety thinking.</p>
            </div>
            <div className="expertise-card">
              <h3>AI & Digital Experience</h3>
              <p>Frontier models used in real-world customer and engineering workflows.</p>
            </div>
            <div className="expertise-card">
              <h3>Virtual & Spatial Computing</h3>
              <p>Preparing organizations for the shift from 2D dashboards to more immersive operational environments.</p>
            </div>
          </div>
          <div className="experience-box">
            <p>Through ventures like <strong>EGYROBO</strong> and <strong>Bionicverse</strong>, our teams have worked on:</p>
            <ul>
              <li>Autonomous and semi-autonomous robotic systems in demanding environments.</li>
              <li>AI-augmented customer experiences (holographic, immersive, and conversational).</li>
              <li>Large-scale digital transformation projects with governments and enterprises.</li>
            </ul>
            <p className="highlight">
              DEV-O is where this experience converges into a single, opinionated platform for AI-native engineering.
            </p>
          </div>
        </section>

        {/* Who DEV-O Is For */}
        <section className="about-section audience-section">
          <div className="section-header">
            <UsersIcon />
            <h2>Who DEV-O Is For</h2>
          </div>
          <p className="section-intro">
            DEV-O is built for organizations that want to:
          </p>
          <ul className="audience-goals">
            <li><CheckCircleIcon /> Move from manual coordination to AI-assisted orchestration.</li>
            <li><CheckCircleIcon /> Turn their engineering organization into a high-leverage, data-driven system.</li>
            <li><CheckCircleIcon /> Adopt AI deeply without compromising safety, control, or compliance.</li>
          </ul>
          <div className="stakeholders-grid">
            <div className="stakeholder-card">
              <h3>CTOs & Heads of Engineering</h3>
              <p>Who want visibility, resilience, and speed.</p>
            </div>
            <div className="stakeholder-card">
              <h3>Platform & DevOps Teams</h3>
              <p>Who are tired of maintaining fragile glue code between tools.</p>
            </div>
            <div className="stakeholder-card">
              <h3>Product Leaders</h3>
              <p>Who need reliable, fast iteration without chaos.</p>
            </div>
          </div>
        </section>

        {/* Our Principles */}
        <section className="about-section principles-section">
          <div className="section-header">
            <TargetIcon />
            <h2>Our Principles</h2>
          </div>
          <p className="section-intro">
            We're building DEV-O around a few non-negotiable principles:
          </p>
          <div className="principles-grid">
            <div className="principle-card">
              <span className="principle-number">1</span>
              <h3>Human-in-Command</h3>
              <p>AI can assist, propose, and automate – but people decide what matters and when.</p>
            </div>
            <div className="principle-card">
              <span className="principle-number">2</span>
              <h3>System Over Tools</h3>
              <p>Tools come and go. DEV-O focuses on the system: how work flows, how knowledge is captured, and how decisions are made.</p>
            </div>
            <div className="principle-card">
              <span className="principle-number">3</span>
              <h3>Open by Design</h3>
              <p>DEV-O integrates with your existing stack instead of trying to replace it. We believe in interoperability, not lock-in.</p>
            </div>
            <div className="principle-card">
              <span className="principle-number">4</span>
              <h3>Safety as a Feature</h3>
              <p>Governance, observability, and auditability are built in – not bolted on.</p>
            </div>
            <div className="principle-card">
              <span className="principle-number">5</span>
              <h3>Measurable Impact</h3>
              <p>If we can't measure the impact on lead time, quality, incidents, reliability, or cost, we don't consider the job done.</p>
            </div>
          </div>
        </section>

        {/* The Road Ahead */}
        <section className="about-section roadmap-section">
          <div className="section-header">
            <TrendingUpIcon />
            <h2>The Road Ahead</h2>
          </div>
          <p className="section-intro">
            DEV-O is evolving quickly along three main horizons:
          </p>
          <div className="timeline">
            <div className="timeline-item">
              <div className="timeline-marker today"></div>
              <div className="timeline-content">
                <h3>Today</h3>
                <p>An orchestrated layer over your engineering tools and processes, powered by frontier AI models and a rich knowledge graph.</p>
              </div>
            </div>
            <div className="timeline-item">
              <div className="timeline-marker near"></div>
              <div className="timeline-content">
                <h3>Near Future</h3>
                <p>Deeper domain-specific agents (for incidents, releases, architecture, governance) and richer analytics on engineering health.</p>
              </div>
            </div>
            <div className="timeline-item">
              <div className="timeline-marker long"></div>
              <div className="timeline-content">
                <h3>Long Term</h3>
                <p>A fully AI-native operations environment, spanning 2D interfaces, conversational agents, and immersive/3D operational views.</p>
              </div>
            </div>
          </div>
          <div className="goal-box">
            <p>
              Our goal is simple: help organizations become truly <strong>bionic</strong> – where humans 
              and intelligent systems work together as one.
            </p>
          </div>
        </section>

        {/* Work With DEV-O */}
        <section className="about-section cta-section">
          <h2>Work With DEV-O</h2>
          <p>If you want to:</p>
          <ul>
            <li><ArrowRightIcon /> Explore how DEV-O can fit into your current engineering stack,</li>
            <li><ArrowRightIcon /> Pilot DEV-O with a specific team or use case,</li>
            <li><ArrowRightIcon /> Or collaborate with us as a partner or early design customer,</li>
          </ul>
          <p className="cta-text">we'd love to talk.</p>
          <div className="cta-buttons">
            <Link to="/contact" className="cta-btn primary">
              Contact Us
              <ArrowRightIcon />
            </Link>
            <Link to="/features" className="cta-btn secondary">
              Explore Features
            </Link>
          </div>
          <p className="cta-footer">
            DEV-O is a project by <strong>Bionicverse Inc. (USA)</strong>.<br />
            Together, we're building the future of AI-native engineering organizations.
          </p>
        </section>
      </main>

      {/* Footer */}
      <footer className="about-footer">
        <div className="about-footer-content">
          <div className="about-footer-brand">
            <Link to="/" className="about-footer-logo">
              <img src="/src/components/Logo/DEV-O_Logo.png" alt="DEV-O" />
            </Link>
            <p>Digital Engineering Virtual Orchestrator</p>
          </div>
          <div className="about-footer-links">
            <div className="footer-link-group">
              <h4>Legal</h4>
              <Link to="/privacy">Privacy Policy</Link>
              <Link to="/terms">Terms of Service</Link>
              <Link to="/security">Security</Link>
            </div>
            <div className="footer-link-group">
              <h4>Company</h4>
              <Link to="/about">About</Link>
              <Link to="/careers">Careers</Link>
              <Link to="/contact">Contact</Link>
              <Link to="/partners">Partners</Link>
            </div>
            <div className="footer-link-group">
              <h4>Resources</h4>
              <Link to="/features">Features</Link>
              <Link to="/pricing">Pricing</Link>
              <Link to="/blog">Blog</Link>
            </div>
          </div>
        </div>
        <div className="about-footer-bottom">
          <p>© {new Date().getFullYear()} DEV-O by Bionicverse Inc. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default AboutPage;
