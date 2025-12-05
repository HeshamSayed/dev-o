/**
 * PricingPage - Display DEV-O pricing tiers with 2-hour reset windows.
 */

import React, { useEffect, useState } from 'react';
import { billingAPI, Plan } from '../api/billing';
import Logo from '../components/Logo/Logo';
import { ChatBubbleIcon, PackageIcon, TimerIcon, CheckmarkIcon } from '../components/Icons/PageIcons';
import './PricingPage.css';

const PricingPage: React.FC = () => {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [loading, setLoading] = useState(true);
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');

  useEffect(() => {
    loadPlans();
  }, []);

  const loadPlans = async () => {
    try {
      const data = await billingAPI.getPlans();
      setPlans(data);
    } catch (error) {
      console.error('Failed to load plans:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (plan: Plan) => {
    const price = billingCycle === 'monthly' ? plan.price_monthly : plan.price_yearly;
    if (price === 0 && plan.plan_type === 'enterprise') {
      return 'Custom';
    }
    if (price === 0) {
      return 'Free';
    }
    const monthlyPrice = billingCycle === 'yearly' ? (price / 12).toFixed(0) : price;
    return `$${monthlyPrice}`;
  };

  const formatLimit = (value: number) => {
    return value === -1 ? 'Unlimited' : value.toLocaleString();
  };

  const getPlanIcon = (planType: string) => {
    switch (planType) {
      case 'free': return 'FREE';
      case 'pro': return 'PRO';
      case 'team': return 'TEAM';
      case 'enterprise': return 'ENTERPRISE';
      default: return 'PLAN';
    }
  };

  const handleSelectPlan = (plan: Plan) => {
    if (plan.plan_type === 'enterprise') {
      window.location.href = 'mailto:sales@dev-o.ai?subject=Enterprise Plan Inquiry';
    } else if (plan.plan_type !== 'free') {
      // TODO: Integrate Stripe checkout
      alert(`Redirecting to checkout for ${plan.name} plan...`);
    }
  };

  if (loading) {
    return (
      <div className="pricing-page">
        <div className="pricing-loading">Loading pricing...</div>
      </div>
    );
  }

  return (
    <div className="pricing-page wavy-scroll">
      <div className="pricing-header">
        <Logo size={60} />
        <h1>Choose Your Plan</h1>
        <p className="pricing-subtitle">
          All plans include 2-hour reset windows for better engagement.
          <br />
          Fresh quotas every 2 hours throughout the day!
        </p>

        <div className="billing-toggle">
          <button
            className={billingCycle === 'monthly' ? 'active' : ''}
            onClick={() => setBillingCycle('monthly')}
          >
            Monthly
          </button>
          <button
            className={billingCycle === 'yearly' ? 'active' : ''}
            onClick={() => setBillingCycle('yearly')}
          >
            Yearly
            <span className="discount-badge">Save 17%</span>
          </button>
        </div>
      </div>

      <div className="pricing-grid">
        {plans.map((plan) => (
          <div
            key={plan.id}
            className={`pricing-card ${plan.plan_type === 'pro' ? 'featured' : ''}`}
          >
            {plan.plan_type === 'pro' && (
              <div className="featured-badge">Most Popular</div>
            )}

            <div className="plan-header">
              <div className="plan-icon">{getPlanIcon(plan.plan_type)}</div>
              <h3>{plan.name}</h3>
              <div className="plan-price">
                <span className="price">{formatPrice(plan)}</span>
                {plan.price_monthly > 0 && (
                  <span className="period">/month</span>
                )}
              </div>
              {billingCycle === 'yearly' && plan.price_yearly > 0 && (
                <div className="yearly-total">
                  ${plan.price_yearly}/year
                </div>
              )}
            </div>

            <button
              className="select-plan-btn"
              onClick={() => handleSelectPlan(plan)}
            >
              {plan.plan_type === 'free' ? 'Get Started' :
               plan.plan_type === 'enterprise' ? 'Contact Sales' :
               'Upgrade Now'}
            </button>

            <div className="plan-features">
              <div className="feature-section">
                <h4><ChatBubbleIcon size={16} /> Chat (per 2-hour window)</h4>
                <ul>
                  <li>{formatLimit(plan.messages_per_window)} messages</li>
                  <li>{formatLimit(plan.max_conversations)} conversations</li>
                  <li>{plan.context_window.toLocaleString()} token context</li>
                </ul>
              </div>

              <div className="feature-section">
                <h4>Projects (per 2-hour window)</h4>
                <ul>
                  <li>{formatLimit(plan.project_requests_per_window)} requests</li>
                  <li>{formatLimit(plan.max_active_projects)} active projects</li>
                  <li>{formatLimit(plan.max_files_per_project)} files per project</li>
                </ul>
              </div>

              <div className="feature-section">
                <h4>AI Agents</h4>
                <ul>
                  {plan.available_agents.length === 4 ? (
                    <li>All 4 expert agents</li>
                  ) : (
                    <li>{plan.available_agents[0]}</li>
                  )}
                  <li>{formatLimit(plan.max_concurrent_agents)} concurrent</li>
                  <li>{plan.model_tier} AI model</li>
                </ul>
              </div>

              <div className="feature-section">
                <h4><PackageIcon size={16} /> Storage & Features</h4>
                <ul>
                  <li>{formatLimit(plan.storage_limit_mb)} MB storage</li>
                  {plan.has_thinking_mode && <li><CheckmarkIcon size={12} /> Thinking mode</li>}
                  {plan.has_download && <li><CheckmarkIcon size={12} /> Project download</li>}
                  {plan.has_git_integration && <li><CheckmarkIcon size={12} /> Git integration</li>}
                  {plan.has_api_access && <li><CheckmarkIcon size={12} /> API access</li>}
                  {plan.has_chat_search && <li><CheckmarkIcon size={12} /> Chat search</li>}
                </ul>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="pricing-footer">
        <div className="reset-info">
          <h3><TimerIcon size={20} /> 2-Hour Reset Windows</h3>
          <p>
            Unlike other platforms with daily limits, DEV-O resets your quotas every 2 hours.
            That means <strong>12 fresh windows per day</strong> to keep you productive!
          </p>
          <div className="window-schedule">
            <div className="window">00:00 - 02:00</div>
            <div className="window">02:00 - 04:00</div>
            <div className="window">04:00 - 06:00</div>
            <div className="dots">...</div>
            <div className="window">22:00 - 00:00</div>
          </div>
        </div>

        <div className="faq-section">
          <h3>Frequently Asked Questions</h3>
          <div className="faq-item">
            <h4>How do 2-hour windows work?</h4>
            <p>
              Every 2 hours (starting at midnight), your message and request quotas reset completely.
              This means you get fresh limits 12 times per day instead of waiting until the next day!
            </p>
          </div>
          <div className="faq-item">
            <h4>Can I upgrade or downgrade anytime?</h4>
            <p>
              Yes! You can change your plan at any time. Upgrades take effect immediately, and downgrades
              will apply at the end of your current billing period.
            </p>
          </div>
          <div className="faq-item">
            <h4>What happens if I hit my limit?</h4>
            <p>
              If you reach your limit, you'll see exactly how many minutes until the next reset.
              You can wait for the reset or upgrade to a higher tier for more capacity.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;
