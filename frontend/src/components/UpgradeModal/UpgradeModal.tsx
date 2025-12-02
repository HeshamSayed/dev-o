/**
 * UpgradeModal - Shown when user hits usage limits.
 */

import React from 'react';
import './UpgradeModal.css';

interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  limitType: 'chat' | 'project';
  used: number;
  limit: number;
  minutesUntilReset: number;
}

const UpgradeModal: React.FC<UpgradeModalProps> = ({
  isOpen,
  onClose,
  limitType,
  used,
  limit,
  minutesUntilReset,
}) => {
  if (!isOpen) return null;

  const getLimitIcon = () => {
    return limitType === 'chat' ? 'CHAT' : 'PROJECT';
  };

  const getLimitName = () => {
    return limitType === 'chat' ? 'Chat Messages' : 'Project Requests';
  };

  const handleUpgrade = () => {
    window.location.href = '/pricing';
  };

  const formatTime = (minutes: number) => {
    if (minutes < 60) {
      return `${minutes} minute${minutes !== 1 ? 's' : ''}`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}h ${mins}m` : `${hours} hour${hours !== 1 ? 's' : ''}`;
  };

  return (
    <div className="upgrade-modal-overlay" onClick={onClose}>
      <div className="upgrade-modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M18 6L6 18M6 6l12 12" strokeWidth="2" strokeLinecap="round" />
          </svg>
        </button>

        <div className="modal-icon limit-reached">
          {getLimitIcon()}
        </div>

        <h2>Limit Reached</h2>
        <p className="modal-subtitle">
          You've used all {used} of your {getLimitName().toLowerCase()} for this 2-hour window.
        </p>

        <div className="limit-stats">
          <div className="stat-card">
            <div className="stat-label">Used</div>
            <div className="stat-value">{used}</div>
          </div>
          <div className="stat-divider">/</div>
          <div className="stat-card">
            <div className="stat-label">Limit</div>
            <div className="stat-value">{limit}</div>
          </div>
        </div>

        <div className="reset-timer">
          <svg className="timer-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" strokeWidth="2" />
            <path d="M12 6v6l4 2" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <span>Resets in {formatTime(minutesUntilReset)}</span>
        </div>

        <div className="modal-options">
          <div className="option wait">
            <h3>⏱️ Wait for Reset</h3>
            <p>Your quota will refresh automatically in {formatTime(minutesUntilReset)}.</p>
            <button className="option-btn secondary" onClick={onClose}>
              I'll Wait
            </button>
          </div>

          <div className="option upgrade">
            <h3>Upgrade to Pro</h3>
            <p>Get 10x more capacity with 2-hour resets. Only $19/month!</p>
            <ul className="benefits">
              <li>100 chat messages per window (vs 10)</li>
              <li>20 project requests per window (vs 2)</li>
              <li>All 4 expert AI agents</li>
              <li>Thinking mode & more features</li>
            </ul>
            <button className="option-btn primary" onClick={handleUpgrade}>
              View Pricing
            </button>
          </div>
        </div>

        <div className="modal-footer">
          <p>
            <strong>Did you know?</strong> Unlike other platforms with daily limits,
            DEV-O resets your quota every 2 hours for maximum productivity!
          </p>
        </div>
      </div>
    </div>
  );
};

export default UpgradeModal;
