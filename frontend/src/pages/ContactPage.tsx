import { useState } from 'react';
import { Link } from 'react-router-dom';
import './ContactPage.css';

// SVG Icon Components
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

const MessageIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
  </svg>
);

const ShieldIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
  </svg>
);

const GlobeIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <line x1="2" y1="12" x2="22" y2="12"/>
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
  </svg>
);

const CalendarIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
    <line x1="16" y1="2" x2="16" y2="6"/>
    <line x1="8" y1="2" x2="8" y2="6"/>
    <line x1="3" y1="10" x2="21" y2="10"/>
  </svg>
);

const HeadphonesIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 18v-6a9 9 0 0 1 18 0v6"/>
    <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>
  </svg>
);

const SendIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13"/>
    <polygon points="22,2 15,22 11,13 2,9"/>
  </svg>
);

const PaperclipIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
  </svg>
);

const ContactPage = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    workEmail: '',
    company: '',
    role: '',
    country: '',
    reason: '',
    message: '',
    followUpMethod: 'email',
    attachment: null as File | null
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitSuccess, setSubmitSuccess] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFormData(prev => ({ ...prev, attachment: e.target.files![0] }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setIsSubmitting(false);
    setSubmitSuccess(true);
    
    // Reset form after success
    setTimeout(() => {
      setSubmitSuccess(false);
      setFormData({
        fullName: '',
        workEmail: '',
        company: '',
        role: '',
        country: '',
        reason: '',
        message: '',
        followUpMethod: 'email',
        attachment: null
      });
    }, 3000);
  };

  return (
    <div className="contact-page wavy-scroll">
      {/* Navigation */}
      <nav className="contact-nav">
        <div className="contact-nav-container">
          <Link to="/" className="contact-logo">
            <img src="/src/components/Logo/DEV-O_Logo.png" alt="DEV-O" className="contact-logo-image" />
          </Link>
          <div className="contact-nav-links">
            <Link to="/features">Features</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/partners">Partners</Link>
            <Link to="/blog">Blog</Link>
          </div>
          <Link to="/login" className="contact-nav-cta">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="contact-hero">
        <div className="contact-hero-content">
          <div className="contact-hero-badge">
            <MessageIcon />
            <span>Contact</span>
          </div>
          <h1>We'd Love to Hear from You</h1>
          <p>
            Whether you want to explore DEV-O for your organization, discuss a partnership, 
            or ask a technical question, this is the place to reach us.
          </p>
          <p className="contact-hero-note">
            DEV-O is a project by Bionicverse Inc. (USA) with a globally distributed team. 
            Use the contact form below or reach out through one of the dedicated email channels.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <main className="contact-main">
        {/* Contact Form Section */}
        <section className="contact-form-section">
          <div className="contact-form-header">
            <h2>Contact Form</h2>
            <p>
              Share a bit about yourself and what you're looking for, and we'll connect you 
              with the right person on the DEV-O team.
            </p>
          </div>

          <form className="contact-form" onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="fullName">Full Name *</label>
                <input
                  type="text"
                  id="fullName"
                  name="fullName"
                  value={formData.fullName}
                  onChange={handleInputChange}
                  placeholder="So we know how to address you"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="workEmail">Work Email *</label>
                <input
                  type="email"
                  id="workEmail"
                  name="workEmail"
                  value={formData.workEmail}
                  onChange={handleInputChange}
                  placeholder="We'll use this to follow up"
                  required
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="company">Company / Organization *</label>
                <input
                  type="text"
                  id="company"
                  name="company"
                  value={formData.company}
                  onChange={handleInputChange}
                  placeholder="Tell us where you work"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="role">Role / Title</label>
                <input
                  type="text"
                  id="role"
                  name="role"
                  value={formData.role}
                  onChange={handleInputChange}
                  placeholder="e.g., CTO, Platform Lead, SRE Manager"
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="country">Country / Region</label>
                <input
                  type="text"
                  id="country"
                  name="country"
                  value={formData.country}
                  onChange={handleInputChange}
                  placeholder="For regional routing"
                />
              </div>
              <div className="form-group">
                <label htmlFor="reason">Reason for Contact *</label>
                <select
                  id="reason"
                  name="reason"
                  value={formData.reason}
                  onChange={handleInputChange}
                  required
                >
                  <option value="">Select a reason...</option>
                  <option value="sales">Talk to Sales / Explore DEV-O for my organization</option>
                  <option value="technical">Product & Technical Questions</option>
                  <option value="partnerships">Partnerships & Alliances</option>
                  <option value="media">Media & Speaking</option>
                  <option value="careers">Careers & Hiring</option>
                  <option value="other">Other / General Inquiry</option>
                </select>
              </div>
            </div>

            <div className="form-group full-width">
              <label htmlFor="message">How Can We Help? *</label>
              <textarea
                id="message"
                name="message"
                value={formData.message}
                onChange={handleInputChange}
                placeholder="A short description of what you're looking for: your current challenges, timelines, or any context you'd like to share."
                rows={5}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Preferred Follow-Up Method</label>
                <div className="radio-group">
                  <label className="radio-label">
                    <input
                      type="radio"
                      name="followUpMethod"
                      value="email"
                      checked={formData.followUpMethod === 'email'}
                      onChange={handleInputChange}
                    />
                    <span>Email only</span>
                  </label>
                  <label className="radio-label">
                    <input
                      type="radio"
                      name="followUpMethod"
                      value="email-meeting"
                      checked={formData.followUpMethod === 'email-meeting'}
                      onChange={handleInputChange}
                    />
                    <span>Email + Meeting request</span>
                  </label>
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="attachment">Attachments (Optional)</label>
                <div className="file-input-wrapper">
                  <input
                    type="file"
                    id="attachment"
                    name="attachment"
                    onChange={handleFileChange}
                    accept=".pdf,.doc,.docx,.png,.jpg,.jpeg"
                  />
                  <div className="file-input-display">
                    <PaperclipIcon />
                    <span>{formData.attachment ? formData.attachment.name : 'Upload RFPs, diagrams, briefs...'}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="form-submit">
              <button 
                type="submit" 
                className={`submit-btn ${isSubmitting ? 'submitting' : ''} ${submitSuccess ? 'success' : ''}`}
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <span>Sending...</span>
                ) : submitSuccess ? (
                  <span>Message Sent!</span>
                ) : (
                  <>
                    <SendIcon />
                    <span>Send Message</span>
                  </>
                )}
              </button>
              <p className="response-time">
                Response time: We aim to respond to most inquiries within 2–3 business days.
              </p>
            </div>
          </form>
        </section>

        {/* Direct Email Contacts */}
        <section className="email-contacts-section">
          <h2>Direct Email Contacts</h2>
          <p className="section-intro">
            If you prefer, you can contact us directly via email. Feel free to choose the address 
            that best matches your request.
          </p>

          <div className="email-grid">
            <div className="email-card">
              <div className="email-card-icon">
                <MailIcon />
              </div>
              <h3>General Inquiries</h3>
              <p>For anything that doesn't fit a specific bucket or you're not sure where to start.</p>
              <a href="mailto:hello@dev-o.ai" className="email-link">hello@dev-o.ai</a>
            </div>

            <div className="email-card">
              <div className="email-card-icon sales">
                <MailIcon />
              </div>
              <h3>Sales & Product Exploration</h3>
              <p>For organizations interested in piloting or deploying DEV-O.</p>
              <a href="mailto:sales@dev-o.ai" className="email-link">sales@dev-o.ai</a>
            </div>

            <div className="email-card">
              <div className="email-card-icon tech">
                <MailIcon />
              </div>
              <h3>Platform, Technical & Integration</h3>
              <p>For questions about architecture, integrations, data, or technical fit.</p>
              <a href="mailto:tech@dev-o.ai" className="email-link">tech@dev-o.ai</a>
            </div>

            <div className="email-card">
              <div className="email-card-icon partners">
                <MailIcon />
              </div>
              <h3>Partnerships & Alliances</h3>
              <p>For technology partners, integrators, resellers, and strategic alliances.</p>
              <a href="mailto:partners@dev-o.ai" className="email-link">partners@dev-o.ai</a>
            </div>

            <div className="email-card">
              <div className="email-card-icon careers">
                <MailIcon />
              </div>
              <h3>Careers & Talent</h3>
              <p>For questions about open roles, hiring, and speculative applications.</p>
              <a href="mailto:careers@dev-o.ai" className="email-link">careers@dev-o.ai</a>
            </div>

            <div className="email-card">
              <div className="email-card-icon press">
                <MailIcon />
              </div>
              <h3>Media, Press & Speaking</h3>
              <p>For press inquiries, interviews, and events.</p>
              <a href="mailto:press@dev-o.ai" className="email-link">press@dev-o.ai</a>
            </div>
          </div>
        </section>

        {/* Support & Security */}
        <section className="support-section">
          <h2>Support & Security</h2>
          <p className="section-intro">
            DEV-O is built for organizations running critical systems, so we take support and security seriously.
          </p>

          <div className="support-grid">
            <div className="support-card">
              <div className="support-card-header">
                <HeadphonesIcon />
                <h3>Customer Support</h3>
              </div>
              <p>
                Existing customers should use their dedicated support channel (portal or shared email) 
                for priority handling.
              </p>
              <p>You can also reach us at:</p>
              <a href="mailto:support@dev-o.ai" className="support-email">support@dev-o.ai</a>
            </div>

            <div className="support-card security">
              <div className="support-card-header">
                <ShieldIcon />
                <h3>Security & Vulnerability Disclosure</h3>
              </div>
              <p>
                If you believe you've found a security issue or vulnerability in DEV-O, please contact us.
                Include a clear description, steps to reproduce (if possible), and any relevant logs or screenshots.
              </p>
              <p>We appreciate responsible disclosure and will work with you to address issues promptly.</p>
              <a href="mailto:security@dev-o.ai" className="support-email">security@dev-o.ai</a>
            </div>
          </div>
        </section>

        {/* Our Locations */}
        <section className="locations-section">
          <h2>Our Locations</h2>
          <p className="section-intro">
            DEV-O is operated by Bionicverse Inc. (USA) with a globally distributed engineering and customer team.
            We work across several key hubs:
          </p>

          <div className="locations-grid">
            <div className="location-card">
              <div className="location-icon">
                <MapPinIcon />
              </div>
              <h3>United States</h3>
              <p>Bionicverse Inc. (USA)</p>
              <span className="location-type">Corporate headquarters and strategy</span>
            </div>

            <div className="location-card">
              <div className="location-icon">
                <MapPinIcon />
              </div>
              <h3>MENA / Africa</h3>
              <p>Regional Operations</p>
              <span className="location-type">Engineering, delivery, and field operations support</span>
            </div>

            <div className="location-card">
              <div className="location-icon">
                <GlobeIcon />
              </div>
              <h3>Europe & Beyond</h3>
              <p>Global Network</p>
              <span className="location-type">Remote contributors and partners</span>
            </div>
          </div>

          <div className="remote-note">
            <p>
              Many of our team members work remotely. We design our processes to be remote-friendly and 
              async-aware, so we can collaborate effectively across time zones.
            </p>
            <p>
              If you need to coordinate with a specific region or time zone, mention it in your message 
              and we'll route your request accordingly.
            </p>
          </div>
        </section>

        {/* Meeting with DEV-O */}
        <section className="meeting-section">
          <h2>Meeting with the DEV-O Team</h2>
          <p className="section-intro">
            If you're interested in a deeper conversation, we're happy to arrange:
          </p>

          <div className="meeting-grid">
            <div className="meeting-card">
              <CalendarIcon />
              <h3>Discovery Calls</h3>
              <p>To understand your current engineering stack and challenges.</p>
            </div>

            <div className="meeting-card">
              <CalendarIcon />
              <h3>Product Walkthroughs</h3>
              <p>High-level overviews of DEV-O's capabilities and roadmap.</p>
            </div>

            <div className="meeting-card">
              <CalendarIcon />
              <h3>Technical Deep Dives</h3>
              <p>Architecture, integrations, data, and security discussions.</p>
            </div>

            <div className="meeting-card">
              <CalendarIcon />
              <h3>Pilot & Rollout Planning</h3>
              <p>For organizations looking to adopt DEV-O as a core orchestration layer.</p>
            </div>
          </div>

          <p className="meeting-note">
            Just mention your preferences in the contact form (or email), and we'll coordinate a time that works.
          </p>
        </section>

        {/* Staying in Touch */}
        <section className="staying-section">
          <h2>Staying in Touch</h2>
          <p className="section-intro">
            If you'd like to follow DEV-O beyond a one-time contact:
          </p>

          <div className="staying-links">
            <Link to="/blog" className="staying-link">
              <span className="staying-link-title">Blog & Insights</span>
              <span className="staying-link-desc">Ideas, frameworks, and field notes</span>
            </Link>
            <a href="https://www.linkedin.com/company/dev-o/" target="_blank" rel="noopener noreferrer" className="staying-link">
              <span className="staying-link-title">Follow Us</span>
              <span className="staying-link-desc">DEV-O and Bionicverse Inc. on LinkedIn</span>
            </a>
          </div>
        </section>

        {/* Closing */}
        <section className="contact-closing">
          <h2>DEV-O – Digital Engineering Virtual Orchestrator</h2>
          <p>A project by <strong>Bionicverse Inc.</strong> (USA)</p>
          <p className="closing-message">
            If you're building – or want to build – an AI-native engineering organization, we'd be glad to talk.
          </p>
        </section>
      </main>

      {/* Footer */}
      <footer className="contact-footer">
        <div className="contact-footer-content">
          <div className="contact-footer-brand">
            <Link to="/" className="contact-footer-logo">
              <img src="/src/components/Logo/DEV-O_Logo.png" alt="DEV-O" />
            </Link>
            <p>Digital Engineering Virtual Orchestrator</p>
          </div>
          <div className="contact-footer-links">
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
        <div className="contact-footer-bottom">
          <p>© {new Date().getFullYear()} DEV-O by Bionicverse Inc. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default ContactPage;
