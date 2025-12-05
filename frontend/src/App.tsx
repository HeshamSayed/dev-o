import { BrowserRouter, Routes, Route, Navigate, useLocation, useSearchParams } from 'react-router-dom';
import { useEffect } from 'react';
import { useAuthStore } from './store/authStore';
import ScrollToTop from './components/ScrollToTop';
import LoginPage from './pages/LoginPage';
import ChatPage from './pages/ChatPage';
import ProjectsPage from './pages/ProjectsPage';
import ProjectWorkspace from './pages/ProjectWorkspace';
import PricingPage from './pages/PricingPageNew';
import ReferralDashboard from './pages/Referrals/ReferralDashboard';
import LandingPage from './pages/LandingPage/LandingPage';
import FeaturesPage from './pages/FeaturesPage';
import BlogPage from './pages/BlogPage';
import CareersPage from './pages/CareersPage';
import PressPage from './pages/PressPage';
import PartnersPage from './pages/PartnersPage';
import SecurityPage from './pages/SecurityPage';
import TermsPage from './pages/TermsPage';
import PrivacyPage from './pages/PrivacyPage';
import ContactPage from './pages/ContactPage';
import AboutPage from './pages/AboutPage';

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

  return (
    <BrowserRouter>
      <ScrollToTop />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupRoute />} />
        <Route path="/pricing" element={<PricingPage />} />
        <Route path="/features" element={<FeaturesPage />} />
        <Route path="/blog" element={<BlogPage />} />
        <Route path="/careers" element={<CareersPage />} />
        <Route path="/press" element={<PressPage />} />
        <Route path="/partners" element={<PartnersPage />} />
        <Route path="/security" element={<SecurityPage />} />
        <Route path="/terms" element={<TermsPage />} />
        <Route path="/privacy" element={<PrivacyPage />} />
        <Route path="/contact" element={<ContactPage />} />
        <Route path="/about" element={<AboutPage />} />
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
            isAuthenticated ? <Navigate to="/projects" /> : <LandingPage />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
