import React from 'react';
import { Link } from 'react-router-dom';
import XIcon from '../Icons/social-x.svg';
import LinkedInIcon from '../Icons/social-linkedin.svg';
import './Footer.css';
import logoImage from '../Logo/DEV-O_Logo.png';

const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          {/* Brand Section */}
          <div className="footer-brand">
            <Link to="/" className="footer-logo">
              <img src={logoImage} alt="DEV-O" className="footer-logo-image" />
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
              <img src={XIcon} alt="X logo" loading="lazy" />
            </a>
            <a href="https://www.linkedin.com/company/dev-o/" className="social-link" aria-label="LinkedIn" target="_blank" rel="noopener noreferrer">
              <img src={LinkedInIcon} alt="LinkedIn logo" loading="lazy" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;