/**
 * UsageIndicator component - Shows current usage with 2-hour reset timer.
 */

import React, { useEffect, useState } from 'react';
import { billingAPI, UsageSummary } from '../../api/billing';
import './UsageIndicator.css';

interface UsageIndicatorProps {
  compact?: boolean;
}

const UsageIndicator: React.FC<UsageIndicatorProps> = ({ compact = false }) => {
  const [usage, setUsage] = useState<UsageSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUsage = async () => {
    try {
      const summary = await billingAPI.getUsageSummary();
      setUsage(summary);
      setError(null);
    } catch (err: any) {
      console.error('Failed to fetch usage:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsage();

    // Refresh every minute
    const interval = setInterval(fetchUsage, 60000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className={`usage-indicator ${compact ? 'compact' : ''}`}>
        <div className="usage-loading">Loading usage...</div>
      </div>
    );
  }

  if (error || !usage) {
    return null;
  }

  const chatPercentage = usage.chat.limit === -1
    ? 0
    : (usage.chat.used / usage.chat.limit) * 100;

  const projectsPercentage = usage.projects.limit === -1
    ? 0
    : (usage.projects.used / usage.projects.limit) * 100;

  const formatLimit = (limit: number) => {
    return limit === -1 ? '∞' : limit;
  };

  const formatRemaining = (remaining: number) => {
    return remaining === -1 ? '∞' : remaining;
  };

  const getUsageColor = (percentage: number) => {
    if (percentage >= 90) return 'danger';
    if (percentage >= 70) return 'warning';
    return 'normal';
  };

  if (compact) {
    return (
      <div className="usage-indicator compact">
        <div className="usage-timer">
          <svg className="timer-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" strokeWidth="2" />
            <path d="M12 6v6l4 2" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <span>{usage.window.minutes_until_reset}m</span>
        </div>
        <div className="usage-stats-compact">
          <span className={`stat ${getUsageColor(chatPercentage)}`}>
            Chat: {usage.chat.used}/{formatLimit(usage.chat.limit)}
          </span>
          <span className={`stat ${getUsageColor(projectsPercentage)}`}>
            Projects: {usage.projects.used}/{formatLimit(usage.projects.limit)}
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="usage-indicator">
      <div className="usage-header">
        <div className="plan-info">
          <span className="plan-name">{usage.plan.name}</span>
          <span className="plan-type">{usage.plan.type.toUpperCase()}</span>
        </div>
        <div className="reset-timer">
          <svg className="timer-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" strokeWidth="2" />
            <path d="M12 6v6l4 2" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <span>Resets in {usage.window.minutes_until_reset} min</span>
        </div>
      </div>

      <div className="usage-section">
        <div className="usage-item">
          <div className="usage-label">
            <span>💬 Chat Messages</span>
            <span className="usage-count">
              {usage.chat.used} / {formatLimit(usage.chat.limit)}
            </span>
          </div>
          {usage.chat.limit !== -1 && (
            <div className="usage-bar">
              <div
                className={`usage-fill ${getUsageColor(chatPercentage)}`}
                style={{ width: `${Math.min(chatPercentage, 100)}%` }}
              />
            </div>
          )}
          <div className="usage-remaining">
            {formatRemaining(usage.chat.remaining)} remaining
          </div>
        </div>

        <div className="usage-item">
          <div className="usage-label">
            <span>Project Requests</span>
            <span className="usage-count">
              {usage.projects.used} / {formatLimit(usage.projects.limit)}
            </span>
          </div>
          {usage.projects.limit !== -1 && (
            <div className="usage-bar">
              <div
                className={`usage-fill ${getUsageColor(projectsPercentage)}`}
                style={{ width: `${Math.min(projectsPercentage, 100)}%` }}
              />
            </div>
          )}
          <div className="usage-remaining">
            {formatRemaining(usage.projects.remaining)} remaining
          </div>
        </div>
      </div>

      {(chatPercentage >= 80 || projectsPercentage >= 80) && usage.plan.type === 'free' && (
        <div className="upgrade-hint">
          <span>Running low? </span>
          <a href="/pricing" className="upgrade-link">Upgrade to Pro</a>
          <span> for 10x more!</span>
        </div>
      )}
    </div>
  );
};

export default UsageIndicator;
