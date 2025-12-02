import { BrowserRouter, Routes, Route, Navigate, useLocation, useSearchParams } from 'react-router-dom';
import { useEffect } from 'react';
import { useAuthStore } from './store/authStore';
import LoginPage from './pages/LoginPage';
import ChatPage from './pages/ChatPage';
import ProjectsPage from './pages/ProjectsPage';
import ProjectWorkspace from './pages/ProjectWorkspace';
import PricingPage from './pages/PricingPage';
import ReferralDashboard from './pages/Referrals/ReferralDashboard';
import LandingPage from './pages/LandingPage/LandingPage';

// Simple signup redirect component
function SignupRoute() {
  const [searchParams] = useSearchParams();
  const ref = searchParams.get('ref');
  const redirectUrl = ref ? `/login?register=true&ref=${ref}` : '/login?register=true';
  return <Navigate to={redirectUrl} replace />;
}

function App() {
  const { isAuthenticated, fetchUser } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated) {
      fetchUser();
    }
  }, [isAuthenticated]);

  // Check if we're on chat subdomain
  const isChatSubdomain = window.location.hostname === 'chat.dev-o.ai';

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupRoute />} />
        <Route path="/pricing" element={<PricingPage />} />
        <Route
          path="/chat"
          element={isAuthenticated ? <ChatPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/projects"
          element={isAuthenticated ? <ProjectsPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/project/:id"
          element={isAuthenticated ? <ProjectWorkspace /> : <Navigate to="/login" />}
        />
        <Route
          path="/referrals"
          element={isAuthenticated ? <ReferralDashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/"
          element={
            isChatSubdomain
              ? (isAuthenticated ? <ChatPage /> : <Navigate to="/login" />)
              : (isAuthenticated ? <Navigate to="/projects" /> : <LandingPage />)
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
