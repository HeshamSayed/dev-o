import React from 'react';
import './SectionDivider.css';

interface SectionDividerProps {
  variant?: 'wave' | 'curve' | 'tilt';
  flip?: boolean;
  color?: string;
}

const SectionDivider: React.FC<SectionDividerProps> = ({
  variant = 'wave',
  flip = false,
  color = '#0a0a0f'
}) => {
  const renderShape = () => {
    switch (variant) {
      case 'wave':
        return (
          <svg
            viewBox="0 0 1440 120"
            preserveAspectRatio="none"
            className={`divider-svg ${flip ? 'flip' : ''}`}
          >
            <path
              d="M0,64L80,69.3C160,75,320,85,480,80C640,75,800,53,960,48C1120,43,1280,53,1360,58.7L1440,64L1440,120L0,120Z"
              fill={color}
            />
          </svg>
        );
      case 'curve':
        return (
          <svg
            viewBox="0 0 1440 120"
            preserveAspectRatio="none"
            className={`divider-svg ${flip ? 'flip' : ''}`}
          >
            <path
              d="M0,32L80,48C160,64,320,96,480,96C640,96,800,64,960,58.7C1120,53,1280,75,1360,85.3L1440,96L1440,120L0,120Z"
              fill={color}
            />
          </svg>
        );
      case 'tilt':
        return (
          <svg
            viewBox="0 0 1440 120"
            preserveAspectRatio="none"
            className={`divider-svg ${flip ? 'flip' : ''}`}
          >
            <path
              d="M0,96L80,85.3C160,75,320,53,480,42.7C640,32,800,32,960,42.7C1120,53,1280,75,1360,85.3L1440,96L1440,120L0,120Z"
              fill={color}
            />
          </svg>
        );
      default:
        return null;
    }
  };

  return (
    <div className="section-divider">
      {renderShape()}
    </div>
  );
};

export default SectionDivider;
