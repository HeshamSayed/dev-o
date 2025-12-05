import React from 'react';
import { Link } from 'react-router-dom';
import { PageIcon } from '../components/Icons/PageIcon';
import './CareersPage.css';

const CareersPage: React.FC = () => {
  return (
    <div className="careers-page">
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
              <div className="careers-pillar-icon">
                <PageIcon name="robot" size={32} />
              </div>
              <h3>AI & Digital Engineering</h3>
              <p>Making frontier models useful, safe, and grounded in real systems.</p>
            </div>
            <div className="careers-pillar">
              <div className="careers-pillar-icon">
                <PageIcon name="gear" size={32} />
              </div>
              <h3>Automation & Robotics</h3>
              <p>Bringing industrial-grade thinking to software reliability.</p>
            </div>
            <div className="careers-pillar">
              <div className="careers-pillar-icon">
                <PageIcon name="globe" size={32} />
              </div>
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
              <div className="careers-work-icon">
                <PageIcon name="wrench" size={24} />
              </div>
              <h3>Builder Mindset</h3>
              <p>We value shipping, learning, and improving over endless debate.</p>
            </div>
            <div className="careers-work-item">
              <div className="careers-work-icon">
                <PageIcon name="globe" size={24} />
              </div>
              <h3>Remote-Friendly & Async-Aware</h3>
              <p>We embrace written communication, clear documentation, and thoughtful meetings.</p>
            </div>
            <div className="careers-work-item">
              <div className="careers-work-icon">
                <PageIcon name="users" size={24} />
              </div>
              <h3>Small, Empowered Teams</h3>
              <p>People closest to the problem have the context and autonomy to solve it.</p>
            </div>
            <div className="careers-work-item">
              <div className="careers-work-icon">
                <PageIcon name="handshake" size={24} />
              </div>
              <h3>High Trust, High Ownership</h3>
              <p>When we commit to something, we own it end-to-end.</p>
            </div>
            <div className="careers-work-item">
              <div className="careers-work-icon">
                <PageIcon name="chat" size={24} />
              </div>
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
              <div className="careers-team-icon">
                <PageIcon name="bolt" size={28} />
              </div>
              <h3>Engineering & Platform</h3>
              <ul>
                <li>Build the core DEV-O platform, orchestration engine, and knowledge graph.</li>
                <li>Work across backend, data, infrastructure, and developer experience.</li>
                <li>Care deeply about reliability, performance, and elegant system design.</li>
              </ul>
            </div>

            <div className="careers-team-card">
              <div className="careers-team-icon">
                <PageIcon name="brain" size={28} />
              </div>
              <h3>AI & Agents</h3>
              <ul>
                <li>Design, train, and orchestrate AI agents across real engineering workflows.</li>
                <li>Focus on grounding, safety, and explainability of AI-assisted actions.</li>
                <li>Collaborate closely with customers to understand real-world constraints.</li>
              </ul>
            </div>

            <div className="careers-team-card">
              <div className="careers-team-icon">
                <PageIcon name="palette" size={28} />
              </div>
              <h3>Product & Design</h3>
              <ul>
                <li>Turn complex engineering realities into clear, intuitive experiences.</li>
                <li>Craft flows, interfaces, and narratives that help users work with AI confidently.</li>
                <li>Own discovery, prioritization, and iteration with customers.</li>
              </ul>
            </div>

            <div className="careers-team-card">
              <div className="careers-team-icon">
                <PageIcon name="handshake" size={28} />
              </div>
              <h3>Customer, Solutions & Partnerships</h3>
              <ul>
                <li>Work directly with engineering, platform, and SRE teams at our customers.</li>
                <li>Design rollout plans, solution architectures, and success metrics.</li>
                <li>Build long-term partnerships with organizations adopting AI-native ways of working.</li>
              </ul>
            </div>

            <div className="careers-team-card">
              <div className="careers-team-icon">
                <PageIcon name="chart" size={28} />
              </div>
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
              <div className="careers-growth-icon">
                <PageIcon name="book" size={28} />
              </div>
              <h3>Deliberate Learning Time</h3>
              <p>Space for deep work, research, and exploration, not just ticket queues.</p>
            </div>
            <div className="careers-growth-item">
              <div className="careers-growth-icon">
                <PageIcon name="mic" size={28} />
              </div>
              <h3>Tech Talks, Guilds & Sharing Rituals</h3>
              <p>Regular sessions where people walk through architectures, incidents, experiments, and tools.</p>
            </div>
            <div className="careers-growth-item">
              <div className="careers-growth-icon">
                <PageIcon name="shuffle" size={28} />
              </div>
              <h3>Cross-Functional Exposure</h3>
              <p>Opportunities to work across product, engineering, AI, and customer teams.</p>
            </div>
            <div className="careers-growth-item">
              <div className="careers-growth-icon">
                <PageIcon name="lightbulb" size={28} />
              </div>
              <h3>Mentorship & Feedback</h3>
              <p>Clear expectations, supportive feedback, and opportunities to mentor others.</p>
            </div>
            <div className="careers-growth-item">
              <div className="careers-growth-icon">
                <PageIcon name="wrench" size={28} />
              </div>
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
                <span className="careers-dei-icon">
                  <PageIcon name="globe" size={22} />
                </span>
                Hiring and growing people from different backgrounds, geographies, and disciplines.
              </li>
              <li>
                <span className="careers-dei-icon">
                  <PageIcon name="chat" size={22} />
                </span>
                Creating a culture where everyone can contribute ideas safely, regardless of title or location.
              </li>
              <li>
                <span className="careers-dei-icon">
                  <PageIcon name="scale" size={22} />
                </span>
                Designing processes that reduce bias in hiring, performance, and promotion.
              </li>
              <li>
                <span className="careers-dei-icon">
                  <PageIcon name="search" size={22} />
                </span>
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
              <div className="careers-balance-icon">
                <PageIcon name="bolt" size={24} />
              </div>
              <p>We favor <strong>sustainable intensity</strong> over constant urgency.</p>
            </div>
            <div className="careers-balance-item">
              <div className="careers-balance-icon">
                <PageIcon name="target" size={24} />
              </div>
              <p>We respect <strong>focus time</strong>, time off, and personal boundaries.</p>
            </div>
            <div className="careers-balance-item">
              <div className="careers-balance-icon">
                <PageIcon name="clipboard" size={24} />
              </div>
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
              <span className="careers-trait-icon">
                <PageIcon name="hammer" size={18} />
              </span>
              <p>Are <strong>builders at heart</strong> – enjoy turning ideas into real systems, not just talking about them.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon">
                <PageIcon name="waves" size={18} />
              </span>
              <p>Are <strong>comfortable with ambiguity</strong> and change – this space evolves quickly.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon">
                <PageIcon name="puzzle" size={18} />
              </span>
              <p>Can <strong>think in systems</strong>, not just individual tasks.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon">
                <PageIcon name="pen" size={18} />
              </span>
              <p><strong>Communicate clearly</strong> in writing and in conversation.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon">
                <PageIcon name="star" size={18} />
              </span>
              <p>Care about <strong>craft, reliability, and impact</strong>.</p>
            </div>
            <div className="careers-trait">
              <span className="careers-trait-icon">
                <PageIcon name="handshake" size={18} />
              </span>
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
              <div className="careers-why-icon">
                <PageIcon name="rocket" size={24} />
              </div>
              <p>Working on <strong>frontier problems</strong> at the intersection of AI, engineering, and operations.</p>
            </div>
            <div className="careers-why-item">
              <div className="careers-why-icon">
                <PageIcon name="target" size={24} />
              </div>
              <p>Having <strong>real ownership</strong> over product areas, systems, and outcomes.</p>
            </div>
            <div className="careers-why-item">
              <div className="careers-why-icon">
                <PageIcon name="building" size={24} />
              </div>
              <p>Helping shape not just a platform, but a <strong>new way of running engineering organizations</strong>.</p>
            </div>
            <div className="careers-why-item">
              <div className="careers-why-icon">
                <PageIcon name="globe" size={24} />
              </div>
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
              <div className="careers-role-icon">
                <PageIcon name="list" size={24} />
              </div>
              <h3>Browse Open Roles</h3>
              <p>Check our current openings across all teams.</p>
              <a href="#" className="careers-role-link">View Openings →</a>
            </div>
            <div className="careers-role-option">
              <div className="careers-role-icon">
                <PageIcon name="mail" size={24} />
              </div>
              <h3>General Application</h3>
              <p>If you don't see a perfect fit, send a general application describing how you'd like to contribute.</p>
              <a href="#" className="careers-role-link">Apply Now →</a>
            </div>
            <div className="careers-role-option">
              <div className="careers-role-icon">
                <PageIcon name="bell" size={24} />
              </div>
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
