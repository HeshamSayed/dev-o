import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import './Settings.css';

const Settings: React.FC = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<'profile' | 'preferences' | 'api'>('profile');
  const [profileData, setProfileData] = useState({
    first_name: '',
    last_name: '',
    email: '',
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    if (user) {
      setProfileData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email || '',
      });
    }
  }, [user]);

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      // This would call an update profile endpoint
      // For now, just show success message
      setMessage({ type: 'success', text: 'Profile updated successfully!' });
    } catch (error: any) {
      setMessage({ type: 'error', text: error.message || 'Failed to update profile' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="settings-page">
      <div className="settings-header">
        <h1 className="settings-title">Settings</h1>
        <p className="settings-subtitle">Manage your account and preferences</p>
      </div>

      {/* Tabs */}
      <div className="settings-tabs">
        <button
          className={`settings-tab ${activeTab === 'profile' ? 'active' : ''}`}
          onClick={() => setActiveTab('profile')}
        >
          👤 Profile
        </button>
        <button
          className={`settings-tab ${activeTab === 'preferences' ? 'active' : ''}`}
          onClick={() => setActiveTab('preferences')}
        >
          ⚙️ Preferences
        </button>
        <button
          className={`settings-tab ${activeTab === 'api' ? 'active' : ''}`}
          onClick={() => setActiveTab('api')}
        >
          🔑 API Keys
        </button>
      </div>

      {/* Content */}
      <div className="settings-content">
        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div className="settings-section">
            <h2 className="section-title">Profile Information</h2>
            <p className="section-description">Update your personal information and email address</p>

            {message && (
              <div className={`message ${message.type}`}>
                {message.text}
              </div>
            )}

            <form onSubmit={handleProfileUpdate} className="settings-form">
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="first_name">First Name</label>
                  <input
                    type="text"
                    id="first_name"
                    className="form-input"
                    value={profileData.first_name}
                    onChange={(e) => setProfileData({ ...profileData, first_name: e.target.value })}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="last_name">Last Name</label>
                  <input
                    type="text"
                    id="last_name"
                    className="form-input"
                    value={profileData.last_name}
                    onChange={(e) => setProfileData({ ...profileData, last_name: e.target.value })}
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="email">Email Address</label>
                <input
                  type="email"
                  id="email"
                  className="form-input"
                  value={profileData.email}
                  onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                  disabled
                />
                <p className="form-hint">Email address cannot be changed</p>
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-primary" disabled={loading}>
                  {loading ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </form>

            {/* Danger Zone */}
            <div className="danger-zone">
              <h3 className="danger-zone-title">Danger Zone</h3>
              <div className="danger-zone-content">
                <div className="danger-zone-item">
                  <div>
                    <h4>Delete Account</h4>
                    <p>Permanently delete your account and all associated data</p>
                  </div>
                  <button className="btn-danger">Delete Account</button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Preferences Tab */}
        {activeTab === 'preferences' && (
          <div className="settings-section">
            <h2 className="section-title">Preferences</h2>
            <p className="section-description">Customize your DEV-O experience</p>

            <div className="preference-item">
              <div className="preference-info">
                <h4>Theme</h4>
                <p>Choose your preferred color theme</p>
              </div>
              <select className="preference-select">
                <option value="dark">Dark</option>
                <option value="light">Light</option>
                <option value="auto">Auto</option>
              </select>
            </div>

            <div className="preference-item">
              <div className="preference-info">
                <h4>Language</h4>
                <p>Select your preferred language</p>
              </div>
              <select className="preference-select">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
              </select>
            </div>

            <div className="preference-item">
              <div className="preference-info">
                <h4>Email Notifications</h4>
                <p>Receive email updates about your projects</p>
              </div>
              <label className="toggle-switch">
                <input type="checkbox" defaultChecked />
                <span className="toggle-slider"></span>
              </label>
            </div>

            <div className="preference-item">
              <div className="preference-info">
                <h4>Auto-save Chat History</h4>
                <p>Automatically save your chat conversations</p>
              </div>
              <label className="toggle-switch">
                <input type="checkbox" defaultChecked />
                <span className="toggle-slider"></span>
              </label>
            </div>
          </div>
        )}

        {/* API Keys Tab */}
        {activeTab === 'api' && (
          <div className="settings-section">
            <h2 className="section-title">API Keys</h2>
            <p className="section-description">Manage your API keys for programmatic access</p>

            <div className="api-key-info">
              <p>API keys allow you to integrate DEV-O with your applications. Keep your keys secure and never share them publicly.</p>
            </div>

            <div className="api-key-list">
              <div className="api-key-item">
                <div className="api-key-details">
                  <h4>Production Key</h4>
                  <code className="api-key-value">devo_••••••••••••••••</code>
                  <p className="api-key-meta">Created on Jan 15, 2025</p>
                </div>
                <div className="api-key-actions">
                  <button className="btn-secondary-small">Regenerate</button>
                  <button className="btn-danger-small">Delete</button>
                </div>
              </div>
            </div>

            <button className="btn-primary">+ Create New API Key</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Settings;
