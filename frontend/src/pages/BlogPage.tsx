/**
 * BlogPage - DEV-O Blog & Insights
 */

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Logo from '../components/Logo/Logo';
import Footer from '../components/Footer/Footer';
import { PageIcon, PageIconName } from '../components/Icons/PageIcon';
import './BlogPage.css';

interface BlogPost {
  id: string;
  title: string;
  excerpt: string;
  category: string;
  date: string;
  readTime: string;
  featured?: boolean;
}

interface Topic {
  id: string;
  number: string;
  title: string;
  description: string;
  items: string[];
  icon: PageIconName;
}

interface HighlightItem {
  icon: PageIconName;
  text: string;
}

interface SeriesItem {
  icon: PageIconName;
  title: string;
  description: string;
}

interface ContentTypeItem {
  icon: PageIconName;
  title: string;
  description: string;
}

interface AudienceItem {
  icon: PageIconName;
  title: string;
  description: string;
}

interface ConnectOption {
  icon: PageIconName;
  text: string;
}

const BlogPage: React.FC = () => {
  const navigate = useNavigate();
  const [activeFilter, setActiveFilter] = useState<string>('all');

  const categories = [
    { id: 'all', name: 'All Posts' },
    { id: 'ai-native', name: 'AI-Native Engineering' },
    { id: 'incidents', name: 'Incidents & Reliability' },
    { id: 'platform', name: 'Platform & DevEx' },
    { id: 'governance', name: 'Architecture & Governance' },
    { id: 'culture', name: 'Teams & Culture' },
    { id: 'product', name: 'Product Updates' }
  ];

  const blogHighlights: HighlightItem[] = [
    { icon: 'microscope', text: 'Deep dives on AI + engineering' },
    { icon: 'clipboard', text: 'Practical playbooks and frameworks' },
    { icon: 'globe', text: 'Stories from the field' },
    { icon: 'package', text: 'Updates from the DEV-O team' }
  ];

  const topics: Topic[] = [
    {
      id: 'ai-native',
      number: '1',
      title: 'AI-Native Engineering',
      description: 'How to design organizations, architectures, and workflows where AI is part of the system, not just a tool on the side.',
      items: [
        'AI-native vs. AI-assisted engineering',
        'Orchestrating agents across the SDLC (plan → build → test → deploy → operate)',
        'Aligning leadership, platform, and product around one AI strategy',
        'Measuring the real impact of AI on engineering performance'
      ],
      icon: 'brain'
    },
    {
      id: 'incidents',
      number: '2',
      title: 'Incident Management & Reliability in an AI World',
      description: 'How to keep systems reliable as they grow more complex and more automated.',
      items: [
        'AI incident co-pilots: what they should (and shouldn\'t) do',
        'Building a living incident knowledge graph',
        'Patterns for faster MTTR without burning out on-call teams',
        'How to learn from incidents and feed that back into your systems'
      ],
      icon: 'alert'
    },
    {
      id: 'platform',
      number: '3',
      title: 'Platform, DevEx & Orchestration',
      description: 'How platform and DevEx teams can use DEV-O to reduce glue code and increase leverage.',
      items: [
        'Designing an orchestration layer over your existing tools',
        'Making CI/CD, observability, and incident tooling work as one system',
        'Developer experience in AI-native environments',
        'Transitioning from ad-hoc scripts to governed workflows'
      ],
      icon: 'wrench'
    },
    {
      id: 'governance',
      number: '4',
      title: 'Architecture, Governance & Safety',
      description: 'How to stay fast and safe when AI and automation can touch production.',
      items: [
        'Human-in-command design patterns',
        'Policy-aware agents and safe approval workflows',
        'Architecture reviews with AI in the loop',
        'Designing guardrails for multi-agent, multi-tool systems'
      ],
      icon: 'shield'
    },
    {
      id: 'culture',
      number: '5',
      title: 'Teams, Culture & Ways of Working',
      description: 'Because tools alone do nothing without people and culture.',
      items: [
        'Building AI-literate engineering cultures',
        'New roles in AI-native organizations (AI platform, orchestration leads, etc.)',
        'Remote, async-first collaboration patterns',
        'How to upskill teams for AI-native work'
      ],
      icon: 'users'
    },
    {
      id: 'product',
      number: '6',
      title: 'Product & Platform Updates',
      description: 'News and deep dives from the DEV-O product team.',
      items: [
        'New DEV-O capabilities and features',
        'Reference architectures and implementation patterns',
        'Customer stories and case studies',
        'Roadmap previews and how we think about the future'
      ],
      icon: 'package'
    }
  ];

  const insightSeries: SeriesItem[] = [
    {
      icon: 'brain',
      title: 'Building an AI-Native Engineering Org',
      description: 'Why AI-native engineering is different from traditional DevOps, how to design an AI-native control plane, and step-by-step journeys from isolated AI tools to full orchestration.'
    },
    {
      icon: 'alert',
      title: 'Incidents, Reliability & Learning',
      description: 'Real-world incident patterns, the anatomy of an effective incident co-pilot, and how to turn post-mortems into a living, searchable asset.'
    },
    {
      icon: 'wrench',
      title: 'Platform, Tools & Integrations',
      description: 'Designing integrations and workflows around DEV-O, best practices for connecting your engineering stack, and examples of custom agents.'
    },
    {
      icon: 'globe',
      title: 'The Future of Engineering Operations',
      description: 'From dashboards to immersive operations environments, the role of robotics, spatial computing, and AI in operations, and what "bionic" organizations might look like.'
    }
  ];

  const contentTypes: ContentTypeItem[] = [
    { icon: 'book', title: 'Deep-Dive Articles', description: 'Long-form explorations with diagrams, patterns, and examples.' },
    { icon: 'clipboard', title: 'Playbooks & Checklists', description: 'Practical guides you can apply directly in your organization.' },
    { icon: 'note', title: 'Field Notes', description: 'Shorter reflections from pilots, experiments, and customer work.' },
    { icon: 'mic', title: 'Talks & Sessions', description: 'Recaps and recordings from DEV-O tech talks, guilds, and events.' },
    { icon: 'gear', title: 'Product Notes', description: 'Detailed explainers of new DEV-O features and their design choices.' }
  ];

  const audience: AudienceItem[] = [
    { icon: 'briefcase', title: 'CTOs & Heads of Engineering', description: 'Thinking about AI strategy, resilience, and organizational design.' },
    { icon: 'wrench', title: 'Platform & SRE Leaders', description: 'Designing the underlying systems, platforms, and guardrails.' },
    { icon: 'chart', title: 'Product & Delivery Leaders', description: 'Navigating speed, risk, and quality with AI in the mix.' },
    { icon: 'laptop', title: 'Senior Engineers & Architects', description: 'Who want to design and operate AI-native systems responsibly.' }
  ];

  const connectOptions: ConnectOption[] = [
    { icon: 'book', text: 'Browse the latest posts on this page' },
    { icon: 'tag', text: 'Filter by topic (AI-native, incidents, platform, governance, culture, updates)' },
    { icon: 'mail', text: 'Subscribe to updates to get new articles in your inbox' },
    { icon: 'globe', text: 'Follow DEV-O and Bionicverse Inc. on social channels' }
  ];

  // Sample blog posts (placeholder)
  const samplePosts: BlogPost[] = [
    {
      id: '1',
      title: 'Why AI-Native Engineering Is Different From DevOps',
      excerpt: 'Understanding the paradigm shift from automation to orchestration in modern engineering organizations.',
      category: 'ai-native',
      date: 'Coming Soon',
      readTime: '12 min read',
      featured: true
    },
    {
      id: '2',
      title: 'Building Your First AI Incident Co-Pilot',
      excerpt: 'A practical guide to implementing AI-assisted incident response without losing human oversight.',
      category: 'incidents',
      date: 'Coming Soon',
      readTime: '8 min read',
      featured: true
    },
    {
      id: '3',
      title: 'The Engineering Knowledge Graph: Your Organization\'s Memory',
      excerpt: 'How to build and maintain a living knowledge graph that captures how your engineering organization actually works.',
      category: 'platform',
      date: 'Coming Soon',
      readTime: '15 min read',
      featured: true
    }
  ];

  return (
    <div className="blog-page wavy-scroll">
      {/* Navigation Header */}
      <header className="blog-header-nav">
        <div className="blog-header-container">
          <Link to="/" className="blog-header-logo">
            <Logo />
          </Link>
          <nav className="blog-header-links">
            <Link to="/features" className="nav-link">Features</Link>
            <Link to="/pricing" className="nav-link">Pricing</Link>
            <Link to="/blog" className="nav-link active">Blog</Link>
            <Link to="/login" className="nav-link">Login</Link>
            <button className="nav-cta" onClick={() => navigate('/login?register=true')}>
              Get Started
            </button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="blog-hero">
        <div className="blog-hero-content">
          <div className="blog-badge">
            <span className="badge-icon">
              <PageIcon name="book" size={18} />
            </span>
            <span>Blog & Insights</span>
          </div>
          <h1 className="blog-title">
            DEV-O Blog & Insights
          </h1>
          <p className="blog-subtitle">
            Ideas, frameworks, and real-world lessons on building AI-native engineering organizations.
          </p>
          <p className="blog-intro">
            The DEV-O Blog & Insights hub is where we share how teams can move beyond AI experiments 
            and build orchestrated, AI-native engineering systems in practice.
          </p>
          <div className="blog-highlights">
            {blogHighlights.map((item, index) => (
              <span key={index} className="blog-highlight-item">
                <PageIcon name={item.icon} size={18} />
                {item.text}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Posts */}
      <section className="featured-posts-section">
        <div className="section-container">
          <h2 className="section-title">Featured Insights</h2>
          <p className="section-description">Latest thinking from the DEV-O team</p>
          <div className="featured-posts-grid">
            {samplePosts.filter(p => p.featured).map((post) => (
              <div key={post.id} className="featured-post-card">
                <div className="post-category">{categories.find(c => c.id === post.category)?.name}</div>
                <h3 className="post-title">{post.title}</h3>
                <p className="post-excerpt">{post.excerpt}</p>
                <div className="post-meta">
                  <span className="post-date">{post.date}</span>
                  <span className="post-read-time">{post.readTime}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* What We Write About */}
      <section className="topics-section">
        <div className="section-container">
          <h2 className="section-title">What We Write About</h2>
          <p className="section-description">
            We focus on the intersection of AI, engineering, operations, and organizational design.
          </p>
          <div className="topics-grid">
            {topics.map((topic) => (
              <div key={topic.id} className="topic-card">
                <div className="topic-header">
                  <span className="topic-icon">
                    <PageIcon name={topic.icon} size={28} />
                  </span>
                  <span className="topic-number">{topic.number}</span>
                </div>
                <h3 className="topic-title">{topic.title}</h3>
                <p className="topic-description">{topic.description}</p>
                <div className="topic-items">
                  <span className="topic-items-label">Typical topics:</span>
                  <ul>
                    {topic.items.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Insight Series */}
      <section className="series-section">
        <div className="section-container">
          <h2 className="section-title">Featured Insight Series</h2>
          <p className="section-description">
            We organize some of our content into recurring series for easier navigation.
          </p>
          <div className="series-grid">
            {insightSeries.map((series, index) => (
              <div key={index} className="series-card">
                <span className="series-icon">
                  <PageIcon name={series.icon} size={32} />
                </span>
                <h3 className="series-title">{series.title}</h3>
                <p className="series-description">{series.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Types of Content */}
      <section className="content-types-section">
        <div className="section-container">
          <h2 className="section-title">Types of Content</h2>
          <p className="section-description">
            We publish a mix of formats to suit different ways of learning.
          </p>
          <div className="content-types-grid">
            {contentTypes.map((type, index) => (
              <div key={index} className="content-type-card">
                <span className="content-type-icon">
                  <PageIcon name={type.icon} size={26} />
                </span>
                <h4 className="content-type-title">{type.title}</h4>
                <p className="content-type-description">{type.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Who the Blog Is For */}
      <section className="audience-section">
        <div className="section-container">
          <h2 className="section-title">Who the Blog Is For</h2>
          <p className="section-description">We write primarily for:</p>
          <div className="audience-grid">
            {audience.map((item, index) => (
              <div key={index} className="audience-card">
                <span className="audience-icon">
                  <PageIcon name={item.icon} size={30} />
                </span>
                <h4 className="audience-title">{item.title}</h4>
                <p className="audience-description">{item.description}</p>
              </div>
            ))}
          </div>
          <p className="audience-note">Curious builders from any discipline are welcome.</p>
        </div>
      </section>

      {/* How DEV-O Uses Its Own Ideas */}
      <section className="practice-section">
        <div className="section-container">
          <div className="practice-card">
            <h2>How DEV-O Uses Its Own Ideas</h2>
            <p className="practice-intro">We don't just write about concepts – we use them.</p>
            <p className="practice-subtitle">Inside DEV-O and Bionicverse Inc. (USA):</p>
            <ul className="practice-list">
              <li>We use our own orchestration patterns to coordinate work across teams.</li>
              <li>We run internal experiments with AI agents under strict, human-in-command guardrails.</li>
              <li>We treat incidents, decisions, and experiments as input to our own knowledge graph.</li>
              <li>We openly share what worked, what failed, and what surprised us.</li>
            </ul>
            <p className="practice-goal">
              Our goal is to keep the blog <strong>honest</strong>, <strong>practical</strong>, and <strong>grounded in reality</strong>.
            </p>
          </div>
        </div>
      </section>

      {/* Stay Connected */}
      <section className="connect-section">
        <div className="section-container">
          <h2 className="section-title">Stay Connected</h2>
          <p className="section-description">If you want to follow DEV-O's thinking:</p>
          <div className="connect-options">
            {connectOptions.map((option, index) => (
              <div key={index} className="connect-option">
                <span className="connect-icon">
                  <PageIcon name={option.icon} size={28} />
                </span>
                <p>{option.text}</p>
              </div>
            ))}
          </div>
          <div className="subscribe-form">
            <input type="email" placeholder="Enter your email for updates" className="subscribe-input" />
            <button className="subscribe-button">Subscribe</button>
          </div>
        </div>
      </section>

      {/* Share Your Story */}
      <section className="share-section">
        <div className="section-container">
          <div className="share-card">
            <h2>Share Your Story</h2>
            <p>
              We're always learning from teams who are pushing the boundaries of how AI and engineering work together.
            </p>
            <div className="share-criteria">
              <p>If you:</p>
              <ul>
                <li>Are experimenting with AI in your engineering organization</li>
                <li>Have built your own orchestration or co-pilot patterns</li>
                <li>Want to collaborate on a case study or guest piece</li>
              </ul>
              <p className="share-cta-text">We'd love to hear from you.</p>
            </div>
            <a href="mailto:hello@dev-o.ai?subject=Blog Collaboration" className="share-cta">
              Get in Touch
            </a>
          </div>
        </div>
      </section>

      {/* Mission Statement */}
      <section className="mission-section">
        <div className="section-container">
          <div className="mission-content">
            <p className="mission-label">DEV-O Blog & Insights is part of our larger mission:</p>
            <blockquote className="mission-quote">
              Help organizations become truly bionic – where humans, AI, and engineered systems operate as one.
            </blockquote>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default BlogPage;
