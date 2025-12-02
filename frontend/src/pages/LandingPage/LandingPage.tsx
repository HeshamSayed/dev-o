import Hero from '../../components/Hero/Hero';
import ChatDemo from '../../components/ChatDemo/ChatDemo';
import Features from '../../components/Features/Features';
import AgentDemo from '../../components/AgentDemo/AgentDemo';
import Footer from '../../components/Footer/Footer';
import SectionDivider from '../../components/SectionDivider/SectionDivider';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <Hero />
      <ChatDemo />
      <SectionDivider variant="wave" color="#0B1220" />
      <Features />
      <SectionDivider variant="curve" flip={true} color="#0B1220" />
      <AgentDemo />
      <SectionDivider variant="tilt" flip={true} color="rgba(5, 8, 22, 0.95)" />
      <Footer />
    </div>
  );
};

export default LandingPage;
