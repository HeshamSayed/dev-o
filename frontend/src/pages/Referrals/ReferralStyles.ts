export const referralStyles = `
  .referral-dashboard {
    min-height: 100vh;
    background: linear-gradient(180deg, #050816 0%, #0a0f1e 50%, #050816 100%);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  }

  .dashboard-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 20px;
  }

  .dashboard-header {
    text-align: center;
    margin-bottom: 50px;
    color: white;
  }

  .devo-brand {
    font-size: 48px;
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
  }

  .dashboard-header h1 {
    font-size: 36px;
    font-weight: bold;
    margin: 0 0 15px 0;
    color: white;
  }

  .subtitle {
    font-size: 18px;
    color: rgba(255, 255, 255, 0.9);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
  }

  .referral-code-card,
  .stat-card,
  .bonus-quota-card,
  .rewards-section,
  .referrals-section,
  .how-it-works,
  .loading-container,
  .error-container {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.02));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .no-referrals {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(88, 101, 242, 0.35), rgba(168, 85, 247, 0.25));
    border: 2px solid rgba(124, 142, 255, 0.6);
    border-radius: 20px;
    padding: 60px 50px;
    margin-bottom: 30px;
    box-shadow: 0 20px 60px rgba(88, 101, 242, 0.6), inset 0 0 80px rgba(88, 101, 242, 0.1);
    text-align: center;
    color: #fff;
  }

  .referral-code-card h2,
  .bonus-quota-card h2,
  .rewards-section h2,
  .referrals-section h2,
  .how-it-works h2 {
    color: #ffffff;
    font-size: 24px;
    margin: 0 0 25px 0;
    font-weight: 600;
  }
  
  .no-referrals h3 {
    font-size: 32px;
    margin-bottom: 16px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.5), 0 0 30px rgba(88, 101, 242, 0.4);
  }
  
  .no-referrals-icon {
    width: 90px;
    height: 90px;
    border-radius: 28px;
    margin: 0 auto 24px;
    font-size: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(124, 142, 255, 0.5), rgba(168, 85, 247, 0.4));
    border: 2px solid rgba(124, 142, 255, 0.8);
    box-shadow: 0 12px 40px rgba(88, 101, 242, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.1) inset;
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);
  }
  
  .no-referrals-message {
    font-size: 18px;
    color: rgba(255, 255, 255, 1);
    margin: 0 0 32px;
    font-weight: 500;
    line-height: 1.6;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }
  
  .no-referrals-perks {
    list-style: none;
    padding: 0;
    margin: 0 0 36px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .no-referrals-perks li {
    background: linear-gradient(135deg, rgba(124, 142, 255, 0.25), rgba(168, 85, 247, 0.15));
    border: 2px solid rgba(124, 142, 255, 0.6);
    border-radius: 12px;
    padding: 18px 20px;
    font-size: 16px;
    line-height: 1.5;
    color: #ffffff;
    font-weight: 600;
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
    box-shadow: 0 4px 12px rgba(88, 101, 242, 0.3);
  }
  
  .no-referrals-perks li:hover {
    background: linear-gradient(135deg, rgba(124, 142, 255, 0.35), rgba(168, 85, 247, 0.25));
    border-color: #7C8EFF;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(88, 101, 242, 0.6), 0 0 0 1px rgba(124, 142, 255, 0.8);
  }
  
  .no-referrals-actions {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 16px;
  }
  
  .no-referrals-btn {
    border: none;
    border-radius: 999px;
    padding: 16px 32px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    color: #ffffff;
    background: linear-gradient(135deg, #5865F2, #A855F7);
    box-shadow: 0 15px 35px rgba(88, 101, 242, 0.4);
    transition: all 0.3s ease;
    text-transform: none;
    letter-spacing: 0.3px;
    text-decoration: none;
    display: inline-block;
  }
  
  .no-referrals-btn.secondary {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.04));
    color: #fff;
    border: 2px solid rgba(124, 142, 255, 0.5);
    box-shadow: 0 8px 20px rgba(88, 101, 242, 0.2);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
  }
  
  .no-referrals-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(88, 101, 242, 0.5);
    background: linear-gradient(135deg, #6b75f7, #b565fa);
  }
  
  .no-referrals-btn.secondary:hover {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.08));
    border-color: #7C8EFF;
    box-shadow: 0 12px 30px rgba(88, 101, 242, 0.35);
  }

  .code-box {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
  }

  .code-label {
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .code-value {
    color: #7C8EFF;
    font-size: 28px;
    font-weight: bold;
    font-family: monospace;
    letter-spacing: 2px;
  }

  .link-box {
    display: flex;
    gap: 10px;
    align-items: stretch;
  }

  .link-input {
    flex: 1;
    padding: 12px 15px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 8px;
    font-size: 14px;
    color: #ffffff;
    background: rgba(255, 255, 255, 0.05);
  }

  .btn-copy {
    padding: 12px 30px;
    background: linear-gradient(135deg, #5865F2, #A855F7);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.3s ease;
  }

  .btn-copy:hover {
    background: linear-gradient(135deg, #6b75f7, #b565fa);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(88, 101, 242, 0.4);
  }
  
  .code-hint,
  .bonus-hint,
  .reward-description,
  .reward-validity {
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    line-height: 1.6;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 25px;
    margin-bottom: 30px;
  }

  .stat-icon {
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #5865F2, #A855F7);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 15px;
    color: white;
    font-size: 20px;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(88, 101, 242, 0.4);
  }

  .stat-content {
    text-align: center;
  }

  .stat-value {
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 5px;
    line-height: 1;
  }

  .stat-label {
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .bonus-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
  }

  .bonus-item {
    background: linear-gradient(135deg, rgba(124, 142, 255, 0.15), rgba(168, 85, 247, 0.1));
    border: 2px solid rgba(124, 142, 255, 0.4);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(88, 101, 242, 0.2);
  }

  .bonus-icon {
    color: #7C8EFF;
    font-size: 24px;
    font-weight: bold;
    display: block;
    margin-bottom: 10px;
  }

  .bonus-value {
    font-size: 36px;
    font-weight: bold;
    color: #ffffff;
    display: block;
    margin-bottom: 5px;
  }

  .bonus-label {
    color: rgba(255, 255, 255, 0.8);
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: block;
  }

  .rewards-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
  }

  .reward-card {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    border-left: 4px solid #7C8EFF;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .reward-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    flex-wrap: wrap;
    gap: 10px;
  }

  .reward-type {
    color: #ffffff;
    font-size: 16px;
    font-weight: 600;
  }

  .reward-status {
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    display: inline-block;
  }

  .status-active {
    background: #c6f6d5;
    color: #22543d;
  }

  .status-pending {
    background: #fed7aa;
    color: #744210;
  }

  .status-redeemed {
    background: #bee3f8;
    color: #2a4e7c;
  }

  .status-expired {
    background: #fed7d7;
    color: #742a2a;
  }

  .reward-amount {
    font-size: 28px;
    font-weight: bold;
    color: #7C8EFF;
    margin-bottom: 10px;
  }

  .referrals-table {
    width: 100%;
    overflow-x: auto;
  }

  .referrals-table table {
    width: 100%;
    border-collapse: collapse;
    min-width: 600px;
  }

  .referrals-table th {
    background: rgba(255, 255, 255, 0.05);
    padding: 12px;
    text-align: left;
    font-weight: 600;
    color: #ffffff;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    font-size: 14px;
  }

  .referrals-table td {
    padding: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;
  }

  .referral-status {
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    display: inline-block;
  }

  .referral-clicked {
    background: #fed7aa;
    color: #744210;
  }

  .referral-signed-up {
    background: #bee3f8;
    color: #2a4e7c;
  }

  .referral-converted {
    background: #c6f6d5;
    color: #22543d;
  }

  .steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
  }

  .step {
    text-align: center;
    padding: 20px;
  }

  .step-number {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #5865F2, #A855F7);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
    margin: 0 auto 20px;
    box-shadow: 0 8px 20px rgba(88, 101, 242, 0.4);
  }

  .step h3 {
    color: #ffffff;
    font-size: 20px;
    margin: 0 0 10px 0;
    font-weight: 600;
  }

  .step p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
  }

  .spinner {
    width: 50px;
    height: 50px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid #7C8EFF;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .btn-retry {
    background: linear-gradient(135deg, #5865F2, #A855F7);
    color: white;
    padding: 12px 30px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .btn-retry:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(88, 101, 242, 0.4);
  }

  @media (max-width: 768px) {
    .dashboard-container {
      padding: 20px 15px;
    }

    .stats-grid {
      grid-template-columns: 1fr;
    }

    .link-box {
      flex-direction: column;
    }

    .link-input,
    .btn-copy {
      width: 100%;
    }
  }
`;