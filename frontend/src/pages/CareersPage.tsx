import React from 'react';
import { Link } from 'react-router-dom';
import './CareersPage.css';

// SVG Icon Components
const RobotIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="10" rx="2"/>
    <circle cx="12" cy="5" r="2"/>
    <path d="M12 7v4"/>
    <line x1="8" y1="16" x2="8" y2="16"/>
    <line x1="16" y1="16" x2="16" y2="16"/>
  </svg>
);

const GearIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="3"/>
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
  </svg>
);

const GlobeIcon = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <line x1="2" y1="12" x2="22" y2="12"/>
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
  </svg>
);

const ToolIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
  </svg>
);

const UsersIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
    <circle cx="9" cy="7" r="4"/>
    <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
    <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
  </svg>
);

const HandshakeIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M11 17a4 4 0 0 0 8 0"/>
    <path d="M12 3v4"/>
    <path d="M3 11h4"/>
    <path d="M17 11h4"/>
    <path d="M5.5 5.5l2.8 2.8"/>
    <path d="M15.7 8.3l2.8-2.8"/>
  </svg>
);

const MessageIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
  </svg>
);

const ZapIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
  </svg>
);

const BrainIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 4.44-1.54"/>
    <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-4.44-1.54"/>
  </svg>
);

const PaletteIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="13.5" cy="6.5" r=".5"/>
    <circle cx="17.5" cy="10.5" r=".5"/>
    <circle cx="8.5" cy="7.5" r=".5"/>
    <circle cx="6.5" cy="12.5" r=".5"/>
    <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.555C21.965 6.012 17.461 2 12 2z"/>
  </svg>
);

const TrendingUpIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/>
    <polyline points="17 6 23 6 23 12"/>
  </svg>
);

const BookIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
  </svg>
);

const MicIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
    <line x1="12" y1="19" x2="12" y2="23"/>
    <line x1="8" y1="23" x2="16" y2="23"/>
  </svg>
);

const ShuffleIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="16 3 21 3 21 8"/>
    <line x1="4" y1="20" x2="21" y2="3"/>
    <polyline points="21 16 21 21 16 21"/>
    <line x1="15" y1="15" x2="21" y2="21"/>
    <line x1="4" y1="4" x2="9" y2="9"/>
  </svg>
);

const LightbulbIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M9 18h6"/>
    <path d="M10 22h4"/>
    <path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 0 1 8.91 14"/>
  </svg>
);

const WrenchIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
  </svg>
);

const EarthIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <path d="M2 12h20"/>
    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
  </svg>
);

const ScaleIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="3" x2="12" y2="21"/>
    <path d="M5 12H2a10 10 0 0 0 20 0h-3"/>
    <path d="M5 12a7 7 0 0 1 14 0"/>
  </svg>
);

const SearchIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8"/>
    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
  </svg>
);

const TargetIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <circle cx="12" cy="12" r="6"/>
    <circle cx="12" cy="12" r="2"/>
  </svg>
);

const ClipboardIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
    <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
  </svg>
);

const HammerIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M15 12l-8.5 8.5c-.83.83-2.17.83-3 0 0 0 0 0 0 0a2.12 2.12 0 0 1 0-3L12 9"/>
    <path d="M17.64 15L22 10.64"/>
    <path d="M20.91 11.7l-1.25-1.25c-.6-.6-.93-1.4-.93-2.25v-.86L16.01 4.6a5.56 5.56 0 0 0-3.94-1.64H9l.92.82A6.18 6.18 0 0 1 12 8.4v1.56l2 2h2.47l2.26 1.91"/>
  </svg>
);

const WavesIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
    <path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
    <path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/>
  </svg>
);

const PuzzleIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M19.439 7.85c-.049.322.059.648.289.878l1.568 1.568c.47.47.706 1.087.706 1.704s-.235 1.233-.706 1.704l-1.611 1.611a.98.98 0 0 1-.837.276c-.47-.07-.802-.48-.968-.925a2.501 2.501 0 1 0-3.214 3.214c.446.166.855.497.925.968a.979.979 0 0 1-.276.837l-1.61 1.61a2.404 2.404 0 0 1-1.705.707 2.402 2.402 0 0 1-1.704-.706l-1.568-1.568a1.026 1.026 0 0 0-.877-.29c-.493.074-.84.504-1.02.968a2.5 2.5 0 1 1-3.237-3.237c.464-.18.894-.527.967-1.02a1.026 1.026 0 0 0-.289-.877l-1.568-1.568A2.402 2.402 0 0 1 1.998 12c0-.617.236-1.234.706-1.704L4.315 8.685a.98.98 0 0 1 .837-.276c.47.07.802.48.968.925a2.501 2.501 0 1 0 3.214-3.214c-.446-.166-.855-.497-.925-.968a.979.979 0 0 1 .276-.837l1.61-1.61a2.404 2.404 0 0 1 1.705-.707c.617 0 1.234.236 1.704.706l1.568 1.568c.23.23.556.338.877.29.493-.074.84-.504 1.02-.968a2.5 2.5 0 1 1 3.237 3.237c-.464.18-.894.527-.967 1.02z"/>
  </svg>
);

const PenIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 19l7-7 3 3-7 7-3-3z"/>
    <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/>
    <path d="M2 2l7.586 7.586"/>
    <circle cx="11" cy="11" r="2"/>
  </svg>
);

const StarIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
  </svg>
);

const RocketIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/>
    <path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>
    <path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>
    <path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>
  </svg>
);

const BuildingIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
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

const ListIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="8" y1="6" x2="21" y2="6"/>
    <line x1="8" y1="12" x2="21" y2="12"/>
    <line x1="8" y1="18" x2="21" y2="18"/>
    <line x1="3" y1="6" x2="3.01" y2="6"/>
    <line x1="3" y1="12" x2="3.01" y2="12"/>
    <line x1="3" y1="18" x2="3.01" y2="18"/>
  </svg>
);

const MailIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
    <polyline points="22,6 12,13 2,6"/>
  </svg>
);

const BellIcon = () => (
  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
    <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
  </svg>
);

const CareersPage: React.FC = () => {
  return (
    <div className="careers-page wavy-scroll">
      {/* Navigation */}
      <nav className="careers-nav">
        <Link to="/" className="careers-nav-logo">
          <img src="/src/components/Logo/logo+icon.png" alt="DEV-O" className="careers-logo-img" />
        </Link>
        <div className="careers-nav-links">
          <Link to="/features">Features</Link>
          <Link to="/pricing">Pricing</Link>
          <Link to="/blog">Blog</Link>
          <Link to="/login" className="careers-nav-cta">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="careers-hero">
        <div className="careers-hero-content">
          <h1>Careers & Culture at DEV-O</h1>
          <p className="careers-hero-subtitle">
            Help build the AI-native engineering layer for the world's most ambitious organizations.
          </p>
          <div className="careers-hero-description">
            <p>
              DEV-O is a Digital Engineering Virtual Orchestrator – a platform by <strong>Bionicverse Inc. (USA)</strong> that 
              helps teams design, build, and run software as truly AI-native systems. Behind the product is a team of 
              builders, systems thinkers, roboticists, designers, and operators who care deeply about doing meaningful 
              work with frontier technology.
            </p>
            <p className="careers-hero-tagline">
              If you're excited by AI, engineering, and orchestration at scale, you'll feel at home here.
            </p>
          </div>
          <a href="#open-roles" className="careers-hero-cta">View Open Roles</a>
        </div>
      </section>

      {/* Quick Navigation */}
      <nav className="careers-quick-nav">
        <div className="careers-quick-nav-inner">
          <a href="#who-we-are">Who We Are</a>
          <a href="#how-we-work">How We Work</a>
          <a href="#culture">Culture</a>
          <a href="#teams">Teams</a>
          <a href="#growth">Growth</a>
          <a href="#dei">DEI</a>
          <a href="#hiring">Hiring</a>
          <a href="#open-roles">Open Roles</a>
        </div>
      </nav>

      {/* Who We Are */}
      <section className="careers-section" id="who-we-are">
        <div className="careers-section-container">
          <h2>Who We Are</h2>
          <p className="careers-section-intro">
            DEV-O is a flagship project of <strong>Bionicverse Inc. (USA)</strong>, a company working at the intersection of:
          </p>
          <div className="careers-pillars">
            <div className="careers-pillar">
              <div className="careers-pillar-icon"><RobotIcon /></div>
              <h3>AI & Digital Engineering</h3>
              <p>Making frontier models useful, safe, and grounded in real systems.</p>
            </div>
            <div className="careers-pillar">
              <div className="careers-pillar-icon"><GearIcon /></div>
              <h3>Automation & Robotics</h3>
              <p>Bringing industrial-grade thinking to software reliability.</p>
            </div>
            <div className="careers-pillar">
              <div className="careers-pillar-icon"><GlobeIcon /></div>
              <h3>Virtual & Spatial Experiences</h3>
              <p>Preparing organizations for the shift beyond 2D dashboards.</p>
            </div>
          </div>
          <div className="careers-mission-box">
            <p>
              We're building DEV-O as the <strong>control plane for AI-native engineering organizations</strong> – 
              a layer that connects tools, people, and systems so work flows from idea to production in a smarter, safer way.
            </p>
          </div>
        </div>
      </section>

      {/* How We Work */}
      <section className="careers-section careers-section-alt" id="how-we-work">
        <div className="careers-section-container">
          <h2>How We Work</h2>
          <p className="careers-section-intro">
            We're designing DEV-O as a modern, globally-collaborative, engineering-first organization.
          </p>
          <div className="careers-work-grid">
            <div className="careers-work-item">
              <div className="careers-work-icon"><ToolIcon /></div>
              <h3>Builder Mindset</h3>
              <p>We value shipping, learning, and improving over endless debate.</p>
            </div>
            <div className="careers-work-item">
              <div className="careers-work-icon"><GlobeIcon /></div>
              <h3>Remote-Friendly & Async-Aware</h3>
              <p>We embrace written communication, clear documentation, and thoughtful meetings.</p>
            </div>
            <div className="careers-work-item">
              <div className="careers-work-icon"><UsersIcon /></div>
              <h3>Small, Empowered Teams</h3>
              <p>People closest to the problem have the context and autonomy to solve it.</p>
            </div>
            <div className="careers-work-item">
              <div className="careers-work-icon"><HandshakeIcon /></div>
              <h3>High Trust, High Ownership</h3>
              <p>When we commit to something, we own it end-to-end.</p>
            </div>
            <div className="careers-work-item">
              <div className="careers-work-icon"><MessageIcon /></div>
              <h3>Customer-Close</h3>
              <p>We spend real time with the teams using DEV-O to understand their world deeply.</p>
            </div>
          </div>
          <div className="careers-callout">
            <p>
              Our work touches critical systems, so we combine speed with a serious respect for 
              <strong> reliability, safety, and governance</strong>.
            </p>
          </div>
        </div>
      </section>

      {/* Culture Principles */}
      <section className="careers-section" id="culture">
        <div className="careers-section-container">
          <h2>Our Culture Principles</h2>
          <p className="careers-section-intro">
            We use DEV-O's own philosophy as the foundation of our culture.
          </p>
          
          <div className="careers-principles">
            <div className="careers-principle">
              <div className="careers-principle-number">1</div>
              <div className="careers-principle-content">
                <h3>Human-in-Command</h3>
                <p className="careers-principle-tagline">We believe AI should augment, not replace, human judgment.</p>
                <ul>
                  <li>We design products where people remain in control of decisions.</li>
                  <li>Internally, we use AI heavily – but we don't abdicate responsibility to it.</li>
                  <li>We encourage thoughtful debate, clear reasoning, and transparent trade-offs.</li>
                </ul>
              </div>
            </div>

            <div className="careers-principle">
              <div className="careers-principle-number">2</div>
              <div className="careers-principle-content">
                <h3>Systems Over Silos</h3>
                <p className="careers-principle-tagline">We think in systems, not just features.</p>
                <ul>
                  <li>We care how parts connect: architecture, teams, workflows, and incentives.</li>
                  <li>We favor long-term health of the system (codebase, culture, and customers) over quick wins.</li>
                  <li>We document how things work so others can build on them.</li>
                </ul>
              </div>
            </div>

            <div className="careers-principle">
              <div className="careers-principle-number">3</div>
              <div className="careers-principle-content">
                <h3>High Bar, Low Ego</h3>
                <p className="careers-principle-tagline">We want to do the best work of our careers without taking ourselves too seriously.</p>
                <ul>
                  <li>We aim for craftsmanship in code, design, content, and operations.</li>
                  <li>We separate ideas from identity – feedback is about the work, not the person.</li>
                  <li>We celebrate wins as a team and learn from mistakes together.</li>
                </ul>
              </div>
            </div>

            <div className="careers-principle">
              <div className="careers-principle-number">4</div>
              <div className="careers-principle-content">
                <h3>Default to Open</h3>
                <p className="careers-principle-tagline">We bias toward transparency and shared context.</p>
                <ul>
                  <li>Plans, decisions, and rationales are written down and shared.</li>
                  <li>We prefer open channels over private backchannels when possible.</li>
                  <li>We treat documentation as a first-class part of building DEV-O.</li>
                </ul>
              </div>
            </div>

            <div className="careers-principle">
              <div className="careers-principle-number">5</div>
              <div className="careers-principle-content">
                <h3>Learn Fast, Safely</h3>
                <p className="careers-principle-tagline">We're working in a fast-moving space – learning is not optional.</p>
                <ul>
                  <li>We design safe-to-try experiments with clear boundaries.</li>
                  <li>We use incidents and failures as inputs to better systems, not blame.</li>
                  <li>We invest in continuous learning for everyone, not just engineers.</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Teams */}
      <section className="careers-section careers-section-alt" id="teams">
        <div className="careers-section-container">
          <h2>Teams at DEV-O</h2>
          <p className="careers-section-intro">
            We're building a multidisciplinary team to match the complexity of the problem.
          </p>
          
          <div className="careers-teams-grid">
            <div className="careers-team-card">
              <div className="careers-team-icon"><ZapIcon /></div>
              <h3>Engineering & Platform</h3>
              <ul>
                <li>Build the core DEV-O platform, orchestration engine, and knowledge graph.</li>
                <li>Work across backend, data, infrastructure, and developer experience.</li>
                <li>Care deeply about reliability, performance, and elegant system design.</li>
              </ul>
            </div>

            <div className="careers-team-card">
              <div className="careers-team-icon"><BrainIcon /></div>
              <h3>AI & Agents</h3>
              <ul>
                <li>Design, train, and orchestrate AI agents across real engineering workflows.</li>
                <li>Focus on grounding, safety, and explainability of AI-assisted actions.</li>
                <li>Collaborate closely with customers to understand real-world constraints.</li>
              </ul>
            </div>

            <div className="careers-team-card">
              <div className="careers-team-icon"><PaletteIcon /></div>
              <h3>Product & Design</h3>
              <ul>
                <li>Turn complex engineering realities into clear, intuitive experiences.</li>
                <li>Craft flows, interfaces, and narratives that help users work with AI confidently.</li>
                <li>Own discovery, prioritization, and iteration with customers.</li>
              </ul>
            </div>

            <div className="careers-team-card">
              <div className="careers-team-icon"><HandshakeIcon /></div>
              <h3>Customer, Solutions & Partnerships</h3>
              <ul>
                <li>Work directly with engineering, platform, and SRE teams at our customers.</li>
                <li>Design rollout plans, solution architectures, and success metrics.</li>
                <li>Build long-term partnerships with organizations adopting AI-native ways of working.</li>
              </ul>
            </div>

            <div className="careers-team-card">
              <div className="careers-team-icon"><TrendingUpIcon /></div>
              <h3>Operations & Growth</h3>
              <ul>
                <li>Ensure we run as a healthy, focused, and scalable business.</li>
                <li>Look after people, processes, finance, and strategic growth.</li>
                <li>Help us stay aligned with our mission and our responsibilities.</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Growth & Learning */}
      <section className="careers-section" id="growth">
        <div className="careers-section-container">
          <h2>Growth, Learning & Career Development</h2>
          <p className="careers-section-intro">
            We want DEV-O to be a place where you grow as fast as the technology does.
          </p>
          
          <div className="careers-growth-grid">
            <div className="careers-growth-item">
              <div className="careers-growth-icon"><BookIcon /></div>
              <h3>Deliberate Learning Time</h3>
              <p>Space for deep work, research, and exploration, not just ticket queues.</p>
            </div>
            <div className="careers-growth-item">
              <div className="careers-growth-icon"><MicIcon /></div>
              <h3>Tech Talks, Guilds & Sharing Rituals</h3>
              <p>Regular sessions where people walk through architectures, incidents, experiments, and tools.</p>
            </div>
            <div className="careers-growth-item">
              <div className="careers-growth-icon"><ShuffleIcon /></div>
              <h3>Cross-Functional Exposure</h3>
              <p>Opportunities to work across product, engineering, AI, and customer teams.</p>
            </div>
            <div className="careers-growth-item">
              <div className="careers-growth-icon"><LightbulbIcon /></div>
              <h3>Mentorship & Feedback</h3>
              <p>Clear expectations, supportive feedback, and opportunities to mentor others.</p>
            </div>
            <div className="careers-growth-item">
              <div className="careers-growth-icon"><WrenchIcon /></div>
              <h3>Access to Tools & Education</h3>
              <p>Modern AI tools, sandbox environments, and curated learning resources.</p>
            </div>
          </div>

          <div className="careers-growth-callout">
            <p>
              If you're curious, reflective, and willing to teach as well as learn, 
              <strong> you'll grow quickly here</strong>.
            </p>
          </div>
        </div>
      </section>

      {/* DEI */}
      <section className="careers-section careers-section-alt" id="dei">
        <div className="careers-section-container">
          <h2>Diversity, Equity & Inclusion</h2>
          <p className="careers-section-intro">
            Building AI-native infrastructure for the world means we need a team that reflects the world.
          </p>
          
          <div className="careers-dei-content">
            <p>At DEV-O and Bionicverse Inc., we are committed to:</p>
            <ul className="careers-dei-list">
              <li>
                <span className="careers-dei-icon"><EarthIcon /></span>
                Hiring and growing people from different backgrounds, geographies, and disciplines.
              </li>
              <li>
                <span className="careers-dei-icon"><MessageIcon /></span>
                Creating a culture where everyone can contribute ideas safely, regardless of title or location.
              </li>
              <li>
                <span className="careers-dei-icon"><ScaleIcon /></span>
                Designing processes that reduce bias in hiring, performance, and promotion.
              </li>
              <li>
                <span className="careers-dei-icon"><SearchIcon /></span>
                Continuously examining how our tools and decisions impact different communities.
              </li>
            </ul>
            <div className="careers-dei-statement">
              <p>
                We're not perfect – but we're intentional. 
                <strong> Inclusion is a design constraint, not an afterthought.</strong>
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Work-Life Balance */}
      <section className="careers-section" id="balance">
        <div className="careers-section-container">
          <h2>Work–Life Balance</h2>
          <p className="careers-section-intro">
            We work on ambitious problems, but we are not building a burnout factory.
          </p>
          
          <div className="careers-balance-grid">
            <div className="careers-balance-item">
              <div className="careers-balance-icon"><ZapIcon /></div>
              <p>We favor <strong>sustainable intensity</strong> over constant urgency.</p>
            </div>
            <div className="careers-balance-item">
              <div className="careers-balance-icon"><TargetIcon /></div>
              <p>We respect <strong>focus time</strong>, time off, and personal boundaries.</p>
            </div>
            <div className="careers-balance-item">
              <div className="careers-balance-icon"><ClipboardIcon /></div>
              <p>We aim for <strong>clear priorities</strong> so people know what matters most.</p>
            </div>
          </div>

          <div className="careers-balance-statement">
            <p>
              We believe people do their best work when they can maintain a healthy life outside of work.
            </p>
          </div>
        </div>
      </section>

      {/* What We Look For */}
      <section className="careers-section careers-section-alt" id="look-for">
        <div className="careers-section-container">
          <h2>What We Look For</h2>
          <p className="careers-section-intro">
            Across roles, we tend to look for people who:
          </p>
          
          <div className="careers-traits-grid">
            <div className="careers-trait">
              <span className="careers-trait-icon"><HammerIcon /></span>
              <p>Are <strong>builders at heart</strong> – enjoy turning ideas into real systems, not just talking about them.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon"><WavesIcon /></span>
              <p>Are <strong>comfortable with ambiguity</strong> and change – this space evolves quickly.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon"><PuzzleIcon /></span>
              <p>Can <strong>think in systems</strong>, not just individual tasks.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon"><PenIcon /></span>
              <p><strong>Communicate clearly</strong> in writing and in conversation.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon"><StarIcon /></span>
              <p>Care about <strong>craft, reliability, and impact</strong>.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon"><HandshakeIcon /></span>
              <p>Treat colleagues, customers, and partners with <strong>respect and curiosity</strong>.</p>
            </div>
          </div>

          <div className="careers-traits-note">
            <p>
              You don't need a perfect resume. We care more about <strong>how you think</strong>, 
              <strong> how you learn</strong>, and <strong>how you work with others</strong>.
            </p>
          </div>
        </div>
      </section>

      {/* Hiring Process */}
      <section className="careers-section" id="hiring">
        <div className="careers-section-container">
          <h2>Our Hiring Approach</h2>
          <p className="careers-section-intro">
            We aim to make the hiring process respectful, efficient, and signal-rich for both sides.
          </p>
          
          <div className="careers-hiring-timeline">
            <div className="careers-hiring-step">
              <div className="careers-hiring-step-number">1</div>
              <div className="careers-hiring-step-content">
                <h3>Application & Screening</h3>
                <p>We review your background, context, and motivation for joining DEV-O.</p>
              </div>
            </div>

            <div className="careers-hiring-step">
              <div className="careers-hiring-step-number">2</div>
              <div className="careers-hiring-step-content">
                <h3>Intro Conversation</h3>
                <p>A discussion about your experience, what you're looking for, and what DEV-O is building.</p>
              </div>
            </div>

            <div className="careers-hiring-step">
              <div className="careers-hiring-step-number">3</div>
              <div className="careers-hiring-step-content">
                <h3>Deep-Dive Interviews</h3>
                <p>Conversations with future teammates or leaders focused on skills, decision-making, and how you work.</p>
              </div>
            </div>

            <div className="careers-hiring-step">
              <div className="careers-hiring-step-number">4</div>
              <div className="careers-hiring-step-content">
                <h3>Practical Exercise</h3>
                <p>A realistic, bounded task (technical, product, or domain-specific) that mirrors the kind of work you'd do here.</p>
              </div>
            </div>

            <div className="careers-hiring-step">
              <div className="careers-hiring-step-number">5</div>
              <div className="careers-hiring-step-content">
                <h3>Final Conversation</h3>
                <p>Time for you to ask deeper questions about culture, strategy, and how you can grow here.</p>
              </div>
            </div>
          </div>

          <div className="careers-hiring-note">
            <p>
              We keep communication transparent and aim to give clear, actionable feedback whenever possible.
            </p>
          </div>
        </div>
      </section>

      {/* Why Join Now */}
      <section className="careers-section careers-section-highlight" id="why-now">
        <div className="careers-section-container">
          <h2>Why Join DEV-O Now</h2>
          <p className="careers-section-intro">
            Joining DEV-O at this stage means:
          </p>
          
          <div className="careers-why-grid">
            <div className="careers-why-item">
              <div className="careers-why-icon"><RocketIcon /></div>
              <p>Working on <strong>frontier problems</strong> at the intersection of AI, engineering, and operations.</p>
            </div>
            <div className="careers-why-item">
              <div className="careers-why-icon"><TargetIcon /></div>
              <p>Having <strong>real ownership</strong> over product areas, systems, and outcomes.</p>
            </div>
            <div className="careers-why-item">
              <div className="careers-why-icon"><BuildingIcon /></div>
              <p>Helping shape not just a platform, but a <strong>new way of running engineering organizations</strong>.</p>
            </div>
            <div className="careers-why-item">
              <div className="careers-why-icon"><GlobeIcon /></div>
              <p>Growing alongside a <strong>small, focused team</strong> with global ambitions.</p>
            </div>
          </div>

          <div className="careers-why-statement">
            <p>
              If you want your work to matter for how AI and engineering evolve in the next decade, 
              <strong> DEV-O is a place to do that</strong>.
            </p>
          </div>
        </div>
      </section>

      {/* Open Roles */}
      <section className="careers-section" id="open-roles">
        <div className="careers-section-container">
          <h2>How to Explore Roles</h2>
          <p className="careers-section-intro">
            We're always interested in meeting people who resonate with this vision.
          </p>
          
          <div className="careers-roles-options">
            <div className="careers-role-option">
              <div className="careers-role-icon"><ListIcon /></div>
              <h3>Browse Open Roles</h3>
              <p>Check our current openings across all teams.</p>
              <a href="#" className="careers-role-link">View Openings →</a>
            </div>
            <div className="careers-role-option">
              <div className="careers-role-icon"><MailIcon /></div>
              <h3>General Application</h3>
              <p>If you don't see a perfect fit, send a general application describing how you'd like to contribute.</p>
              <a href="#" className="careers-role-link">Apply Now →</a>
            </div>
            <div className="careers-role-option">
              <div className="careers-role-icon"><BellIcon /></div>
              <h3>Stay Updated</h3>
              <p>Follow DEV-O and Bionicverse Inc. on our channels to stay updated on new roles and projects.</p>
              <a href="#" className="careers-role-link">Follow Us →</a>
            </div>
          </div>

          <div className="careers-roles-footer">
            <p className="careers-bionicverse">DEV-O is a project by <strong>Bionicverse Inc. (USA)</strong>.</p>
            <p className="careers-final-cta">
              If you'd like to help build the AI-native engineering layer of the future, 
              <strong> we'd love to hear from you</strong>.
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="careers-footer">
        <div className="careers-footer-content">
          <p>© {new Date().getFullYear()} DEV-O by Bionicverse Inc. All rights reserved.</p>
          <div className="careers-footer-links">
            <Link to="/">Home</Link>
            <Link to="/features">Features</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/blog">Blog</Link>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default CareersPage;
