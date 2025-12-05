import { Link } from 'react-router-dom';
import { PageIcon } from '../components/Icons/PageIcon';
import './PartnersPage.css';

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
            <PageIcon name="network" />
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
              <PageIcon name="arrow" size={18} />
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
              <PageIcon name="handshake" />
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
                <li><PageIcon name="code" size={18} /> Code hosting and CI/CD pipelines</li>
                <li><PageIcon name="clipboard" size={18} /> Issue trackers and project tools</li>
                <li><PageIcon name="activity" size={18} /> Observability, logging, and incident management</li>
                <li><PageIcon name="book" size={18} /> Documentation and knowledge systems</li>
                <li><PageIcon name="cloud" size={18} /> Cloud and infrastructure platforms</li>
              </ul>
            </div>
            <div className="partner-benefits">
              <h3>By integrating with DEV-O, partners can:</h3>
              <div className="benefits-grid">
                <div className="benefit-card">
                  <div className="benefit-icon"><PageIcon name="bolt" /></div>
                  <h4>Increase Tool Value</h4>
                  <p>Plug into a broader orchestration and AI layer to amplify your tool's capabilities.</p>
                </div>
                <div className="benefit-card">
                  <div className="benefit-icon"><PageIcon name="users" /></div>
                  <h4>Reach New Customers</h4>
                  <p>Connect with organizations standardizing on DEV-O as their engineering control plane.</p>
                </div>
                <div className="benefit-card">
                  <div className="benefit-icon"><PageIcon name="network" /></div>
                  <h4>Enable AI-Native Workflows</h4>
                  <p>Power workflows that span multiple products and teams seamlessly.</p>
                </div>
                <div className="benefit-card">
                  <div className="benefit-icon"><PageIcon name="code" /></div>
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
              <PageIcon name="users" />
            </div>
            <h2>Types of Partners</h2>
          </div>
          <p className="section-intro">We work with a variety of partners to build a rich ecosystem around DEV-O.</p>
          
          <div className="partner-types-grid">
            <div className="partner-type-card">
              <div className="partner-type-header">
                <div className="partner-type-icon"><PageIcon name="code" /></div>
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
                <div className="partner-type-icon"><PageIcon name="cloud" /></div>
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
                <div className="partner-type-icon"><PageIcon name="users" /></div>
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
                <div className="partner-type-icon"><PageIcon name="shopping" /></div>
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
                <div className="partner-type-icon"><PageIcon name="star" /></div>
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
              <PageIcon name="network" />
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
                  <PageIcon name="database" />
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
                  <PageIcon name="share" />
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
                  <PageIcon name="bolt" />
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
            <PageIcon name="shield" />
            <p>All of this is controlled by <strong>permissions</strong>, <strong>policies</strong>, and <strong>explicit configuration</strong>.</p>
          </div>
        </section>

        {/* Integration Categories Section */}
        <section id="categories" className="partners-section">
          <div className="section-header">
            <div className="section-icon">
              <PageIcon name="server" />
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
                <PageIcon name="git" />
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
                <PageIcon name="clipboard" />
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
                <PageIcon name="activity" />
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
                <PageIcon name="book" />
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
                <PageIcon name="shield" />
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
                <PageIcon name="cloud" />
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
              <PageIcon name="code" />
            </div>
            <h2>How Integrations Work</h2>
          </div>

          <div className="how-it-works-content">
            <div className="how-card">
              <div className="how-card-header">
                <PageIcon name="lock" />
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
                  <li><PageIcon name="check" size={18} /> Which tools are connected</li>
                  <li><PageIcon name="check" size={18} /> Which projects, repos, or services are in scope</li>
                  <li><PageIcon name="check" size={18} /> Which actions DEV-O is allowed to perform</li>
                </ul>
              </div>
            </div>

            <div className="how-card">
              <div className="how-card-header">
                <PageIcon name="webhook" />
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
                <PageIcon name="code" />
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
              <PageIcon name="rocket" />
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
              <PageIcon name="users" />
            </div>
            <h2>For Existing DEV-O Customers</h2>
          </div>
          <div className="existing-customers-content">
            <p>If you're already using DEV-O and:</p>
            <ul className="customer-needs">
              <li><PageIcon name="check" size={18} /> Want to connect a new tool</li>
              <li><PageIcon name="check" size={18} /> Need help designing a custom integration</li>
              <li><PageIcon name="check" size={18} /> Would like us to work with one of your existing vendors or partners</li>
            </ul>
            <p>Please contact your DEV-O representative or email us:</p>
            <div className="customer-contacts">
              <a href="mailto:tech@dev-o.ai" className="contact-link">
                <PageIcon name="mail" />
                <div>
                  <span className="contact-label">Technical & Integration Support</span>
                  <span className="contact-email">tech@dev-o.ai</span>
                </div>
              </a>
              <a href="mailto:support@dev-o.ai" className="contact-link">
                <PageIcon name="mail" />
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
              <PageIcon name="mail" />
            </div>
            <h2>Partner & Integration Contact</h2>
          </div>
          <div className="contact-content">
            <div className="contact-cards">
              <a href="mailto:partners@dev-o.ai" className="contact-card primary">
                <PageIcon name="mail" />
                <div>
                  <span className="contact-label">Partners & Alliances</span>
                  <span className="contact-email">partners@dev-o.ai</span>
                </div>
              </a>
                          <a href="mailto:hello@dev-o.ai" className="contact-card">
                <PageIcon name="mail" />
                <div>
                  <span className="contact-label">General Inquiries</span>
                  <span className="contact-email">hello@dev-o.ai</span>
                </div>
              </a>
            </div>
            <div className="mailing-address">
              <PageIcon name="map" />
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
                <PageIcon name="arrow" size={18} />
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
