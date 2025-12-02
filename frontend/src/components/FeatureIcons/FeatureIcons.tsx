import React from 'react';

interface IconProps {
  size?: number;
  className?: string;
}

// Multi-Agent Collaboration Icon
export const MultiAgentIcon: React.FC<IconProps> = ({ size = 48, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <circle cx="24" cy="14" r="6" stroke="currentColor" strokeWidth="2" fill="none"/>
    <circle cx="14" cy="30" r="5" stroke="currentColor" strokeWidth="2" fill="none"/>
    <circle cx="34" cy="30" r="5" stroke="currentColor" strokeWidth="2" fill="none"/>
    <circle cx="24" cy="38" r="4" stroke="currentColor" strokeWidth="2" fill="none"/>
    <line x1="24" y1="20" x2="24" y2="34" stroke="currentColor" strokeWidth="2"/>
    <line x1="22" y1="18" x2="16" y2="26" stroke="currentColor" strokeWidth="2"/>
    <line x1="26" y1="18" x2="32" y2="26" stroke="currentColor" strokeWidth="2"/>
  </svg>
);

// Private & Local Icon
export const PrivateLocalIcon: React.FC<IconProps> = ({ size = 48, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <path d="M24 8 L38 16 L38 28 C38 34 32 38 24 40 C16 38 10 34 10 28 L10 16 Z" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M24 18 L24 28 M24 28 L20 24 M24 28 L28 24" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="24" cy="14" r="2" fill="currentColor"/>
  </svg>
);

// Production Ready Icon
export const ProductionReadyIcon: React.FC<IconProps> = ({ size = 48, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <rect x="8" y="12" width="32" height="26" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M8 20 L40 20" stroke="currentColor" strokeWidth="2"/>
    <circle cx="13" cy="16" r="1.5" fill="currentColor"/>
    <circle cx="18" cy="16" r="1.5" fill="currentColor"/>
    <circle cx="23" cy="16" r="1.5" fill="currentColor"/>
    <path d="M16 26 L20 30 L32 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Context-Aware Memory Icon
export const ContextMemoryIcon: React.FC<IconProps> = ({ size = 48, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <circle cx="24" cy="24" r="14" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M24 10 L24 18 M24 30 L24 38 M10 24 L18 24 M30 24 L38 24" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    <circle cx="24" cy="24" r="5" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M19 19 L15 15 M29 19 L33 15 M29 29 L33 33 M19 29 L15 33" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

// Natural Language Icon
export const NaturalLanguageIcon: React.FC<IconProps> = ({ size = 48, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <path d="M12 16 L20 16 C24 16 26 18 26 22 C26 26 24 28 20 28 L12 28 L12 16 Z" stroke="currentColor" strokeWidth="2" fill="none"/>
    <path d="M12 22 L20 22" stroke="currentColor" strokeWidth="2"/>
    <path d="M30 16 L30 32 M30 24 L38 24 M38 16 L38 32" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Full Stack Icon
export const FullStackIcon: React.FC<IconProps> = ({ size = 48, className = '' }) => (
  <svg width={size} height={size} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" className={className}>
    <rect x="10" y="10" width="28" height="8" rx="1" stroke="currentColor" strokeWidth="2" fill="none"/>
    <rect x="10" y="22" width="28" height="8" rx="1" stroke="currentColor" strokeWidth="2" fill="none"/>
    <rect x="10" y="34" width="28" height="8" rx="1" stroke="currentColor" strokeWidth="2" fill="none"/>
    <circle cx="15" cy="14" r="1.5" fill="currentColor"/>
    <circle cx="20" cy="14" r="1.5" fill="currentColor"/>
    <circle cx="15" cy="26" r="1.5" fill="currentColor"/>
    <circle cx="20" cy="26" r="1.5" fill="currentColor"/>
    <circle cx="15" cy="38" r="1.5" fill="currentColor"/>
    <circle cx="20" cy="38" r="1.5" fill="currentColor"/>
  </svg>
);

export default {
  MultiAgentIcon,
  PrivateLocalIcon,
  ProductionReadyIcon,
  ContextMemoryIcon,
  NaturalLanguageIcon,
  FullStackIcon,
};
