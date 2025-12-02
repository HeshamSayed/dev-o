import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { trackReferralClick } from '../api/referral';
import Logo from '../components/Logo/Logo';
import './LoginPage.css';

export default function LoginPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { login, register } = useAuthStore();

  // Check if register parameter is present to show register tab
  const shouldShowRegister = searchParams.get('register') === 'true';

  const [isLogin, setIsLogin] = useState(!shouldShowRegister);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [referralTracked, setReferralTracked] = useState(false);

  // Track referral click on page load
  useEffect(() => {
    const referralCode = searchParams.get('ref');
    if (referralCode && !referralTracked) {
      trackReferral(referralCode);
    }
  }, [searchParams, referralTracked]);

  const trackReferral = async (referralCode: string) => {
    try {
      const response = await trackReferralClick(referralCode);
      // Store referral ID in sessionStorage for signup attribution
      sessionStorage.setItem('referral_id', response.referral_id);
      setReferralTracked(true);
      console.log('Referral click tracked:', referralCode);
    } catch (err) {
      console.error('Failed to track referral:', err);
      // Don't show error to user - this is background tracking
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate confirm password for registration
    if (!isLogin && password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(email, password, username || email, firstName, lastName);
      }
      navigate('/chat');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <Logo size={200} showText={true} />
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-tabs">
            <button
              type="button"
              className={isLogin ? 'active' : ''}
              onClick={() => setIsLogin(true)}
            >
              Login
            </button>
            <button
              type="button"
              className={!isLogin ? 'active' : ''}
              onClick={() => setIsLogin(false)}
            >
              Register
            </button>
          </div>

          {error && <div className="error-message">{error}</div>}

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          {!isLogin && (
            <>
              <input
                type="text"
                placeholder="First Name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required={!isLogin}
              />

              <input
                type="text"
                placeholder="Last Name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required={!isLogin}
              />
            </>
          )}

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {!isLogin && (
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required={!isLogin}
            />
          )}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Please wait...' : isLogin ? 'Login' : 'Register'}
          </button>
        </form>
      </div>
    </div>
  );
}
