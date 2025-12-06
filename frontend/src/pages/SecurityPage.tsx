import { Link } from 'react-router-dom';
import Logo from '../components/Logo/Logo';
import Footer from '../components/Footer/Footer';
import './SecurityPage.css';

// SVG Icon Components
const ShieldIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
  </svg>
);

const LockIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
  </svg>
);

const KeyIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/>
  </svg>
);

const EyeIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
    <circle cx="12" cy="12" r="3"/>
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

const ServerIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="2" width="20" height="8" rx="2" ry="2"/>
    <rect x="2" y="14" width="20" height="8" rx="2" ry="2"/>
    <line x1="6" y1="6" x2="6.01" y2="6"/>
    <line x1="6" y1="18" x2="6.01" y2="18"/>
  </svg>
);

const DatabaseIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <ellipse cx="12" cy="5" rx="9" ry="3"/>
    <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/>
    <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
  </svg>
);

const CodeIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="16,18 22,12 16,6"/>
    <polyline points="8,6 2,12 8,18"/>
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

const CloudIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>
  </svg>
);

const CheckCircleIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
    <polyline points="22,4 12,14.01 9,11.01"/>
  </svg>
);

const AlertTriangleIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
    <line x1="12" y1="9" x2="12" y2="13"/>
    <line x1="12" y1="17" x2="12.01" y2="17"/>
  </svg>
);

const RefreshIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23,4 23,10 17,10"/>
    <polyline points="1,20 1,14 7,14"/>
    <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
  </svg>
);

const FileTextIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14,2 14,8 20,8"/>
    <line x1="16" y1="13" x2="8" y2="13"/>
    <line x1="16" y1="17" x2="8" y2="17"/>
    <polyline points="10,9 9,9 8,9"/>
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

const SecurityPage = () => {
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="security-page">
      {/* Navigation */}
      <nav className="security-nav">
        <div className="security-nav-container">
          <Link to="/" className="security-logo">
            <Logo size={40} showText={false} />
          </Link>
          <div className="security-nav-links">
            <Link to="/features">Features</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/partners">Partners</Link>
            <Link to="/blog">Blog</Link>
          </div>
          <Link to="/login" className="security-nav-cta">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="security-hero">
        <div className="security-hero-content">
          <div className="security-hero-badge">
            <ShieldIcon />
            <span>Security & Trust</span>
          </div>
          <h1>Security and Trust Are Core to DEV-O</h1>
          <p>
            This page explains how Bionicverse Inc. (USA), the company behind DEV-O, approaches security, 
            compliance, and data protection so you can confidently use DEV-O as a Digital Engineering 
            Virtual Orchestrator for mission-critical systems.
          </p>
          <div className="security-hero-note">
            <AlertTriangleIcon />
            <span>
              This page is an overview, not a legally binding document. It should be read alongside our{' '}
              <Link to="/privacy">Privacy Policy</Link>, <Link to="/terms">Terms of Service</Link>, and any applicable 
              Data Processing Addendum (DPA) or enterprise agreements.
            </span>
          </div>
        </div>
      </section>

      {/* Table of Contents */}
      <aside className="security-toc">
        <h3>On This Page</h3>
        <ul>
          <li><button onClick={() => scrollToSection('principles')}>Security Principles</button></li>
          <li><button onClick={() => scrollToSection('architecture')}>Platform Architecture</button></li>
          <li><button onClick={() => scrollToSection('identity')}>Identity & Access</button></li>
          <li><button onClick={() => scrollToSection('data-protection')}>Data Protection</button></li>
          <li><button onClick={() => scrollToSection('app-security')}>Application Security</button></li>
          <li><button onClick={() => scrollToSection('ai-guardrails')}>AI & Guardrails</button></li>
          <li><button onClick={() => scrollToSection('subprocessors')}>Subprocessors</button></li>
          <li><button onClick={() => scrollToSection('compliance')}>Compliance</button></li>
          <li><button onClick={() => scrollToSection('incident-response')}>Incident Response</button></li>
          <li><button onClick={() => scrollToSection('responsibilities')}>Customer Responsibilities</button></li>
          <li><button onClick={() => scrollToSection('reporting')}>Reporting Issues</button></li>
          <li><button onClick={() => scrollToSection('contact')}>Contact</button></li>
        </ul>
      </aside>

      {/* Main Content */}
      <main className="security-main">
        {/* Security Principles */}
        <section id="principles" className="security-section">
          <div className="section-header">
            <div className="section-number">1</div>
            <h2>Our Security Principles</h2>
          </div>
          <p className="section-intro">We build DEV-O around a few non-negotiable security principles:</p>
          
          <div className="principles-grid">
            <div className="principle-card">
              <div className="principle-number">01</div>
              <h3>Security by Design</h3>
              <p>Security is part of the architecture and development process, not an afterthought.</p>
            </div>
            <div className="principle-card">
              <div className="principle-number">02</div>
              <h3>Defense in Depth</h3>
              <p>Multiple layers of technical and organizational controls protect systems and data.</p>
            </div>
            <div className="principle-card">
              <div className="principle-number">03</div>
              <h3>Least Privilege</h3>
              <p>Access is granted only where necessary, with strong authentication and authorization.</p>
            </div>
            <div className="principle-card">
              <div className="principle-number">04</div>
              <h3>Transparency & Accountability</h3>
              <p>We aim to be clear about how DEV-O works, how data flows, and how we respond to issues.</p>
            </div>
            <div className="principle-card">
              <div className="principle-number">05</div>
              <h3>Human-in-Command</h3>
              <p>AI and automation in DEV-O are designed so humans remain in control of sensitive actions.</p>
            </div>
          </div>
        </section>

        {/* Platform Architecture */}
        <section id="architecture" className="security-section">
          <div className="section-header">
            <div className="section-number">2</div>
            <h2>Platform Architecture & Isolation</h2>
          </div>
          <p className="section-intro">
            DEV-O is designed as a multi-tenant platform with logical separation between customers, 
            built with security and reliability in mind.
          </p>
          
          <div className="architecture-grid">
            <div className="architecture-card">
              <div className="architecture-icon"><DatabaseIcon /></div>
              <h3>Isolated Customer Data</h3>
              <p>Logical separation of customer data at the application and data layers.</p>
            </div>
            <div className="architecture-card">
              <div className="architecture-icon"><ServerIcon /></div>
              <h3>Segregated Environments</h3>
              <p>Separate environments for development, staging, and production.</p>
            </div>
            <div className="architecture-card">
              <div className="architecture-icon"><ShieldIcon /></div>
              <h3>Secure-by-Default</h3>
              <p>Hardened defaults for network, compute, and storage components.</p>
            </div>
            <div className="architecture-card">
              <div className="architecture-icon"><CloudIcon /></div>
              <h3>Network Segmentation</h3>
              <p>Separation of public-facing services and internal management components.</p>
            </div>
          </div>
          
          <div className="architecture-note">
            <FileTextIcon />
            <p>Architecture details can be provided under NDA for security reviews and due diligence.</p>
          </div>
        </section>

        {/* Identity & Access */}
        <section id="identity" className="security-section">
          <div className="section-header">
            <div className="section-number">3</div>
            <h2>Identity, Access & Authentication</h2>
          </div>

          <div className="subsection">
            <h3><KeyIcon /> User Authentication</h3>
            <p>DEV-O supports modern authentication approaches, such as:</p>
            <ul className="feature-list">
              <li>Email/password with industry-standard hashing</li>
              <li>Optional multi-factor authentication (where enabled)</li>
              <li>SSO / SAML / OIDC integration (for enterprise customers)</li>
              <li>Session management with secure cookies and timeouts</li>
            </ul>
          </div>

          <div className="subsection">
            <h3><UsersIcon /> Authorization & Roles</h3>
            <p>Authorization is based on role-based access control (RBAC) and, where needed, more granular permissions.</p>
            <ul className="feature-list">
              <li>Users can be assigned roles (e.g., admin, operator, viewer)</li>
              <li>Access to services, workflows, and data is restricted based on role and configuration</li>
              <li>Sensitive operations can require elevated permissions and approvals</li>
            </ul>
          </div>

          <div className="subsection">
            <h3><LockIcon /> Least Privilege</h3>
            <p>Internally, access to infrastructure, logs, and data is limited to personnel who need it to perform their duties. Access is:</p>
            <div className="access-features">
              <div className="access-item"><CheckCircleIcon /> Role-based</div>
              <div className="access-item"><CheckCircleIcon /> Logged and monitored</div>
              <div className="access-item"><CheckCircleIcon /> Reviewed periodically</div>
            </div>
          </div>
        </section>

        {/* Data Protection */}
        <section id="data-protection" className="security-section">
          <div className="section-header">
            <div className="section-number">4</div>
            <h2>Data Protection & Encryption</h2>
          </div>

          <div className="data-protection-grid">
            <div className="data-card">
              <div className="data-card-header">
                <LockIcon />
                <h3>Data in Transit</h3>
              </div>
              <p>Data in transit between clients and DEV-O is protected using TLS (HTTPS) or equivalent secure transport mechanisms.</p>
            </div>

            <div className="data-card">
              <div className="data-card-header">
                <DatabaseIcon />
                <h3>Data at Rest</h3>
              </div>
              <p>Where applicable, DEV-O uses encryption at rest for databases and storage volumes holding customer data.</p>
            </div>

            <div className="data-card">
              <div className="data-card-header">
                <EyeIcon />
                <h3>Data Minimization</h3>
              </div>
              <p>We aim to collect and store only the data necessary to operate DEV-O and deliver value. Customers can further limit scope by controlling:</p>
              <ul>
                <li>Which tools and repositories are integrated</li>
                <li>Which environments are in scope</li>
                <li>What categories of data are sent through DEV-O</li>
              </ul>
            </div>
          </div>

          <p className="section-note">
            For more information on personal data and GDPR, see the <Link to="/privacy">Privacy Policy</Link>.
          </p>
        </section>

        {/* Application Security */}
        <section id="app-security" className="security-section">
          <div className="section-header">
            <div className="section-number">5</div>
            <h2>Application Security</h2>
          </div>

          <div className="app-security-content">
            <div className="app-security-card">
              <h3><CodeIcon /> Secure Development Practices</h3>
              <p>Our development processes incorporate:</p>
              <ul>
                <li>Code reviews and peer review for critical changes</li>
                <li>Use of version control, CI/CD, and automated checks</li>
                <li>Static analysis and dependency scanning (where applicable)</li>
                <li>Separation of duties between development, staging, and production operations</li>
              </ul>
            </div>

            <div className="app-security-card">
              <h3><AlertTriangleIcon /> Vulnerability Management</h3>
              <p>We monitor for vulnerabilities in our stack and dependencies and aim to:</p>
              <ul>
                <li>Evaluate risk and prioritize remediation</li>
                <li>Patch and update components in a timely manner</li>
                <li>Track fixes through our internal ticketing and review processes</li>
              </ul>
              <div className="disclosure-box">
                <MailIcon />
                <p>We encourage responsible disclosure of security issues via <a href="mailto:security@dev-o.ai">security@dev-o.ai</a></p>
              </div>
            </div>

            <div className="app-security-card">
              <h3><CheckCircleIcon /> Testing & Quality</h3>
              <p>We combine automated and manual testing approaches such as:</p>
              <ul>
                <li>Unit and integration tests</li>
                <li>End-to-end and regression tests</li>
                <li>Targeted security and resilience testing for critical components</li>
              </ul>
            </div>
          </div>
        </section>

        {/* AI & Guardrails */}
        <section id="ai-guardrails" className="security-section">
          <div className="section-header">
            <div className="section-number">6</div>
            <h2>AI, Agents & Guardrails</h2>
          </div>
          <p className="section-intro">
            DEV-O orchestrates AI agents and automations across engineering workflows. 
            Security and governance are built into this layer.
          </p>

          <div className="ai-content">
            <div className="ai-card">
              <h3><CpuIcon /> Grounded & Scoped AI</h3>
              <ul>
                <li>AI agents operate using context provided by the knowledge graph and relevant integrations</li>
                <li>Access to data is restricted according to roles, environments, and customer configuration</li>
                <li>Customers can control what data is in scope for AI and which actions agents are allowed to perform</li>
              </ul>
            </div>

            <div className="ai-card">
              <h3><UsersIcon /> Modes of Operation</h3>
              <p>DEV-O supports multiple modes of AI-assisted operation:</p>
              <div className="modes-grid">
                <div className="mode-item">
                  <span className="mode-badge advisory">Advisory</span>
                  <p>AI suggests actions; humans execute</p>
                </div>
                <div className="mode-item">
                  <span className="mode-badge assisted">Assisted</span>
                  <p>AI prepares actions; humans review and approve</p>
                </div>
                <div className="mode-item">
                  <span className="mode-badge orchestrated">Orchestrated</span>
                  <p>Predefined workflows may be executed automatically under clear policies</p>
                </div>
              </div>
              <p className="mode-note">
                By default, we encourage human-in-command patterns, especially for production-impacting changes.
              </p>
            </div>

            <div className="ai-card">
              <h3><CloudIcon /> AI Providers & Data Handling</h3>
              <p>When external AI models or providers are used, we work with customers to:</p>
              <ul>
                <li>Define what data may be shared with those providers</li>
                <li>Use secure channels and, where possible, regional or private deployments</li>
                <li>Reflect relevant terms in contracts and DPAs</li>
              </ul>
              <p className="ai-note">
                See the <Link to="/privacy">Privacy Policy</Link> for more detail on data flows.
              </p>
            </div>
          </div>
        </section>

        {/* Subprocessors */}
        <section id="subprocessors" className="security-section">
          <div className="section-header">
            <div className="section-number">7</div>
            <h2>Subprocessors & Third-Party Services</h2>
          </div>
          <p className="section-intro">
            To operate DEV-O, Bionicverse may use subprocessors (third-party providers) for:
          </p>
          <ul className="subprocessor-list">
            <li>Hosting and infrastructure</li>
            <li>Monitoring and observability</li>
            <li>Support and ticketing systems</li>
            <li>Communication and email services</li>
          </ul>
          <p>Each subprocessor is:</p>
          <div className="subprocessor-features">
            <div className="subprocessor-item"><CheckCircleIcon /> Evaluated for security and privacy practices</div>
            <div className="subprocessor-item"><CheckCircleIcon /> Bound by contractual obligations to protect data</div>
            <div className="subprocessor-item"><CheckCircleIcon /> Included in our DPA and related documentation</div>
          </div>
          <p className="section-note">
            A list of core subprocessors can be provided to customers and may be maintained separately as part of our trust documentation.
          </p>
        </section>

        {/* Compliance */}
        <section id="compliance" className="security-section">
          <div className="section-header">
            <div className="section-number">8</div>
            <h2>Compliance & Certifications (Roadmap)</h2>
          </div>
          <p className="section-intro">
            DEV-O and Bionicverse are committed to aligning with recognized security and compliance standards over time.
          </p>
          <p>Examples of frameworks and certifications we may pursue or align with include:</p>
          
          <div className="compliance-grid">
            <div className="compliance-card">
              <div className="compliance-badge">ISO 27001</div>
              <p>Information Security Management</p>
            </div>
            <div className="compliance-card">
              <div className="compliance-badge">SOC 2</div>
              <p>Security, availability, and confidentiality controls</p>
            </div>
            <div className="compliance-card">
              <div className="compliance-badge">GDPR / UK GDPR</div>
              <p>Data protection compliance for EEA/UK customers</p>
            </div>
            <div className="compliance-card">
              <div className="compliance-badge">Other Frameworks</div>
              <p>Regional / industry frameworks as needs evolve</p>
            </div>
          </div>

          <p className="section-note">
            Up-to-date information on certifications, audits, and reports can be shared with customers under NDA upon request.
          </p>
        </section>

        {/* Incident Response */}
        <section id="incident-response" className="security-section">
          <div className="section-header">
            <div className="section-number">9</div>
            <h2>Business Continuity & Incident Response</h2>
          </div>

          <div className="incident-content">
            <div className="incident-card">
              <h3><RefreshIcon /> Business Continuity & Backups</h3>
              <p>We maintain processes designed to:</p>
              <ul>
                <li>Backup key systems and data at regular intervals</li>
                <li>Store backups in secure, redundant locations where applicable</li>
                <li>Support restoration and continuity in the event of certain failures</li>
              </ul>
            </div>

            <div className="incident-card">
              <h3><AlertTriangleIcon /> Incident Detection & Response</h3>
              <p>We monitor DEV-O for security and availability incidents. Our incident response practices include:</p>
              <ol className="incident-steps">
                <li><strong>Detection & Triage</strong> – Identify potential incidents via monitoring, alerts, or reports</li>
                <li><strong>Containment & Mitigation</strong> – Limit impact and stabilize systems</li>
                <li><strong>Investigation</strong> – Identify root cause and affected components</li>
                <li><strong>Communication</strong> – Notify affected customers where required, and provide updates</li>
                <li><strong>Post-Incident Review</strong> – Use DEV-O's own workflows to capture learnings and improve our systems</li>
              </ol>
              <p className="incident-note">
                Security incidents involving personal data are handled in accordance with applicable laws and our contractual commitments.
              </p>
            </div>
          </div>
        </section>

        {/* Customer Responsibilities */}
        <section id="responsibilities" className="security-section">
          <div className="section-header">
            <div className="section-number">10</div>
            <h2>Customer Responsibilities</h2>
          </div>
          <p className="section-intro">Security and compliance are shared responsibilities.</p>
          <p>Customers are responsible for:</p>
          <ul className="responsibility-list">
            <li><CheckCircleIcon /> Managing user accounts, roles, and access within their organization</li>
            <li><CheckCircleIcon /> Choosing and configuring integrations and data sources</li>
            <li><CheckCircleIcon /> Ensuring their use of DEV-O complies with applicable laws and internal policies</li>
            <li><CheckCircleIcon /> Implementing additional controls in their environment (e.g., VPNs, endpoint security, internal monitoring)</li>
          </ul>
          <p className="section-note">
            We work with you to align DEV-O's configuration with your security posture and requirements.
          </p>
        </section>

        {/* Reporting Issues */}
        <section id="reporting" className="security-section">
          <div className="section-header">
            <div className="section-number">11</div>
            <h2>Reporting Security Issues</h2>
          </div>
          <p className="section-intro">
            If you discover or suspect a security vulnerability, data exposure, or other issue related to DEV-O, please contact us promptly:
          </p>
          
          <div className="reporting-box">
            <a href="mailto:security@dev-o.ai" className="reporting-email">
              <MailIcon />
              <div>
                <span className="reporting-label">Security Email</span>
                <span className="reporting-address">security@dev-o.ai</span>
              </div>
            </a>
          </div>

          <p>Include as much detail as you can (without sharing sensitive data unnecessarily):</p>
          <ul className="reporting-list">
            <li>Description of the issue</li>
            <li>Steps to reproduce, if known</li>
            <li>Relevant environment or context</li>
            <li>Any immediate impact observed</li>
          </ul>
          <p className="section-note">
            We appreciate responsible disclosure and will work with you to address issues promptly.
          </p>
        </section>

        {/* Contact */}
        <section id="contact" className="security-section contact-section">
          <div className="section-header">
            <div className="section-number">12</div>
            <h2>Contact & Trust Queries</h2>
          </div>
          <p className="section-intro">
            For security, compliance, or trust-related questions, you can contact us at:
          </p>

          <div className="contact-grid">
            <a href="mailto:security@dev-o.ai" className="contact-card">
              <MailIcon />
              <div>
                <span className="contact-label">Security & Technical</span>
                <span className="contact-email">security@dev-o.ai</span>
                <span className="contact-alt">or tech@dev-o.ai</span>
              </div>
            </a>
            <a href="mailto:privacy@dev-o.ai" className="contact-card">
              <MailIcon />
              <div>
                <span className="contact-label">Data Protection & Privacy</span>
                <span className="contact-email">privacy@dev-o.ai</span>
                <span className="contact-alt">or legal@dev-o.ai</span>
              </div>
            </a>
          </div>

          <div className="mailing-address">
            <MapPinIcon />
            <div>
              <strong>Mailing Address:</strong>
              <p>
                Bionicverse Inc.<br />
                (Attn: Security & Compliance / DEV-O)<br />
                5830 E 2nd St, Ste 7000 #9656<br />
                Casper, Wyoming 82609<br />
                United States
              </p>
            </div>
          </div>

          <p className="contact-note">
            We are happy to collaborate with your security, compliance, and legal teams to answer due diligence questionnaires, 
            share additional documentation under NDA, and design configurations that meet your organization's needs.
          </p>
        </section>

        {/* CTA Section */}
        <section className="security-cta-section">
          <div className="security-cta-content">
            <h2>DEV-O – Digital Engineering Virtual Orchestrator</h2>
            <p className="cta-subtitle">A project by <strong>Bionicverse Inc.</strong> (USA)</p>
            <p className="cta-description">
              Our goal is simple: help you build AI-native engineering operations without compromising security, compliance, or trust.
            </p>
            <div className="cta-buttons">
              <Link to="/login" className="security-btn-primary">
                Get Started
                <ArrowRightIcon />
              </Link>
              <Link to="/features" className="security-btn-secondary">
                Explore Features
              </Link>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default SecurityPage;
