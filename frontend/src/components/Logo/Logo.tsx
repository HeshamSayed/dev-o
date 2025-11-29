import React from 'react';
import './Logo.css';

interface LogoProps {
  size?: number;
  showText?: boolean;
}

const Logo: React.FC<LogoProps> = ({ size = 120, showText = true }) => {
  return (
    <div className="dev-o-logo" style={{ width: size }}>
      <svg
        viewBox="0 0 220 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="logo-svg"
      >
        {/* D */}
        <text
          x="5"
          y="65"
          fontSize="56"
          fontWeight="700"
          fill="url(#textGradient)"
          className="logo-letter"
          letterSpacing="-2"
        >
          D
        </text>

        {/* E */}
        <text
          x="45"
          y="65"
          fontSize="56"
          fontWeight="700"
          fill="url(#textGradient)"
          className="logo-letter"
          letterSpacing="-2"
        >
          E
        </text>

        {/* V */}
        <text
          x="80"
          y="65"
          fontSize="56"
          fontWeight="700"
          fill="url(#textGradient)"
          className="logo-letter"
          letterSpacing="-2"
        >
          V
        </text>

        {/* DASH - */}
        <rect
          x="120"
          y="43"
          width="16"
          height="6"
          fill="url(#textGradient)"
          rx="3"
          className="logo-dash"
        />

        {/* O with AI neural network */}
        <g className="letter-o-group">
          {/* Main O */}
          <circle
            cx="170"
            cy="46"
            r="24"
            stroke="url(#textGradient)"
            strokeWidth="7"
            fill="none"
            className="o-outer"
          />

          {/* Inner AI core */}
          <circle
            cx="170"
            cy="46"
            r="13"
            fill="url(#coreGradient)"
            className="o-inner"
          />

          {/* Center dot */}
          <circle
            cx="170"
            cy="46"
            r="3"
            fill="#ffffff"
            className="o-center"
          />

          {/* Neural nodes - 8 points */}
          <circle cx="170" cy="30" r="1.8" fill="#60A5FA" className="neural-node n1" />
          <circle cx="181" cy="35" r="1.8" fill="#8B5CF6" className="neural-node n2" />
          <circle cx="186" cy="46" r="1.8" fill="#06B6D4" className="neural-node n3" />
          <circle cx="181" cy="57" r="1.8" fill="#60A5FA" className="neural-node n4" />
          <circle cx="170" cy="62" r="1.8" fill="#8B5CF6" className="neural-node n5" />
          <circle cx="159" cy="57" r="1.8" fill="#06B6D4" className="neural-node n6" />
          <circle cx="154" cy="46" r="1.8" fill="#60A5FA" className="neural-node n7" />
          <circle cx="159" cy="35" r="1.8" fill="#8B5CF6" className="neural-node n8" />

          {/* Connection lines */}
          <line x1="170" y1="30" x2="170" y2="41" stroke="#60A5FA" strokeWidth="0.6" opacity="0.3" className="neural-link" />
          <line x1="181" y1="35" x2="174" y2="41" stroke="#8B5CF6" strokeWidth="0.6" opacity="0.3" className="neural-link" />
          <line x1="186" y1="46" x2="174" y2="46" stroke="#06B6D4" strokeWidth="0.6" opacity="0.3" className="neural-link" />
          <line x1="181" y1="57" x2="174" y2="51" stroke="#60A5FA" strokeWidth="0.6" opacity="0.3" className="neural-link" />
          <line x1="170" y1="62" x2="170" y2="51" stroke="#8B5CF6" strokeWidth="0.6" opacity="0.3" className="neural-link" />
          <line x1="159" y1="57" x2="166" y2="51" stroke="#06B6D4" strokeWidth="0.6" opacity="0.3" className="neural-link" />
          <line x1="154" y1="46" x2="166" y2="46" stroke="#60A5FA" strokeWidth="0.6" opacity="0.3" className="neural-link" />
          <line x1="159" y1="35" x2="166" y2="41" stroke="#8B5CF6" strokeWidth="0.6" opacity="0.3" className="neural-link" />
        </g>

        {/* Gradients */}
        <defs>
          <linearGradient id="textGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#60A5FA" />
            <stop offset="50%" stopColor="#8B5CF6" />
            <stop offset="100%" stopColor="#06B6D4" />
          </linearGradient>

          <linearGradient id="coreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3B82F6" />
            <stop offset="50%" stopColor="#7C3AED" />
            <stop offset="100%" stopColor="#0891B2" />
          </linearGradient>

          {/* Glow Filter */}
          <filter id="textGlow">
            <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
      </svg>

      {showText && (
        <div className="logo-text">
          <span className="logo-text-main gradient-text">DEV-O</span>
          <span className="logo-text-sub">Your Vision. AI Precision.</span>
        </div>
      )}
    </div>
  );
};

export default Logo;
