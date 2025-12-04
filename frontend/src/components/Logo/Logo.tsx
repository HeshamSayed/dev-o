import React from 'react';
import logoImage from './DEV-O_Logo.png';
import './Logo.css';

interface LogoProps {
  size?: number;
  showText?: boolean;
}

const Logo: React.FC<LogoProps> = ({ size = 120, showText = true }) => {
  return (
    <div className="dev-o-logo" style={{ width: size }}>
      <img 
        src={logoImage} 
        alt="DEV-O Logo" 
        className="logo-image"
        style={{ width: size, height: 'auto' }}
      />

      {showText && (
        <div className="logo-text">
          <span className="logo-text-sub">Your Vision. AI Precision.</span>
        </div>
      )}
    </div>
  );
};

export default Logo;
