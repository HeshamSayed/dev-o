import { Link } from 'react-router-dom';
import Footer from '../components/Footer/Footer';
import './TermsPage.css';

// SVG Icon Components
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

const TermsPage = () => {
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="terms-page">
      {/* Navigation */}
      <nav className="terms-nav">
        <div className="terms-nav-container">
          <Link to="/" className="terms-logo">
            <img src="/src/components/Logo/logo+icon.png" alt="DEV-O" className="terms-logo-image" />
          </Link>
          <div className="terms-nav-links">
            <Link to="/features">Features</Link>
            <Link to="/pricing">Pricing</Link>
            <Link to="/partners">Partners</Link>
            <Link to="/blog">Blog</Link>
          </div>
          <Link to="/login" className="terms-nav-cta">Get Started</Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="terms-hero">
        <div className="terms-hero-content">
          <div className="terms-hero-badge">
            <FileTextIcon />
            <span>Legal</span>
          </div>
          <h1>Terms of Service</h1>
          <p>
            These Terms of Service ("Terms") govern your access to and use of the DEV-O platform, 
            websites, APIs, and related services (collectively, the "Services") provided by 
            Bionicverse Inc. (USA) ("Bionicverse", "we", "us", or "our").
          </p>
          <p className="terms-hero-note">
            By accessing or using the Services, you agree to be bound by these Terms. If you are 
            accepting these Terms on behalf of a company or other legal entity, you represent that 
            you have authority to bind that entity, and "you" or "Customer" will refer to that entity.
          </p>
        </div>
      </section>

      {/* Table of Contents */}
      <aside className="terms-toc">
        <h3>Contents</h3>
        <ul>
          <li><button onClick={() => scrollToSection('who-we-are')}>1. Who We Are</button></li>
          <li><button onClick={() => scrollToSection('eligibility')}>2. Eligibility & Accounts</button></li>
          <li><button onClick={() => scrollToSection('use-of-services')}>3. Use of the Services</button></li>
          <li><button onClick={() => scrollToSection('beta-features')}>4. Beta Features</button></li>
          <li><button onClick={() => scrollToSection('availability')}>5. Availability</button></li>
          <li><button onClick={() => scrollToSection('fees')}>6. Fees & Payment</button></li>
          <li><button onClick={() => scrollToSection('intellectual-property')}>7. Intellectual Property</button></li>
          <li><button onClick={() => scrollToSection('data-protection')}>8. Data Protection</button></li>
          <li><button onClick={() => scrollToSection('confidentiality')}>9. Confidentiality</button></li>
          <li><button onClick={() => scrollToSection('disclaimers')}>10. Disclaimers</button></li>
          <li><button onClick={() => scrollToSection('limitation')}>11. Limitation of Liability</button></li>
          <li><button onClick={() => scrollToSection('indemnification')}>12. Indemnification</button></li>
          <li><button onClick={() => scrollToSection('term')}>13. Term & Termination</button></li>
          <li><button onClick={() => scrollToSection('governing-law')}>14. Governing Law</button></li>
          <li><button onClick={() => scrollToSection('export')}>15. Export & Compliance</button></li>
          <li><button onClick={() => scrollToSection('changes')}>16. Changes to Terms</button></li>
          <li><button onClick={() => scrollToSection('miscellaneous')}>17. Miscellaneous</button></li>
          <li><button onClick={() => scrollToSection('contact')}>18. Contact</button></li>
        </ul>
      </aside>

      {/* Main Content */}
      <main className="terms-main">
        {/* Section 1 */}
        <section id="who-we-are" className="terms-section">
          <h2>1. Who We Are</h2>
          <p>The Services are operated by:</p>
          <div className="company-info">
            <p><strong>Bionicverse Inc.</strong></p>
            <p>5830 E 2nd St, Ste 7000 #9656</p>
            <p>Casper, Wyoming 82609</p>
            <p>United States</p>
          </div>
          <p>If you have questions about these Terms, you may contact us at:</p>
          <p className="contact-email"><a href="mailto:legal@dev-o.ai">legal@dev-o.ai</a></p>
        </section>

        {/* Section 2 */}
        <section id="eligibility" className="terms-section">
          <h2>2. Eligibility & Accounts</h2>
          
          <h3>2.1 Eligibility</h3>
          <p>
            The Services are intended for use by organizations and individuals acting in a professional capacity. 
            By using the Services, you represent and warrant that:
          </p>
          <ul>
            <li>You are at least the age of majority in your jurisdiction, and</li>
            <li>You have the authority to enter into these Terms personally or on behalf of your organization.</li>
          </ul>
          <p>The Services are not intended for children under the age of 16.</p>

          <h3>2.2 Accounts & Access</h3>
          <p>To use certain parts of the Services, you may need to create an account or access the Services through your organization's account.</p>
          <p>You agree to:</p>
          <ul>
            <li>Provide accurate and complete information when creating an account,</li>
            <li>Keep your login credentials confidential,</li>
            <li>Notify us or your organization promptly in case of any suspected unauthorized access.</li>
          </ul>
          <p>You are responsible for all activities that occur under your account, unless you promptly notify us of unauthorized use.</p>

          <h3>2.3 Organization Accounts</h3>
          <p>If you access the Services as part of an organization (for example, your employer):</p>
          <ul>
            <li>Your use may be subject to that organization's policies and instructions,</li>
            <li>The organization may control and administer your account and data within the Services,</li>
            <li>We are not responsible for any internal arrangements between you and the organization.</li>
          </ul>
        </section>

        {/* Section 3 */}
        <section id="use-of-services" className="terms-section">
          <h2>3. Use of the Services</h2>
          
          <h3>3.1 License to Use the Services</h3>
          <p>
            Subject to these Terms and any applicable order form or agreement, we grant you a limited, 
            non-exclusive, non-transferable, non-sublicensable license to access and use the Services 
            for your internal business purposes.
          </p>

          <h3>3.2 Acceptable Use</h3>
          <p>You agree not to:</p>
          <ul>
            <li>Use the Services in violation of any applicable law or regulation,</li>
            <li>Reverse engineer, decompile, or attempt to derive the source code of the Services (except to the extent permitted by law),</li>
            <li>Access the Services in order to build a competing product or service,</li>
            <li>Interfere with or disrupt the integrity or performance of the Services,</li>
            <li>Use the Services to transmit malicious code, spam, or harmful content,</li>
            <li>Misrepresent your identity or affiliation with any person or entity,</li>
            <li>Use the Services in a way that infringes or violates third-party rights (including privacy or intellectual property rights).</li>
          </ul>
          <p>
            We may, without liability, suspend or restrict access to the Services if we reasonably believe 
            you are violating these Terms, creating a security risk, or causing harm to the Services or others.
          </p>

          <h3>3.3 Third-Party Services & Integrations</h3>
          <p>
            The Services may integrate with third-party products, services, or platforms (e.g., code repositories, 
            issue trackers, observability tools, identity providers). Your use of such third-party services is 
            subject to their own terms and policies.
          </p>
          <p>
            We do not control and are not responsible for third-party services. Integrations may require us to 
            exchange certain data with those services as configured by you or your organization.
          </p>
        </section>

        {/* Section 4 */}
        <section id="beta-features" className="terms-section">
          <h2>4. Beta, Preview & Experimental Features</h2>
          <p>
            From time to time, we may offer access to features or services labeled as beta, preview, 
            early access, or similar ("Beta Features").
          </p>
          <p>You acknowledge that Beta Features:</p>
          <ul>
            <li>May be experimental, incomplete, or change at any time,</li>
            <li>May not be covered by the same support or availability commitments as the main Services,</li>
            <li>Are provided "as is" without warranties of any kind.</li>
          </ul>
          <p>We may discontinue Beta Features at any time, in our discretion.</p>
        </section>

        {/* Section 5 */}
        <section id="availability" className="terms-section">
          <h2>5. Availability & Modifications</h2>
          <p>We aim to provide reliable Services, but:</p>
          <ul>
            <li>The Services may occasionally be unavailable due to maintenance, updates, or factors beyond our control,</li>
            <li>We may modify, update, or discontinue parts of the Services from time to time.</li>
          </ul>
          <p>
            Where feasible and appropriate, we will provide notice of material changes that significantly 
            affect your use of the Services.
          </p>
        </section>

        {/* Section 6 */}
        <section id="fees" className="terms-section">
          <h2>6. Fees & Payment (If Applicable)</h2>
          <p>If you purchase paid Services or enter into an order form or subscription:</p>
          <ul>
            <li>Pricing, payment terms, and any additional conditions will be described in your order or separate commercial agreement,</li>
            <li>You agree to pay the applicable fees in accordance with those terms,</li>
            <li>Fees are typically non-refundable unless explicitly stated otherwise.</li>
          </ul>
          <p>
            Late payments may result in suspension or termination of access to the Services, subject to 
            any notice requirements in your agreement.
          </p>
          <p>
            If you are using a trial or evaluation version of the Services, your access may be limited 
            in time, features, or usage.
          </p>
        </section>

        {/* Section 7 */}
        <section id="intellectual-property" className="terms-section">
          <h2>7. Intellectual Property</h2>
          
          <h3>7.1 Our IP</h3>
          <p>
            The Services, including all software, user interfaces, designs, documentation, and underlying 
            technology, are owned by Bionicverse Inc. or its licensors and are protected by intellectual property laws.
          </p>
          <p>
            Except for the limited rights expressly granted to you in these Terms, we reserve all rights, 
            title, and interest in and to the Services.
          </p>

          <h3>7.2 Your Content & Customer Data</h3>
          <p>
            "Customer Data" means data, content, and other information that you or your users submit to the 
            Services (including through integrations), excluding system-generated data and our own content.
          </p>
          <p>
            As between you and us, you retain all rights in your Customer Data. You grant us a limited, 
            non-exclusive, worldwide license to use, host, process, transmit, and display Customer Data solely to:
          </p>
          <ul>
            <li>Provide, maintain, and improve the Services,</li>
            <li>Prevent or address service, security, or technical issues,</li>
            <li>Comply with applicable laws and legal requests.</li>
          </ul>
          <p>
            Where we process personal information as part of Customer Data on behalf of a Customer, we do so 
            as a processor/service provider in accordance with our data protection or processing agreements.
          </p>

          <h3>7.3 Feedback</h3>
          <p>
            If you provide feedback, suggestions, or ideas about the Services ("Feedback"), you agree that 
            we may use such Feedback without restriction or obligation to you.
          </p>
          <p>
            You will not provide Feedback containing confidential or third-party proprietary information 
            unless you are permitted to do so.
          </p>
        </section>

        {/* Section 8 */}
        <section id="data-protection" className="terms-section">
          <h2>8. Data Protection & Privacy</h2>
          <p>
            Your use of the Services is also subject to our <Link to="/privacy">Privacy Policy</Link>, 
            which explains how we collect, use, and protect personal information. The Privacy Policy forms part of these Terms.
          </p>
          <p>
            If your organization requires a separate data processing agreement or similar, that document 
            will govern our processing of personal information on your behalf.
          </p>
        </section>

        {/* Section 9 */}
        <section id="confidentiality" className="terms-section">
          <h2>9. Confidentiality</h2>
          <p>
            "Confidential Information" means non-public information disclosed by one party ("Disclosing Party") 
            to the other party ("Receiving Party") that is marked or identified as confidential, or that should 
            reasonably be understood to be confidential given the nature of the information and circumstances.
          </p>
          <p>The Receiving Party agrees to:</p>
          <ul>
            <li>Use Confidential Information only for purposes consistent with these Terms and any applicable agreements,</li>
            <li>Protect Confidential Information with at least reasonable care,</li>
            <li>Not disclose Confidential Information to third parties except as permitted under these Terms.</li>
          </ul>
          <p>Confidential Information does not include information that:</p>
          <ul>
            <li>Is or becomes publicly available through no fault of the Receiving Party,</li>
            <li>Was lawfully known to the Receiving Party before disclosure,</li>
            <li>Is received from a third party without breach of confidentiality,</li>
            <li>Is independently developed by the Receiving Party without use of the Disclosing Party's Confidential Information.</li>
          </ul>
          <p>
            The Receiving Party may disclose Confidential Information if required by law or legal process, 
            provided it (where legally permitted) gives the Disclosing Party reasonable notice to seek protection.
          </p>
        </section>

        {/* Section 10 */}
        <section id="disclaimers" className="terms-section">
          <h2>10. Disclaimers</h2>
          <p>
            To the maximum extent permitted by law, the Services are provided on an "as is" and "as available" basis.
          </p>
          <p>We and our affiliates, licensors, and suppliers:</p>
          <ul>
            <li>Do not guarantee that the Services will be uninterrupted, error-free, or completely secure,</li>
            <li>Do not make any warranties, express or implied, including implied warranties of merchantability, fitness for a particular purpose, or non-infringement.</li>
          </ul>
          <p>
            You are responsible for determining whether the Services meet your requirements, including with 
            respect to compliance, security, and regulatory obligations applicable to your organization.
          </p>
        </section>

        {/* Section 11 */}
        <section id="limitation" className="terms-section">
          <h2>11. Limitation of Liability</h2>
          <p>To the maximum extent permitted by law:</p>
          
          <h3>Exclusion of Indirect Damages</h3>
          <p>
            Neither party will be liable to the other for any indirect, incidental, special, consequential, 
            or punitive damages, or for any loss of profits, revenues, savings, or data, even if advised 
            of the possibility of such damages.
          </p>

          <h3>Cap on Direct Damages</h3>
          <p>
            Our total aggregate liability arising out of or related to the Services and these Terms will be 
            limited to the greater of:
          </p>
          <ul>
            <li>The amount you paid to us for the Services in the twelve (12) months preceding the event giving rise to the claim; or</li>
            <li>USD $1,000.</li>
          </ul>
          <p>
            These limitations will apply regardless of the form of action (contract, tort, negligence, 
            strict liability, etc.) and even if a remedy fails of its essential purpose.
          </p>
          <p>
            Some jurisdictions do not allow certain limitations; in such cases, these limitations will 
            apply to the fullest extent permitted by law.
          </p>
        </section>

        {/* Section 12 */}
        <section id="indemnification" className="terms-section">
          <h2>12. Indemnification</h2>
          <p>
            You agree to indemnify and hold harmless Bionicverse Inc., its affiliates, officers, directors, 
            employees, and agents from and against any claims, damages, liabilities, losses, and expenses 
            (including reasonable attorneys' fees) arising out of or related to:
          </p>
          <ul>
            <li>Your use of the Services in violation of these Terms,</li>
            <li>Customer Data that infringes or misappropriates any third-party rights or violates applicable law,</li>
            <li>Your breach of any representations or warranties in these Terms.</li>
          </ul>
        </section>

        {/* Section 13 */}
        <section id="term" className="terms-section">
          <h2>13. Term & Termination</h2>
          <p>These Terms apply from the time you first access the Services and continue until terminated.</p>
          <p>We may suspend or terminate your access to the Services if:</p>
          <ul>
            <li>You materially breach these Terms or any applicable agreement and fail to cure within a reasonable period after notice, or</li>
            <li>We reasonably believe your use of the Services poses a security or legal risk.</li>
          </ul>
          <p>
            You may stop using the Services at any time. If you have a separate commercial agreement or 
            subscription, the termination provisions in that agreement will also apply.
          </p>
          <p>Upon termination:</p>
          <ul>
            <li>Your right to access and use the Services will cease,</li>
            <li>We may deactivate or delete your account and related data, subject to our data retention and legal obligations.</li>
          </ul>
        </section>

        {/* Section 14 */}
        <section id="governing-law" className="terms-section">
          <h2>14. Governing Law & Dispute Resolution</h2>
          <p>
            These Terms and any dispute arising out of or relating to them or the Services will be governed 
            by and construed in accordance with the laws of the State of Wyoming, United States, without 
            regard to its conflict of law principles.
          </p>
          <p>
            You agree that any legal action or proceeding arising under or relating to these Terms will be 
            brought exclusively in the state or federal courts located in Wyoming, USA, and you consent to 
            the personal jurisdiction and venue of such courts.
          </p>
          <p>
            If required by local law, other dispute resolution mechanisms may apply in specific jurisdictions; 
            these can be addressed in a separate or localized version of these Terms.
          </p>
        </section>

        {/* Section 15 */}
        <section id="export" className="terms-section">
          <h2>15. Export & Compliance</h2>
          <p>You agree to comply with all applicable export control, sanctions, and trade laws and regulations.</p>
          <p>You may not use or access the Services if:</p>
          <ul>
            <li>You are located in a jurisdiction subject to comprehensive sanctions, or</li>
            <li>You are on any U.S. or other applicable government restricted party list.</li>
          </ul>
          <p>
            You are responsible for ensuring that your use of the Services complies with any industry-specific 
            regulations or internal policies applicable to your organization.
          </p>
        </section>

        {/* Section 16 */}
        <section id="changes" className="terms-section">
          <h2>16. Changes to These Terms</h2>
          <p>We may update these Terms from time to time. When we make material changes, we will:</p>
          <ul>
            <li>Update the "Last updated" date at the top of this page, and</li>
            <li>Provide additional notice where appropriate (for example, via email or in-product notification).</li>
          </ul>
          <p>
            Your continued use of the Services after changes become effective constitutes your acceptance 
            of the updated Terms.
          </p>
          <p>If you do not agree with the updated Terms, you must stop using the Services.</p>
        </section>

        {/* Section 17 */}
        <section id="miscellaneous" className="terms-section">
          <h2>17. Miscellaneous</h2>
          <ul className="misc-list">
            <li>
              <strong>Entire Agreement</strong> – These Terms, together with any applicable order forms or 
              separate written agreements, constitute the entire agreement between you and us regarding the Services.
            </li>
            <li>
              <strong>Severability</strong> – If any provision of these Terms is found to be invalid or 
              unenforceable, the remaining provisions will remain in full force and effect.
            </li>
            <li>
              <strong>No Waiver</strong> – Our failure to enforce any provision of these Terms will not be 
              deemed a waiver of our right to do so later.
            </li>
            <li>
              <strong>Assignment</strong> – You may not assign or transfer these Terms without our prior 
              written consent. We may assign these Terms in connection with a merger, acquisition, or sale 
              of assets, or to an affiliate.
            </li>
            <li>
              <strong>Third-Party Beneficiaries</strong> – These Terms do not create any third-party beneficiary rights.
            </li>
          </ul>
        </section>

        {/* Section 18 */}
        <section id="contact" className="terms-section contact-section">
          <h2>18. Contact</h2>
          <p>If you have questions about these Terms or the Services, please contact us at:</p>
          
          <div className="contact-info">
            <div className="contact-address">
              <MapPinIcon />
              <div>
                <p><strong>Bionicverse Inc.</strong></p>
                <p>(Attn: Legal / DEV-O)</p>
                <p>5830 E 2nd St, Ste 7000 #9656</p>
                <p>Casper, Wyoming 82609</p>
                <p>United States</p>
              </div>
            </div>
            <div className="contact-email-box">
              <MailIcon />
              <a href="mailto:legal@dev-o.ai">legal@dev-o.ai</a>
            </div>
          </div>
        </section>

        {/* Closing */}
        <section className="terms-closing">
          <h2>DEV-O – Digital Engineering Virtual Orchestrator</h2>
          <p>A project by <strong>Bionicverse Inc.</strong> (USA)</p>
          <p className="closing-message">
            Thank you for using DEV-O to help build AI-native engineering organizations.
          </p>
        </section>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default TermsPage;
