import React from 'react';
import logoImage from './logo+icon.png';
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

      
    </div>
  );
};

export default Logo;
