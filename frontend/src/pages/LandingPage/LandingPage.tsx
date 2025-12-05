import Hero from '../../components/Hero/Hero';
import ChatDemo from '../../components/ChatDemo/ChatDemo';
import Features from '../../components/Features/Features';
import Footer from '../../components/Footer/Footer';
import WaveDivider from '../../components/WaveDivider/WaveDivider';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <Hero />
      <div className="section-with-wave">
        <WaveDivider position="top" variant="wave1" color="#0d1225" flip />
        <ChatDemo />
        <WaveDivider position="bottom" variant="wave2" color="#0a0e27" />
      </div>
      <Features />
      <WaveDivider position="top" variant="wave3" color="#060912" flip />
      <Footer />
    </div>
  );
};

export default LandingPage;
