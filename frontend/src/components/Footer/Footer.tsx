import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          {/* Brand Section */}
          <div className="footer-brand">
            <Link to="/" className="footer-logo">
              <img src="/src/components/Logo/DEV-O_Logo.png" alt="DEV-O" className="footer-logo-image" />
            </Link>
            <p className="footer-description">
              Accelerate your development workflow with intelligent AI agents that
              transform ideas into production-ready applications.
            </p>
            <Link to="/login" className="footer-cta">
              Get Started Free
            </Link>
          </div>

          {/* Product Links */}
          <div className="footer-section">
            <h3>Product</h3>
            <ul>
              <li><Link to="/features">Features</Link></li>
              <li><Link to="/pricing">Pricing</Link></li>
            </ul>
          </div>

          {/* Resources */}
          <div className="footer-section">
            <h3>Resources</h3>
            <ul>
              <li><a href="#">API Reference</a></li>
              <li><a href="#">Guides</a></li>
              <li><Link to="/blog">Blog</Link></li>
              <li><a href="#">Community</a></li>
              <li><a href="#">Support</a></li>
            </ul>
          </div>

          {/* Company */}
          <div className="footer-section">
            <h3>Company</h3>
            <ul>
              <li><Link to="/about">About</Link></li>
              <li><Link to="/careers">Careers</Link></li>
              <li><Link to="/contact">Contact</Link></li>
              <li><Link to="/partners">Partners</Link></li>
              <li><Link to="/press">Press Kit</Link></li>
            </ul>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="footer-bottom">
          <div className="footer-copyright">
            © {currentYear} DEV-O. All rights reserved.
          </div>

          <div className="footer-legal">
            <Link to="/privacy">Privacy Policy</Link>
            <Link to="/terms">Terms of Service</Link>
            <Link to="/security">Security</Link>
          </div>

          <div className="footer-social">
            <a href="https://x.com/DEV_O_ai" className="social-link" aria-label="X (Twitter)" target="_blank" rel="noopener noreferrer">
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
            </a>
            <a href="https://www.linkedin.com/company/dev-o/" className="social-link" aria-label="LinkedIn" target="_blank" rel="noopener noreferrer">
              <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;