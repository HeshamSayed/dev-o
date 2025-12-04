import { Link } from 'react-router-dom';
import './PartnersPage.css';

// SVG Icon Components
const NetworkIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="5" r="3"/>
    <circle cx="5" cy="19" r="3"/>
    <circle cx="19" cy="19" r="3"/>
    <line x1="12" y1="8" x2="5" y2="16"/>
    <line x1="12" y1="8" x2="19" y2="16"/>
  </svg>
);

const CodeIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="16,18 22,12 16,6"/>
    <polyline points="8,6 2,12 8,18"/>
  </svg>
);

const CloudIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>
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

const ShoppingBagIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
    <line x1="3" y1="6" x2="21" y2="6"/>
    <path d="M16 10a4 4 0 0 1-8 0"/>
  </svg>
);

const StarIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26 12,2"/>
  </svg>
);

const DatabaseIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <ellipse cx="12" cy="5" rx="9" ry="3"/>
    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
  </svg>
);

const GraphIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="2"/>
    <circle cx="6" cy="6" r="2"/>
    <circle cx="18" cy="6" r="2"/>
    <circle cx="6" cy="18" r="2"/>
    <circle cx="18" cy="18" r="2"/>
    <line x1="12" y1="10" x2="12" y2="8"/>
    <line x1="6" y1="8" x2="6" y2="16"/>
    <line x1="18" y1="8" x2="18" y2="16"/>
    <line x1="10.5" y1="11" x2="7.5" y2="7.5"/>
    <line x1="13.5" y1="11" x2="16.5" y2="7.5"/>
  </svg>
);

const ZapIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="13,2 3,14 12,14 11,22 21,10 12,10 13,2"/>
  </svg>
);

const GitBranchIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="6" y1="3" x2="6" y2="15"/>
    <circle cx="18" cy="6" r="3"/>
    <circle cx="6" cy="18" r="3"/>
    <path d="M18 9a9 9 0 0 1-9 9"/>
  </svg>
);

const ClipboardIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
    <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
  </svg>
);

const ActivityIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>
  </svg>
);

const BookIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
  </svg>
);

const ShieldIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
  </svg>
);

const ServerIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
    <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
    <line x1="6" y1="6" x2="6.01" y2="6"/>
    <line x1="6" y1="18" x2="6.01" y2="18"/>
  </svg>
);

const LockIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
  </svg>
);

const WebhookIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 16.98h-5.99c-1.1 0-1.95.68-2.95 1.76C8.07 19.83 6.22 21 4 21c-1.5 0-2.5-1-3-2"/>
    <path d="M9 10a5 5 0 0 1 5 5v3.03"/>
    <circle cx="19" cy="19" r="2"/>
    <circle cx="5" cy="5" r="2"/>
    <circle cx="5" cy="19" r="2"/>
    <path d="M5 7v10"/>
    <path d="M19 17v-5.5a6.5 6.5 0 0 0-13 0V17"/>
  </svg>
);

const ApiIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 4h6v6H4z"/>
    <path d="M14 4h6v6h-6z"/>
    <path d="M4 14h6v6H4z"/>
    <path d="M17 14v3a2 2 0 0 1-2 2h-3"/>
    <path d="M14 17h3"/>
    <path d="M17 14h3"/>
  </svg>
);

const HandshakeIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M11 17a4 4 0 0 1-8 0c0-2.21 1.79-5 4-5"/>
    <path d="M13 17a4 4 0 0 0 8 0c0-2.21-1.79-5-4-5"/>
    <path d="M12 12V4"/>
    <path d="M7 8l5-4 5 4"/>
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

const CheckCircleIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
    <polyline points="22,4 12,14.01 9,11.01"/>
  </svg>
);

const MailIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
    <polyline points="22,6 12,13 2,6"/>
  </svg>
);

const MapPinIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
    <circle cx="12" cy="10" r="3"/>
  </svg>
);

const ArrowRightIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="5" y1="12" x2="19" y2="12"/>
    <polyline points="12,5 19,12 12,19"/>
  </svg>
);

const PartnersPage = () => {
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="partners-page wavy-scroll">
      {/* Navigation */}
      <nav className="partners-nav">
        <div className="partners-nav-container">
          <Link to="/" className="partners-logo">
            <img src="/src/components/Logo/DEV-O_Logo.png" alt="DEV-O" className="partners-logo-image" />
          </Link>
          <div className="partners-nav-links">
            <Link to="/features">Features</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/blog">Blog</Link>
            <Link to="/careers">Careers</Link>
          </div>
          <Link to="/login" className="partners-nav-cta">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="partners-hero">
        <div className="partners-hero-content">
          <div className="partners-hero-badge">
            <NetworkIcon />
            <span>Partners & Integrations</span>
          </div>
          <h1>Built to Work With the Tools You Trust</h1>
          <p>
            DEV-O partners with technology providers, systems integrators, and channel partners – 
            turning DEV-O into the orchestration layer for your engineering ecosystem.
          </p>
          <div className="partners-hero-actions">
            <a href="mailto:partners@dev-o.ai" className="partners-btn-primary">
              Become a Partner
              <ArrowRightIcon />
            </a>
            <button onClick={() => scrollToSection('integrations')} className="partners-btn-secondary">
              View Integrations
            </button>
          </div>
          <p className="partners-hero-subtitle">
            DEV-O is a project by <strong>Bionicverse Inc.</strong> (USA)
          </p>
        </div>
      </section>

      {/* Table of Contents */}
      <aside className="partners-toc">
        <h3>On This Page</h3>
        <ul>
          <li><button onClick={() => scrollToSection('why-partner')}>Why Partner with DEV-O?</button></li>
          <li><button onClick={() => scrollToSection('partner-types')}>Types of Partners</button></li>
          <li><button onClick={() => scrollToSection('integrations')}>Integration Overview</button></li>
          <li><button onClick={() => scrollToSection('categories')}>Integration Categories</button></li>
          <li><button onClick={() => scrollToSection('how-it-works')}>How Integrations Work</button></li>
          <li><button onClick={() => scrollToSection('become-partner')}>Becoming a Partner</button></li>
          <li><button onClick={() => scrollToSection('existing-customers')}>For Existing Customers</button></li>
          <li><button onClick={() => scrollToSection('contact')}>Contact</button></li>
        </ul>
      </aside>

      {/* Main Content */}
      <main className="partners-main">
        {/* Why Partner Section */}
        <section id="why-partner" className="partners-section">
          <div className="section-header">
            <div className="section-icon">
              <HandshakeIcon />
            </div>
            <h2>Why Partner with DEV-O?</h2>
          </div>
          <div className="why-partner-content">
            <div className="why-partner-intro">
              <p>
                DEV-O is a <strong>Digital Engineering Virtual Orchestrator</strong> – an AI-native control layer 
                that sits on top of your existing engineering stack and connects:
              </p>
              <ul className="connection-list">
                <li><CodeIcon /> Code hosting and CI/CD pipelines</li>
                <li><ClipboardIcon /> Issue trackers and project tools</li>
                <li><ActivityIcon /> Observability, logging, and incident management</li>
                <li><BookIcon /> Documentation and knowledge systems</li>
                <li><CloudIcon /> Cloud and infrastructure platforms</li>
              </ul>
            </div>
            <div className="partner-benefits">
              <h3>By integrating with DEV-O, partners can:</h3>
              <div className="benefits-grid">
                <div className="benefit-card">
                  <div className="benefit-icon"><ZapIcon /></div>
                  <h4>Increase Tool Value</h4>
                  <p>Plug into a broader orchestration and AI layer to amplify your tool's capabilities.</p>
                </div>
                <div className="benefit-card">
                  <div className="benefit-icon"><UsersIcon /></div>
                  <h4>Reach New Customers</h4>
                  <p>Connect with organizations standardizing on DEV-O as their engineering control plane.</p>
                </div>
                <div className="benefit-card">
                  <div className="benefit-icon"><NetworkIcon /></div>
                  <h4>Enable AI-Native Workflows</h4>
                  <p>Power workflows that span multiple products and teams seamlessly.</p>
                </div>
                <div className="benefit-card">
                  <div className="benefit-icon"><CodeIcon /></div>
                  <h4>Reduce Custom Glue Code</h4>
                  <p>Eliminate the custom integration work customers would otherwise build on their own.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Types of Partners Section */}
        <section id="partner-types" className="partners-section">
          <div className="section-header">
            <div className="section-icon">
              <UsersIcon />
            </div>
            <h2>Types of Partners</h2>
          </div>
          <p className="section-intro">We work with a variety of partners to build a rich ecosystem around DEV-O.</p>
          
          <div className="partner-types-grid">
            <div className="partner-type-card">
              <div className="partner-type-header">
                <div className="partner-type-icon"><CodeIcon /></div>
                <h3>Technology Partners</h3>
              </div>
              <p>Technology partners provide tools and platforms that connect directly to DEV-O:</p>
              <ul>
                <li>Code hosting & version control platforms</li>
                <li>Issue tracking & project management tools</li>
                <li>CI/CD & deployment systems</li>
                <li>Observability, logging & APM solutions</li>
                <li>Incident management & on-call tools</li>
                <li>Documentation & knowledge base platforms</li>
                <li>Chat & collaboration tools</li>
                <li>Cloud & infrastructure providers</li>
              </ul>
              <div className="partner-type-benefits">
                <h4>Integration Benefits:</h4>
                <ul>
                  <li>Participate in orchestrated workflows (incidents, releases, governance, onboarding)</li>
                  <li>Contribute data to DEV-O's engineering knowledge graph</li>
                  <li>Be invoked by AI agents with the right context and permissions</li>
                </ul>
              </div>
            </div>

            <div className="partner-type-card">
              <div className="partner-type-header">
                <div className="partner-type-icon"><CloudIcon /></div>
                <h3>Cloud & AI Partners</h3>
              </div>
              <p>DEV-O is designed to work with modern cloud and AI providers.</p>
              <div className="partner-type-benefits">
                <h4>Cloud and AI partners can:</h4>
                <ul>
                  <li>Provide infrastructure and data services that DEV-O orchestrates</li>
                  <li>Offer AI models and runtimes that DEV-O agents can call under clear guardrails</li>
                  <li>Collaborate on reference architectures and best practices for AI-native engineering</li>
                </ul>
              </div>
            </div>

            <div className="partner-type-card">
              <div className="partner-type-header">
                <div className="partner-type-icon"><UsersIcon /></div>
                <h3>Systems Integrators & Consulting Partners</h3>
              </div>
              <p>Systems integrators (SIs), consulting firms, and specialized engineering partners help customers:</p>
              <ul>
                <li>Design and implement AI-native engineering workflows using DEV-O</li>
                <li>Integrate DEV-O with complex existing stacks and regulated environments</li>
                <li>Develop custom runbooks, automations, and agents tailored to each organization</li>
              </ul>
              <div className="partner-type-benefits">
                <h4>We collaborate closely on:</h4>
                <ul>
                  <li>Discovery & assessment of current engineering practices</li>
                  <li>Solution design and rollout plans</li>
                  <li>Training & enablement for customer teams</li>
                </ul>
              </div>
            </div>

            <div className="partner-type-card">
              <div className="partner-type-header">
                <div className="partner-type-icon"><ShoppingBagIcon /></div>
                <h3>Channel Partners, Resellers & MSPs</h3>
              </div>
              <p>Channel partners, resellers, and managed service providers (MSPs) can:</p>
              <ul>
                <li>Bundle DEV-O with their own services and offerings</li>
                <li>Provide managed orchestration and engineering operations to customers</li>
                <li>Extend their portfolio with AI-native control plane capabilities</li>
              </ul>
              <p className="partner-type-note">
                DEV-O supports flexible commercial models so partners can create sustainable, value-driven offerings.
              </p>
            </div>

            <div className="partner-type-card featured">
              <div className="partner-type-header">
                <div className="partner-type-icon"><StarIcon /></div>
                <h3>Design Partners & Lighthouse Customers</h3>
              </div>
              <p>We work with a select group of design partners and lighthouse customers who:</p>
              <ul>
                <li>Operate complex engineering environments</li>
                <li>Are early adopters of AI-native workflows</li>
                <li>Want direct input into DEV-O's roadmap and features</li>
              </ul>
              <p className="partner-type-note highlight">
                These collaborations help shape DEV-O around real-world needs and use cases.
              </p>
            </div>
          </div>
        </section>

        {/* Integration Overview Section */}
        <section id="integrations" className="partners-section">
          <div className="section-header">
            <div className="section-icon">
              <NetworkIcon />
            </div>
            <h2>Integration Overview</h2>
          </div>
          <p className="section-intro">
            DEV-O is <strong>tool-agnostic</strong> and <strong>API-first</strong>. 
            Integrations typically cover three key dimensions:
          </p>

          <div className="integration-dimensions">
            <div className="dimension-card">
              <div className="dimension-number">1</div>
              <div className="dimension-content">
                <div className="dimension-header">
                  <DatabaseIcon />
                  <h3>Data Ingest & Sync</h3>
                </div>
                <p>DEV-O ingests events and metadata from your tools, such as:</p>
                <ul>
                  <li>Commits, branches, and releases</li>
                  <li>Tickets, epics, and incident records</li>
                  <li>Logs, metrics, traces, and alerts</li>
                  <li>Service definitions and ownership mappings</li>
                </ul>
              </div>
            </div>

            <div className="dimension-card">
              <div className="dimension-number">2</div>
              <div className="dimension-content">
                <div className="dimension-header">
                  <GraphIcon />
                  <h3>Knowledge Graph Enrichment</h3>
                </div>
                <p>Data from integrations is used to build and update DEV-O's engineering knowledge graph:</p>
                <ul>
                  <li>Services ↔ dependencies ↔ teams</li>
                  <li>Incidents ↔ changes ↔ environments</li>
                  <li>Docs ↔ runbooks ↔ architecture decisions</li>
                </ul>
              </div>
            </div>

            <div className="dimension-card">
              <div className="dimension-number">3</div>
              <div className="dimension-content">
                <div className="dimension-header">
                  <ZapIcon />
                  <h3>Actions & Orchestration</h3>
                </div>
                <p>DEV-O can trigger actions back into integrated tools, such as:</p>
                <ul>
                  <li>Creating or updating tickets or incidents</li>
                  <li>Triggering or annotating deployments</li>
                  <li>Updating status pages or communication channels</li>
                  <li>Linking context into documentation or runbooks</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="integration-note">
            <ShieldIcon />
            <p>All of this is controlled by <strong>permissions</strong>, <strong>policies</strong>, and <strong>explicit configuration</strong>.</p>
          </div>
        </section>

        {/* Integration Categories Section */}
        <section id="categories" className="partners-section">
          <div className="section-header">
            <div className="section-icon">
              <ServerIcon />
            </div>
            <h2>Integration Categories</h2>
          </div>
          <p className="section-intro">
            Below is a high-level view of the kinds of tools DEV-O connects with. 
            Specific vendors and versions may vary; reach out to discuss your stack.
          </p>

          <div className="categories-grid">
            <div className="category-card">
              <div className="category-header">
                <GitBranchIcon />
                <h3>Code, CI/CD & Artifacts</h3>
              </div>
              <ul>
                <li>Git hosting and source code management</li>
                <li>Build and test pipelines</li>
                <li>Deployment orchestration and release tools</li>
                <li>Artifact repositories</li>
              </ul>
            </div>

            <div className="category-card">
              <div className="category-header">
                <ClipboardIcon />
                <h3>Planning, Issues & Incidents</h3>
              </div>
              <ul>
                <li>Work item and issue tracking</li>
                <li>Agile and project management tools</li>
                <li>Incident management and on-call scheduling</li>
              </ul>
            </div>

            <div className="category-card">
              <div className="category-header">
                <ActivityIcon />
                <h3>Observability & Operations</h3>
              </div>
              <ul>
                <li>Metrics & time-series databases</li>
                <li>Log aggregation and search</li>
                <li>Tracing systems</li>
                <li>APM / performance monitoring</li>
                <li>Synthetic monitoring and uptime checks</li>
              </ul>
            </div>

            <div className="category-card">
              <div className="category-header">
                <BookIcon />
                <h3>Knowledge & Documentation</h3>
              </div>
              <ul>
                <li>Wikis and documentation platforms</li>
                <li>Runbook and playbook repositories</li>
                <li>Architecture decision records (ADRs)</li>
              </ul>
            </div>

            <div className="category-card">
              <div className="category-header">
                <ShieldIcon />
                <h3>Identity, Access & Collaboration</h3>
              </div>
              <ul>
                <li>Identity providers (SSO / SAML / OIDC)</li>
                <li>Chat and collaboration tools (for war rooms, alerts, and updates)</li>
                <li>Ticketing and service management systems</li>
              </ul>
            </div>

            <div className="category-card">
              <div className="category-header">
                <CloudIcon />
                <h3>Cloud & Infrastructure</h3>
              </div>
              <ul>
                <li>Public cloud providers</li>
                <li>Container orchestration platforms</li>
                <li>Infrastructure-as-code systems</li>
                <li>Configuration management tools</li>
              </ul>
            </div>
          </div>
        </section>

        {/* How Integrations Work Section */}
        <section id="how-it-works" className="partners-section">
          <div className="section-header">
            <div className="section-icon">
              <ApiIcon />
            </div>
            <h2>How Integrations Work</h2>
          </div>

          <div className="how-it-works-content">
            <div className="how-card">
              <div className="how-card-header">
                <LockIcon />
                <h3>Secure Connections</h3>
              </div>
              <p>Integrations are established using:</p>
              <ul>
                <li>API keys, OAuth, or service accounts</li>
                <li>Scopes and permissions configured by the customer</li>
                <li>Secure network channels (e.g., HTTPS, VPN, or private links where applicable)</li>
              </ul>
              <div className="customer-control">
                <h4>Customers retain control over:</h4>
                <ul>
                  <li><CheckCircleIcon /> Which tools are connected</li>
                  <li><CheckCircleIcon /> Which projects, repos, or services are in scope</li>
                  <li><CheckCircleIcon /> Which actions DEV-O is allowed to perform</li>
                </ul>
              </div>
            </div>

            <div className="how-card">
              <div className="how-card-header">
                <WebhookIcon />
                <h3>Events & Webhooks</h3>
              </div>
              <p>DEV-O can receive events via webhooks or polling, and can send events to partner systems to:</p>
              <ul>
                <li>Keep incident and service status in sync</li>
                <li>Trigger downstream automations</li>
                <li>Annotate records with context from the knowledge graph</li>
              </ul>
            </div>

            <div className="how-card">
              <div className="how-card-header">
                <ApiIcon />
                <h3>Extensibility & APIs</h3>
              </div>
              <p>For custom integrations, DEV-O offers:</p>
              <ul>
                <li>REST APIs for services, incidents, events, and knowledge graph entities</li>
                <li>Webhook support for outbound notifications</li>
                <li>A growing set of SDKs and client libraries (see Developer & API Docs)</li>
              </ul>
              <p className="how-card-note">
                Partners and customers can build custom adapters to plug bespoke systems into DEV-O.
              </p>
            </div>
          </div>
        </section>

        {/* Becoming a Partner Section */}
        <section id="become-partner" className="partners-section">
          <div className="section-header">
            <div className="section-icon">
              <RocketIcon />
            </div>
            <h2>Becoming a DEV-O Partner</h2>
          </div>
          <p className="section-intro">
            If you're a technology provider, integrator, consultancy, or channel partner interested in working with DEV-O, we'd love to talk.
          </p>

          <div className="partnership-steps">
            <h3>Typical Partnership Steps</h3>
            <div className="steps-timeline">
              <div className="step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h4>Intro & Alignment</h4>
                  <p>We explore your offerings, customer base, and how DEV-O can complement them.</p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h4>Integration & Use Cases</h4>
                  <p>We identify key joint use cases and design the integration or solution pattern.</p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h4>Technical Enablement</h4>
                  <p>We provide access to sandbox environments, documentation, and technical contacts.</p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h4>Go-to-Market & Co-Selling</h4>
                  <p>We define how to bring the combined solution to customers (joint marketing, sales plays, reference architectures).</p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">5</div>
                <div className="step-content">
                  <h4>Ongoing Collaboration</h4>
                  <p>Regular check-ins, roadmap discussions, and shared customer feedback shape future work.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="partner-tiers">
            <h3>Partner Program</h3>
            <p>As we grow, we plan to offer structured partner tiers:</p>
            <div className="tiers-grid">
              <div className="tier-card">
                <div className="tier-badge">Technology Partner</div>
                <p>Verified integrations and joint technical validation</p>
              </div>
              <div className="tier-card">
                <div className="tier-badge">Solution & SI Partner</div>
                <p>Certified implementation and consulting partners</p>
              </div>
              <div className="tier-card">
                <div className="tier-badge">Channel Partner / MSP</div>
                <p>Organizations that resell or embed DEV-O in their own services</p>
              </div>
            </div>
            <p className="tiers-note">Details can be tailored to specific regions and industries.</p>
          </div>
        </section>

        {/* For Existing Customers Section */}
        <section id="existing-customers" className="partners-section">
          <div className="section-header">
            <div className="section-icon">
              <UsersIcon />
            </div>
            <h2>For Existing DEV-O Customers</h2>
          </div>
          <div className="existing-customers-content">
            <p>If you're already using DEV-O and:</p>
            <ul className="customer-needs">
              <li><CheckCircleIcon /> Want to connect a new tool</li>
              <li><CheckCircleIcon /> Need help designing a custom integration</li>
              <li><CheckCircleIcon /> Would like us to work with one of your existing vendors or partners</li>
            </ul>
            <p>Please contact your DEV-O representative or email us:</p>
            <div className="customer-contacts">
              <a href="mailto:tech@dev-o.ai" className="contact-link">
                <MailIcon />
                <div>
                  <span className="contact-label">Technical & Integration Support</span>
                  <span className="contact-email">tech@dev-o.ai</span>
                </div>
              </a>
              <a href="mailto:support@dev-o.ai" className="contact-link">
                <MailIcon />
                <div>
                  <span className="contact-label">Customer Support</span>
                  <span className="contact-email">support@dev-o.ai</span>
                </div>
              </a>
            </div>
            <p className="customer-note">
              We'll help you map out the best integration pattern and, where relevant, involve our partner team.
            </p>
          </div>
        </section>

        {/* Contact Section */}
        <section id="contact" className="partners-section contact-section">
          <div className="section-header">
            <div className="section-icon">
              <MailIcon />
            </div>
            <h2>Partner & Integration Contact</h2>
          </div>
          <div className="contact-content">
            <div className="contact-cards">
              <a href="mailto:partners@dev-o.ai" className="contact-card primary">
                <MailIcon />
                <div>
                  <span className="contact-label">Partners & Alliances</span>
                  <span className="contact-email">partners@dev-o.ai</span>
                </div>
              </a>
                          <a href="mailto:hello@dev-o.ai" className="contact-card">
                <MailIcon />
                <div>
                  <span className="contact-label">General Inquiries</span>
                  <span className="contact-email">hello@dev-o.ai</span>
                </div>
              </a>
            </div>
            <div className="mailing-address">
              <MapPinIcon />
              <div>
                <strong>Mailing Address:</strong>
                <p>
                  Bionicverse Inc.<br />
                  (Attn: Partnerships / DEV-O)<br />
                  5830 E 2nd St, Ste 7000 #9656<br />
                  Casper, Wyoming 82609<br />
                  United States
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="partners-cta-section">
          <div className="partners-cta-content">
            <h2>DEV-O – Digital Engineering Virtual Orchestrator</h2>
            <p className="cta-subtitle">A project by <strong>Bionicverse Inc.</strong> (USA)</p>
            <p className="cta-description">
              We're building an ecosystem where tools, teams, and AI agents work together as one orchestrated system.
            </p>
            <div className="cta-buttons">
              <a href="mailto:partners@dev-o.ai" className="partners-btn-primary">
                Become a Partner
                <ArrowRightIcon />
              </a>
              <Link to="/features" className="partners-btn-secondary">
                Explore Features
              </Link>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="partners-footer">
        <div className="partners-footer-content">
          <div className="partners-footer-brand">
            <Link to="/" className="partners-footer-logo">
              <img src="/src/components/Logo/DEV-O_Logo.png" alt="DEV-O" />
            </Link>
            <p>Digital Engineering Virtual Orchestrator</p>
          </div>
          <div className="partners-footer-links">
            <div className="footer-link-group">
              <h4>Product</h4>
              <Link to="/features">Features</Link>
              <Link to="/pricing">Pricing</Link>
            </div>
            <div className="footer-link-group">
              <h4>Company</h4>
              <Link to="/careers">Careers</Link>
              <Link to="/press">Press</Link>
            </div>
            <div className="footer-link-group">
              <h4>Resources</h4>
              <Link to="/blog">Blog</Link>
              <Link to="/partners">Partners</Link>
            </div>
          </div>
        </div>
        <div className="partners-footer-bottom">
          <p>© {new Date().getFullYear()} DEV-O by Bionicverse Inc. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default PartnersPage;
