import React from 'react';

interface IconProps {
  className?: string;
  size?: number;
  color?: string;
}

// Unique Brain Network Icon for AI
export const BrainNetworkIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C13.1 2 14 2.9 14 4C14 4.4 13.9 4.8 13.7 5.1L16.3 7.7C16.6 7.5 17 7.4 17.4 7.4C18.5 7.4 19.4 8.3 19.4 9.4C19.4 10.5 18.5 11.4 17.4 11.4C17 11.4 16.6 11.3 16.3 11.1L13.7 13.7C13.9 14 14 14.4 14 14.8C14 15.9 13.1 16.8 12 16.8C10.9 16.8 10 15.9 10 14.8C10 14.4 10.1 14 10.3 13.7L7.7 11.1C7.4 11.3 7 11.4 6.6 11.4C5.5 11.4 4.6 10.5 4.6 9.4C4.6 8.3 5.5 7.4 6.6 7.4C7 7.4 7.4 7.5 7.7 7.7L10.3 5.1C10.1 4.8 10 4.4 10 4C10 2.9 10.9 2 12 2Z" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 16.8V22M6.6 11.4L3 15M17.4 11.4L21 15" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="12" cy="4" r="1.5" fill={color}/>
    <circle cx="6.6" cy="9.4" r="1.5" fill={color}/>
    <circle cx="17.4" cy="9.4" r="1.5" fill={color}/>
    <circle cx="12" cy="14.8" r="1.5" fill={color}/>
  </svg>
);

// Unique Hexagon Stack for Architecture
export const HexagonStackIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L19 6.5V11.5L12 16L5 11.5V6.5L12 2Z" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 8L16 10.5V13.5L12 16L8 13.5V10.5L12 8Z" fill={color} fillOpacity="0.2" stroke={color} strokeWidth="1.5"/>
    <path d="M12 16V22M5 11.5L2 13.5M19 11.5L22 13.5" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Unique Crystal for Speed
export const CrystalIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L16 7L20 12L16 17L12 22L8 17L4 12L8 7L12 2Z" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 2L12 22M4 12L20 12M8 7L16 17M16 7L8 17" stroke={color} strokeWidth="1" strokeOpacity="0.3"/>
    <circle cx="12" cy="12" r="3" fill={color} fillOpacity="0.2" stroke={color} strokeWidth="1.5"/>
  </svg>
);

// Unique Infinity Loop for Continuous Integration
export const InfinityLoopIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M5.5 12C5.5 10 3.5 8 1.5 10C-0.5 12 -0.5 12 1.5 14C3.5 16 5.5 14 5.5 12ZM5.5 12C5.5 12 7 10 9 10C11 10 12 12 12 12C12 12 13 10 15 10C17 10 18.5 12 18.5 12C18.5 10 20.5 8 22.5 10C24.5 12 24.5 12 22.5 14C20.5 16 18.5 14 18.5 12" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="6" cy="12" r="2" fill={color} fillOpacity="0.3"/>
    <circle cx="18" cy="12" r="2" fill={color} fillOpacity="0.3"/>
  </svg>
);

// Unique Cube Matrix for Memory/Database
export const CubeMatrixIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L20 7V17L12 22L4 17V7L12 2Z" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 2V8M12 8L4 13M12 8L20 13M12 8V14M12 14L4 19M12 14L20 19M12 14V22" stroke={color} strokeWidth="1" strokeOpacity="0.5"/>
    <circle cx="12" cy="8" r="1.5" fill={color}/>
    <circle cx="12" cy="14" r="1.5" fill={color}/>
    <circle cx="8" cy="11" r="1" fill={color} fillOpacity="0.5"/>
    <circle cx="16" cy="11" r="1" fill={color} fillOpacity="0.5"/>
  </svg>
);

// Unique Diamond Circuit for Code Quality
export const DiamondCircuitIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L18 8L12 14L6 8L12 2Z" fill={color} fillOpacity="0.2" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 10L18 16L12 22L6 16L12 10Z" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 2V10M12 14V22M6 8H2M22 8H18M6 16H2M22 16H18" stroke={color} strokeWidth="1" strokeOpacity="0.5"/>
    <circle cx="12" cy="6" r="1" fill={color}/>
    <circle cx="12" cy="18" r="1" fill={color}/>
  </svg>
);

// Unique Orbital Rings for Cloud
export const OrbitalRingsIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="12" cy="12" rx="10" ry="4" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
    <ellipse cx="12" cy="12" rx="4" ry="10" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
    <ellipse cx="12" cy="12" rx="8" ry="8" transform="rotate(45 12 12)" stroke={color} strokeWidth="1" strokeOpacity="0.5"/>
    <circle cx="12" cy="12" r="3" fill={color} fillOpacity="0.2" stroke={color} strokeWidth="1.5"/>
    <circle cx="12" cy="12" r="1" fill={color}/>
  </svg>
);

// Unique Shield Lock for Security
export const ShieldLockIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L4 6V12C4 16.5 7 20.3 12 21C17 20.3 20 16.5 20 12V6L12 2Z" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 7V11M12 11C11 11 10 12 10 13V15C10 16 11 17 12 17C13 17 14 16 14 15V13C14 12 13 11 12 11Z" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="12" cy="13" r="0.5" fill={color}/>
  </svg>
);

// Unique Pulse Wave for Real-time
export const PulseWaveIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M2 12H7L9 6L12 18L15 8L17 14H22" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="9" cy="6" r="1.5" fill={color}/>
    <circle cx="12" cy="18" r="1.5" fill={color}/>
    <circle cx="15" cy="8" r="1.5" fill={color}/>
  </svg>
);

// Unique Pyramid for Hierarchy
export const PyramidIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L22 20H2L12 2Z" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 2L12 20M2 20L17 8M22 20L7 8" stroke={color} strokeWidth="1" strokeOpacity="0.3"/>
    <path d="M12 8L16 14H8L12 8Z" fill={color} fillOpacity="0.2" stroke={color} strokeWidth="1"/>
  </svg>
);

// Unique Star Burst for Features
export const StarBurstIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L13.5 8.5L20 7L15.5 11.5L21 16L14 14.5L12 22L10 14.5L3 16L8.5 11.5L4 7L10.5 8.5L12 2Z" fill={color} fillOpacity="0.1" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="12" cy="12" r="3" fill={color} fillOpacity="0.3" stroke={color} strokeWidth="1.5"/>
  </svg>
);

// Unique Flow Arrows for Process
export const FlowArrowsIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 7H15L12 4M21 17H9L12 20" stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M15 7C15 7 18 7 18 10V14C18 17 15 17 15 17" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
    <path d="M9 17C9 17 6 17 6 14V10C6 7 9 7 9 7" stroke={color} strokeWidth="1.5" strokeLinecap="round"/>
    <circle cx="3" cy="7" r="2" fill={color} fillOpacity="0.2" stroke={color} strokeWidth="1.5"/>
    <circle cx="21" cy="17" r="2" fill={color} fillOpacity="0.2" stroke={color} strokeWidth="1.5"/>
  </svg>
);