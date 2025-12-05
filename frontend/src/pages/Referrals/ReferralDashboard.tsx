/**
 * Referral Dashboard - Track referrals and rewards
 */

import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getReferralStats,
  getActiveRewards,
  getBonusQuota,
  ReferralStats,
  ReferralReward,
  BonusQuota,
} from '../../api/referral';
import { referralStyles } from './ReferralStyles';

const ReferralDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState<ReferralStats | null>(null);
  const [activeRewards, setActiveRewards] = useState<ReferralReward[]>([]);
  const [bonusQuota, setBonusQuota] = useState<BonusQuota | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    loadReferralData();
  }, []);

  const loadReferralData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [statsData, rewardsData, quotaData] = await Promise.all([
        getReferralStats(),
        getActiveRewards(),
        getBonusQuota(),
      ]);

      setStats(statsData);
      setActiveRewards(rewardsData);
      setBonusQuota(quotaData);
    } catch (err: any) {
      console.error('Failed to load referral data:', err);
      if (err.response?.status === 401) {
        navigate('/login');
      } else {
        setError(err.response?.data?.error || 'Failed to load referral data');
      }
    } finally {
      setLoading(false);
    }
  };

  const copyReferralLink = () => {
    if (stats?.referral_link) {
      navigator.clipboard.writeText(stats.referral_link);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const referralEmailLink = stats?.referral_link
    ? `mailto:?subject=Join%20me%20on%20DEV-O&body=${encodeURIComponent(
        `I'm using DEV-O to orchestrate my engineering work. Here's a link so you can try it (and we both get rewards): ${stats.referral_link}`
      )}`
    : undefined;

  const getRewardTypeLabel = (type: string): string => {
    const labels: Record<string, string> = {
      extra_messages: 'Extra Messages',
      extra_requests: 'Extra Project Requests',
      discount: 'Discount',
      free_upgrade: 'Free Upgrade',
    };
    return labels[type] || type;
  };

  const getStatusBadgeClass = (status: string): string => {
    const classes: Record<string, string> = {
      active: 'status-active',
      pending: 'status-pending',
      redeemed: 'status-redeemed',
      expired: 'status-expired',
    };
    return classes[status] || '';
  };

  const getReferralStatusLabel = (status: string): string => {
    const labels: Record<string, string> = {
      clicked: 'Clicked Link',
      signed_up: 'Signed Up',
      converted: 'Converted to Paid',
    };
    return labels[status] || status;
  };

  const getReferralStatusClass = (status: string): string => {
    const classes: Record<string, string> = {
      clicked: 'referral-clicked',
      signed_up: 'referral-signed-up',
      converted: 'referral-converted',
    };
    return classes[status] || '';
  };

  const formatDate = (dateString: string | null): string => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  if (loading) {
    return (
      <div className="referral-dashboard">
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading referral data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="referral-dashboard">
        <div className="error-container">
          <h2>Error</h2>
          <p>{error}</p>
          <button onClick={loadReferralData} className="btn-retry">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <style>{referralStyles}</style>
      <div className="referral-dashboard">
        <div className="dashboard-container">
        <div className="dashboard-header">
          <div className="header-logo-section">
            <div className="devo-brand">DEV-O</div>
          </div>
          <h1>Referral Program</h1>
          <p className="subtitle">
            Earn bonus quota by inviting friends to DEV-O. Both you and your friends get rewards.
          </p>
        </div>

      {/* Referral Code Section */}
      <div className="referral-code-card">
        <h2>Your Referral Link</h2>
        <div className="code-display">
          <div className="code-box">
            <span className="code-label">Code:</span>
            <span className="code-value">{stats?.code}</span>
          </div>
          <div className="link-box">
            <input
              type="text"
              value={stats?.referral_link || ''}
              readOnly
              className="link-input"
              aria-label="Referral link"
            />
            <button onClick={copyReferralLink} className="btn-copy">
              {copied ? 'Copied!' : 'Copy Link'}
            </button>
          </div>
        </div>
        <p className="code-hint">
          Share this link with friends. When they sign up, you both get bonus quota!
        </p>
      </div>

      {/* Stats Section */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">C</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.total_clicks || 0}</div>
            <div className="stat-label">Total Clicks</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">S</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.total_signups || 0}</div>
            <div className="stat-label">Signups</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">P</div>
          <div className="stat-content">
            <div className="stat-value">{stats?.total_conversions || 0}</div>
            <div className="stat-label">Conversions</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">%</div>
          <div className="stat-content">
            <div className="stat-value">
              {stats?.conversion_rate ? `${stats.conversion_rate.toFixed(1)}%` : '0%'}
            </div>
            <div className="stat-label">Conversion Rate</div>
          </div>
        </div>
      </div>

      {/* Bonus Quota Section */}
      {bonusQuota && (bonusQuota.messages > 0 || bonusQuota.requests > 0) && (
        <div className="bonus-quota-card">
          <h2>Active Bonus Quota</h2>
          <div className="bonus-grid">
            {bonusQuota.messages > 0 && (
              <div className="bonus-item">
                <span className="bonus-icon">M</span>
                <span className="bonus-value">+{bonusQuota.messages}</span>
                <span className="bonus-label">Extra Messages</span>
              </div>
            )}
            {bonusQuota.requests > 0 && (
              <div className="bonus-item">
                <span className="bonus-icon">R</span>
                <span className="bonus-value">+{bonusQuota.requests}</span>
                <span className="bonus-label">Extra Project Requests</span>
              </div>
            )}
          </div>
          <p className="bonus-hint">
            These bonuses are added to your plan limits and reset every 2 hours!
          </p>
        </div>
      )}

      {/* Active Rewards Section */}
      {activeRewards.length > 0 && (
        <div className="rewards-section">
          <h2>Active Rewards</h2>
          <div className="rewards-list">
            {activeRewards.map((reward) => (
              <div key={reward.id} className="reward-card">
                <div className="reward-header">
                  <span className="reward-type">{getRewardTypeLabel(reward.reward_type)}</span>
                  <span className={`reward-status ${getStatusBadgeClass(reward.status)}`}>
                    {reward.status}
                  </span>
                </div>
                <div className="reward-amount">+{reward.amount}</div>
                <div className="reward-description">{reward.description}</div>
                <div className="reward-validity">
                  <span>Valid until: {formatDate(reward.valid_until)}</span>
                  {reward.days_remaining !== null && (
                    <span className="days-remaining">
                      ({reward.days_remaining} days remaining)
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Referrals List */}
      {stats && stats.referrals && stats.referrals.length > 0 && (
        <div className="referrals-section">
          <h2>Your Referrals</h2>
          <div className="referrals-table">
            <table>
              <thead>
                <tr>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Clicked</th>
                  <th>Signed Up</th>
                  <th>Converted</th>
                </tr>
              </thead>
              <tbody>
                {stats.referrals.map((referral) => (
                  <tr key={referral.id}>
                    <td>{referral.referee_email || 'Pending signup'}</td>
                    <td>
                      <span className={`referral-status ${getReferralStatusClass(referral.status)}`}>
                        {getReferralStatusLabel(referral.status)}
                      </span>
                    </td>
                    <td>{formatDate(referral.clicked_at)}</td>
                    <td>{formatDate(referral.signed_up_at)}</td>
                    <td>{formatDate(referral.converted_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* No Referrals Yet */}
      {(!stats?.referrals || stats.referrals.length === 0) && (
        <div className="no-referrals">
          <div className="no-referrals-icon">🎯</div>
          <h3>Kick off your referral streak</h3>
          <p className="no-referrals-message">
            No referrals yet. Start sharing your referral link to earn rewards!
          </p>
          <ul className="no-referrals-perks">
            <li>+5 bonus messages for every successful signup</li>
            <li>+25 project requests when a friend upgrades</li>
            <li>Priority access to upcoming referral raffles</li>
          </ul>
          <div className="no-referrals-actions">
            <button type="button" className="no-referrals-btn" onClick={copyReferralLink}>
              Copy referral link
            </button>
            {referralEmailLink && (
              <a href={referralEmailLink} className="no-referrals-btn secondary">
                Invite via email
              </a>
            )}
          </div>
        </div>
      )}

      {/* How It Works Section */}
      <div className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps-grid">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Share Your Link</h3>
            <p>Share your unique referral link with friends and colleagues.</p>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>They Sign Up</h3>
            <p>When they sign up, both of you receive +5 bonus messages!</p>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>They Upgrade</h3>
            <p>When they upgrade to a paid plan, you get +25 bonus project requests!</p>
          </div>
        </div>
      </div>
      </div>
    </div>
    </>
  );
};

export default ReferralDashboard;
