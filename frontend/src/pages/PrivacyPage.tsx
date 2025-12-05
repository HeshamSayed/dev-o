import { Link } from 'react-router-dom';
import './PrivacyPage.css';

// SVG Icon Components
const ShieldIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
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

const EyeIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
    <circle cx="12" cy="12" r="3"/>
  </svg>
);

const PrivacyPage = () => {
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="privacy-page">
      {/* Navigation */}
      <nav className="privacy-nav">
        <div className="privacy-nav-container">
          <Link to="/" className="privacy-logo">
            <img src="/src/components/Logo/logo+icon.png" alt="DEV-O" className="privacy-logo-image" />
          </Link>
          <div className="privacy-nav-links">
            <Link to="/features">Features</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/partners">Partners</Link>
            <Link to="/blog">Blog</Link>
          </div>
          <Link to="/login" className="privacy-nav-cta">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="privacy-hero">
        <div className="privacy-hero-content">
          <div className="privacy-hero-badge">
            <EyeIcon />
            <span>Privacy</span>
          </div>
          <h1>Privacy Policy</h1>
          <p>
            DEV-O is a project operated by Bionicverse Inc. (USA) ("Bionicverse", "we", "us", or "our"). 
            This Privacy Policy describes how we collect, use, disclose, and protect personal information.
          </p>
          <p className="privacy-hero-note">
            We are committed to handling personal information responsibly and transparently.
          </p>
        </div>
      </section>

      {/* Table of Contents */}
      <aside className="privacy-toc">
        <h3>Contents</h3>
        <ul>
          <li><button onClick={() => scrollToSection('controller')}>1. Data Controller</button></li>
          <li><button onClick={() => scrollToSection('scope')}>2. Scope</button></li>
          <li><button onClick={() => scrollToSection('information')}>3. Information We Collect</button></li>
          <li><button onClick={() => scrollToSection('how-we-use')}>4. How We Use Info</button></li>
          <li><button onClick={() => scrollToSection('legal-bases')}>5. Legal Bases</button></li>
          <li><button onClick={() => scrollToSection('sharing')}>6. Sharing Info</button></li>
          <li><button onClick={() => scrollToSection('transfers')}>7. International Transfers</button></li>
          <li><button onClick={() => scrollToSection('cookies')}>8. Cookies</button></li>
          <li><button onClick={() => scrollToSection('retention')}>9. Data Retention</button></li>
          <li><button onClick={() => scrollToSection('rights')}>10. Your Rights</button></li>
          <li><button onClick={() => scrollToSection('children')}>11. Children's Privacy</button></li>
          <li><button onClick={() => scrollToSection('security')}>12. Security</button></li>
          <li><button onClick={() => scrollToSection('marketing')}>13. Marketing</button></li>
          <li><button onClick={() => scrollToSection('changes')}>14. Changes</button></li>
          <li><button onClick={() => scrollToSection('contact')}>15. Contact Us</button></li>
        </ul>
      </aside>

      {/* Main Content */}
      <main className="privacy-main">
        {/* Section 1 */}
        <section id="controller" className="privacy-section">
          <h2>1. Who We Are (Data Controller)</h2>
          <p>For the purposes of applicable data protection laws, the entity responsible for your personal information is:</p>
          <div className="company-info">
            <p><strong>Bionicverse Inc.</strong></p>
            <p>(Operating the DEV-O platform)</p>
            <p>5830 E 2nd St, Ste 7000 #9656</p>
            <p>Casper, Wyoming 82609</p>
            <p>United States</p>
          </div>
          <p>If you have questions about this Privacy Policy, please contact us at:</p>
          <div className="contact-emails">
            <a href="mailto:privacy@dev-o.ai">privacy@dev-o.ai</a>
            <span> or </span>
            <a href="mailto:legal@dev-o.ai">legal@dev-o.ai</a>
          </div>
        </section>

        {/* Section 2 */}
        <section id="scope" className="privacy-section">
          <h2>2. Scope of This Privacy Policy</h2>
          <p>This Privacy Policy applies to:</p>
          <ul>
            <li>Visitors to our website(s),</li>
            <li>Users of the DEV-O platform and related services,</li>
            <li>Representatives of our customers, partners, and suppliers,</li>
            <li>Individuals who contact us (e.g., via email, forms, or events).</li>
          </ul>
          <p>This Privacy Policy does not apply to:</p>
          <ul>
            <li>Third-party websites, services, or platforms that we do not control,</li>
            <li>Data that our customers input into DEV-O where they act as the data controller (we process such data as a processor/service provider on their instructions).</li>
          </ul>
          <p className="note">
            If you use DEV-O as part of your employer's or organization's account, your use may also be governed by that organization's own policies.
          </p>
        </section>

        {/* Section 3 */}
        <section id="information" className="privacy-section">
          <h2>3. Information We Collect</h2>
          <p>We collect information in several ways, depending on how you interact with DEV-O.</p>

          <h3>3.1 Information You Provide to Us</h3>
          <p>This includes information you provide directly, for example when you:</p>
          <ul>
            <li>Fill out a contact or demo request form,</li>
            <li>Create or manage an account,</li>
            <li>Use the DEV-O platform and input data,</li>
            <li>Subscribe to our newsletters or marketing communications,</li>
            <li>Apply for a job or express interest in working with us,</li>
            <li>Communicate with us via email, chat, or other channels.</li>
          </ul>
          <p>Examples of information you may provide:</p>
          <ul className="info-categories">
            <li><strong>Identification and contact details</strong> – name, email address, company, role/title, phone number.</li>
            <li><strong>Account information</strong> – username, credentials (stored in a secure form), profile details.</li>
            <li><strong>Professional information</strong> – organization, department, area of responsibility.</li>
            <li><strong>Support and communication data</strong> – messages, feedback, or other details you share.</li>
            <li><strong>Job application information</strong> – resume/CV, work history, education.</li>
          </ul>

          <h3>3.2 Information We Collect Automatically</h3>
          <p>When you visit our websites or use the DEV-O platform, we may automatically collect certain information, such as:</p>
          <ul>
            <li><strong>Usage data</strong> – pages visited, features used, clicks, timestamps, referring URLs.</li>
            <li><strong>Device and technical data</strong> – IP address, browser type and version, operating system, device identifiers, language settings.</li>
            <li><strong>Log data</strong> – system logs, access logs, error logs, and performance metrics.</li>
          </ul>

          <h3>3.3 Information from Integrations & Third Parties</h3>
          <p>
            If your organization connects DEV-O to other tools (such as code repositories, issue trackers, 
            observability platforms, or identity providers), DEV-O may process information from those systems 
            as configured by your organization.
          </p>
          <p>Examples include:</p>
          <ul>
            <li>Metadata about services, components, and deployments,</li>
            <li>Ticket and incident information,</li>
            <li>Logs, metrics, and event data,</li>
            <li>User and team identifiers/roles from your identity system.</li>
          </ul>

          <h3>3.4 Sensitive Information</h3>
          <p>
            We do not intentionally seek to collect sensitive personal information (such as information on health, 
            religion, or political opinions) through DEV-O unless required by law or explicitly provided by you with your consent.
          </p>
          <p className="note">
            If you believe we have collected such information inadvertently, please contact us so we can review and address it.
          </p>
        </section>

        {/* Section 4 */}
        <section id="how-we-use" className="privacy-section">
          <h2>4. How We Use Personal Information</h2>
          <p>We use personal information for the following purposes:</p>
          
          <div className="use-cases">
            <div className="use-case">
              <h4>To provide and operate the DEV-O platform</h4>
              <ul>
                <li>Creating and managing user accounts</li>
                <li>Enabling features, workflows, and integrations</li>
                <li>Processing customer and user requests</li>
              </ul>
            </div>
            <div className="use-case">
              <h4>To maintain and improve our services</h4>
              <ul>
                <li>Monitoring performance and availability</li>
                <li>Debugging and troubleshooting</li>
                <li>Developing new features and enhancements</li>
              </ul>
            </div>
            <div className="use-case">
              <h4>To communicate with you</h4>
              <ul>
                <li>Responding to inquiries and support requests</li>
                <li>Sending service-related notices</li>
                <li>Sending marketing updates where permitted</li>
              </ul>
            </div>
            <div className="use-case">
              <h4>To support security and prevent misuse</h4>
              <ul>
                <li>Detecting and preventing fraud, abuse, or security incidents</li>
                <li>Enforcing our terms and policies</li>
              </ul>
            </div>
            <div className="use-case">
              <h4>To comply with legal obligations</h4>
              <ul>
                <li>Responding to lawful requests from authorities</li>
                <li>Meeting regulatory or compliance requirements</li>
              </ul>
            </div>
            <div className="use-case">
              <h4>For recruitment and hiring</h4>
              <ul>
                <li>Evaluating job applications</li>
                <li>Managing recruitment and related processes</li>
              </ul>
            </div>
          </div>

          <p className="note">
            We may aggregate or de-identify information for analytics, research, or product improvement. 
            Where we do so, we take steps to ensure individuals cannot reasonably be re-identified.
          </p>
        </section>

        {/* Section 5 */}
        <section id="legal-bases" className="privacy-section">
          <h2>5. Legal Bases for Processing (EEA/UK)</h2>
          <p>
            If you are located in the European Economic Area (EEA), the United Kingdom (UK), or similar jurisdictions, 
            we process personal information under one or more of the following legal bases:
          </p>
          <ul className="legal-bases-list">
            <li><strong>Performance of a contract</strong> – when processing is necessary to provide the services you or your organization requested.</li>
            <li><strong>Legitimate interests</strong> – for example, to maintain and improve our services, secure our systems, and communicate with you about relevant updates (where these interests are not overridden by your rights).</li>
            <li><strong>Consent</strong> – where required, for certain marketing communications or optional features. You can withdraw consent at any time.</li>
            <li><strong>Compliance with legal obligations</strong> – where processing is necessary to comply with applicable laws.</li>
          </ul>
        </section>

        {/* Section 6 */}
        <section id="sharing" className="privacy-section">
          <h2>6. How We Share Personal Information</h2>
          <p>We may share personal information in the following circumstances:</p>

          <h3>Within Bionicverse Group / Affiliates</h3>
          <p>We may share information with related entities that help operate DEV-O, always under appropriate safeguards.</p>

          <h3>Service Providers & Subprocessors</h3>
          <p>We engage trusted third-party providers for functions such as:</p>
          <ul>
            <li>Hosting and infrastructure,</li>
            <li>Analytics and monitoring,</li>
            <li>Customer support tools,</li>
            <li>Communication services.</li>
          </ul>
          <p className="note">
            These providers may process personal information on our behalf and only in accordance with our instructions 
            and applicable data protection agreements.
          </p>

          <h3>With Your Organization & Other Users</h3>
          <p>
            If you use DEV-O as part of an organization, certain information may be visible to other users in your 
            organization (e.g., your name, email, activity, and contributions within DEV-O).
          </p>

          <h3>Legal & Safety Requirements</h3>
          <p>We may disclose information if we believe it is reasonably necessary to:</p>
          <ul>
            <li>Comply with a law, regulation, or legal request,</li>
            <li>Protect the rights, property, or safety of Bionicverse, our users, or the public,</li>
            <li>Detect, prevent, or address fraud, security, or technical issues.</li>
          </ul>

          <h3>Business Transfers</h3>
          <p>
            In the context of a merger, acquisition, financing, reorganization, or sale of assets, personal information 
            may be transferred as part of the transaction, subject to confidentiality obligations and applicable law.
          </p>

          <div className="important-notice">
            <ShieldIcon />
            <p>
              We do not sell personal information in the sense of many privacy laws (such as the CCPA/CPRA definition) 
              and do not share personal information with third parties for their own direct marketing without your consent.
            </p>
          </div>
        </section>

        {/* Section 7 */}
        <section id="transfers" className="privacy-section">
          <h2>7. International Data Transfers</h2>
          <p>
            Because DEV-O and Bionicverse Inc. operate globally, your personal information may be transferred to, 
            and processed in, countries other than your own.
          </p>
          <p>
            Where we transfer personal information from the EEA/UK or other regions with data transfer restrictions, 
            we implement appropriate safeguards, which may include:
          </p>
          <ul>
            <li>Standard Contractual Clauses (SCCs),</li>
            <li>Other legally recognized transfer mechanisms,</li>
            <li>Additional technical and organizational safeguards.</li>
          </ul>
        </section>

        {/* Section 8 */}
        <section id="cookies" className="privacy-section">
          <h2>8. Cookies & Similar Technologies</h2>
          <p>We use cookies and similar technologies on our websites and platform to:</p>
          <ul>
            <li>Remember your preferences and settings,</li>
            <li>Keep you signed in where applicable,</li>
            <li>Understand how the site and platform are used,</li>
            <li>Improve performance and user experience.</li>
          </ul>
          <p>
            You can typically control cookies through your browser settings (e.g., to block or delete cookies). 
            Some features of our services may not function properly if certain cookies are disabled.
          </p>
          <p className="note">
            Where required by law, we will obtain your consent before using non-essential cookies.
          </p>
        </section>

        {/* Section 9 */}
        <section id="retention" className="privacy-section">
          <h2>9. Data Retention</h2>
          <p>We retain personal information for as long as necessary to:</p>
          <ul>
            <li>Provide the services and fulfill the purposes described in this Policy,</li>
            <li>Comply with our legal and contractual obligations,</li>
            <li>Resolve disputes and enforce agreements.</li>
          </ul>
          <p>
            Retention periods may vary depending on the type of data and context. When personal information is no longer 
            needed, we will take reasonable steps to delete, anonymize, or securely store it in a form that no longer identifies you.
          </p>
        </section>

        {/* Section 10 */}
        <section id="rights" className="privacy-section">
          <h2>10. Your Rights & Choices</h2>
          <p>Depending on your location and applicable law, you may have certain rights regarding your personal information, such as:</p>
          <ul className="rights-list">
            <li><strong>Access</strong> – request a copy of the personal information we hold about you.</li>
            <li><strong>Correction</strong> – ask us to correct inaccurate or incomplete information.</li>
            <li><strong>Deletion</strong> – request deletion of personal information in certain circumstances.</li>
            <li><strong>Restriction</strong> – ask us to limit the processing of your information in certain cases.</li>
            <li><strong>Objection</strong> – object to certain processing (for example, direct marketing or processing based on legitimate interests).</li>
            <li><strong>Data portability</strong> – request a machine-readable copy of your data, or ask us to transfer it to another controller where technically feasible.</li>
            <li><strong>Withdraw consent</strong> – where processing is based on consent, you can withdraw it at any time.</li>
          </ul>
          <p>
            To exercise these rights, please contact us at <a href="mailto:privacy@dev-o.ai">privacy@dev-o.ai</a> or{' '}
            <a href="mailto:legal@dev-o.ai">legal@dev-o.ai</a>. We may need to verify your identity before responding.
          </p>
          <p className="note">
            If you are in the EEA/UK and are not satisfied with our response, you may have the right to lodge a complaint 
            with your local data protection authority.
          </p>
        </section>

        {/* Section 11 */}
        <section id="children" className="privacy-section">
          <h2>11. Children's Privacy</h2>
          <p>
            The DEV-O platform and related services are not intended for children under the age of 16 (or other age 
            as defined by local law), and we do not knowingly collect personal information from children.
          </p>
          <p>
            If you believe a child has provided personal information to us, please contact us so we can take appropriate steps.
          </p>
        </section>

        {/* Section 12 */}
        <section id="security" className="privacy-section">
          <h2>12. Security</h2>
          <p>We take reasonable and appropriate technical and organizational measures to protect personal information against:</p>
          <ul>
            <li>Accidental or unlawful destruction,</li>
            <li>Loss, alteration,</li>
            <li>Unauthorized disclosure or access.</li>
          </ul>
          <p>However, no system can be completely secure. You are responsible for:</p>
          <ul>
            <li>Keeping your login credentials confidential,</li>
            <li>Using strong passwords and enabling additional security features where available,</li>
            <li>Notifying us promptly if you suspect any unauthorized access to your account.</li>
          </ul>
        </section>

        {/* Section 13 */}
        <section id="marketing" className="privacy-section">
          <h2>13. Marketing Communications</h2>
          <p>Where permitted by law, we may use your contact details to send you information about DEV-O, such as:</p>
          <ul>
            <li>Product news and feature updates,</li>
            <li>Events, webinars, and content,</li>
            <li>Surveys and feedback requests.</li>
          </ul>
          <p>
            You can opt out of marketing emails at any time by using the unsubscribe link in the email or contacting us directly. 
            Service-related communications (such as security or billing notices) are typically not optional.
          </p>
        </section>

        {/* Section 14 */}
        <section id="changes" className="privacy-section">
          <h2>14. Changes to This Privacy Policy</h2>
          <p>We may update this Privacy Policy from time to time to reflect changes in:</p>
          <ul>
            <li>Our services and practices,</li>
            <li>Legal requirements,</li>
            <li>Industry standards.</li>
          </ul>
          <p>When we make material changes, we will:</p>
          <ul>
            <li>Update the "Last updated" date at the top of this page, and</li>
            <li>Provide additional notice where appropriate (e.g., via email or in-product notifications).</li>
          </ul>
          <p className="note">We encourage you to review this Privacy Policy periodically.</p>
        </section>

        {/* Section 15 */}
        <section id="contact" className="privacy-section contact-section">
          <h2>15. Contact Us</h2>
          <p>If you have any questions, concerns, or requests related to this Privacy Policy or your personal information, you can contact us at:</p>
          
          <div className="contact-info">
            <div className="contact-emails-box">
              <MailIcon />
              <div>
                <a href="mailto:privacy@dev-o.ai">privacy@dev-o.ai</a>
                <span> or </span>
                <a href="mailto:legal@dev-o.ai">legal@dev-o.ai</a>
              </div>
            </div>
            <div className="contact-address">
              <MapPinIcon />
              <div>
                <p><strong>Bionicverse Inc.</strong></p>
                <p>(Attn: Privacy / DEV-O)</p>
                <p>5830 E 2nd St, Ste 7000 #9656</p>
                <p>Casper, Wyoming 82609</p>
                <p>United States</p>
              </div>
            </div>
          </div>
        </section>

        {/* Closing */}
        <section className="privacy-closing">
          <h2>DEV-O – Digital Engineering Virtual Orchestrator</h2>
          <p>A project by <strong>Bionicverse Inc.</strong> (USA)</p>
          <p className="closing-message">
            We are committed to protecting your privacy while helping you build AI-native engineering systems.
          </p>
        </section>
      </main>

      {/* Footer */}
      <footer className="privacy-footer">
        <div className="privacy-footer-content">
          <div className="privacy-footer-brand">
            <Link to="/" className="privacy-footer-logo">
              <img src="/src/components/Logo/logo+icon.png" alt="DEV-O" />
            </Link>
            <p>Digital Engineering Virtual Orchestrator</p>
          </div>
          <div className="privacy-footer-links">
            <div className="footer-link-group">
              <h4>Legal</h4>
              <Link to="/privacy">Privacy Policy</Link>
              <Link to="/terms">Terms of Service</Link>
              <Link to="/security">Security</Link>
            </div>
            <div className="footer-link-group">
              <h4>Company</h4>
              <Link to="/careers">Careers</Link>
              <Link to="/press">Press</Link>
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
        <div className="privacy-footer-bottom">
          <p>© {new Date().getFullYear()} DEV-O by Bionicverse Inc. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default PrivacyPage;
