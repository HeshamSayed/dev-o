import Hero from '../../components/Hero/Hero';
import ChatDemo from '../../components/ChatDemo/ChatDemo';
import Features from '../../components/Features/Features';
import Footer from '../../components/Footer/Footer';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <Hero />
      <ChatDemo />
      <Features />
      <Footer />
    </div>
  );
};

export default LandingPage;
