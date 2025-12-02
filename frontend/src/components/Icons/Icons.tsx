import React from 'react';

interface IconProps {
  className?: string;
  size?: number;
  color?: string;
}

export const RobotIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C11.45 2 11 2.45 11 3V4.18C8.24 4.6 6 7.07 6 10V16C6 16.55 6.45 17 7 17H8V20C8 21.1 8.9 22 10 22H14C15.1 22 16 21.1 16 20V17H17C17.55 17 18 16.55 18 16V10C18 7.07 15.76 4.6 13 4.18V3C13 2.45 12.55 2 12 2ZM9 10C9.55 10 10 10.45 10 11C10 11.55 9.55 12 9 12C8.45 12 8 11.55 8 11C8 10.45 8.45 10 9 10ZM15 10C15.55 10 16 10.45 16 11C16 11.55 15.55 12 15 12C14.45 12 14 11.55 14 11C14 10.45 14.45 10 15 10ZM12 14C13.1 14 14 14.45 14 15C14 15.55 13.1 16 12 16C10.9 16 10 15.55 10 15C10 14.45 10.9 14 12 14Z" fill={color} />
    <path d="M20 10C20 9.45 19.55 9 19 9C18.45 9 18 9.45 18 10V12C18 12.55 18.45 13 19 13C19.55 13 20 12.55 20 12V10Z" fill={color} />
    <path d="M4 10C4 9.45 4.45 9 5 9C5.55 9 6 9.45 6 10V12C6 12.55 5.55 13 5 13C4.45 13 4 12.55 4 12V10Z" fill={color} />
  </svg>
);

export const UserIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 12C14.21 12 16 10.21 16 8C16 5.79 14.21 4 12 4C9.79 4 8 5.79 8 8C8 10.21 9.79 12 12 12ZM12 14C9.33 14 4 15.34 4 18V20H20V18C20 15.34 14.67 14 12 14Z" fill={color} />
  </svg>
);

export const RocketIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12.5 2C11.5 2 10.5 2.3 9.7 2.9C7.5 4.5 4 8.1 4 13C4 14.3 4.3 15.5 4.9 16.5L2.1 19.3C1.7 19.7 1.7 20.3 2.1 20.7L3.3 21.9C3.7 22.3 4.3 22.3 4.7 21.9L7.5 19.1C8.5 19.7 9.7 20 11 20C15.9 20 19.5 16.5 21.1 14.3C21.7 13.5 22 12.5 22 11.5C22 6 18 2 12.5 2ZM12 9C13.1 9 14 9.9 14 11C14 12.1 13.1 13 12 13C10.9 13 10 12.1 10 11C10 9.9 10.9 9 12 9Z" fill={color} />
  </svg>
);

export const SparklesIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L13.09 8.26L19 7L15.45 11.82L20 16L13.09 14.74L12 21L10.91 14.74L4 16L8.55 11.82L5 7L10.91 8.26L12 2Z" fill={color} />
  </svg>
);

export const CodeIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M9.4 16.6L4.8 12L9.4 7.4L8 6L2 12L8 18L9.4 16.6ZM14.6 16.6L19.2 12L14.6 7.4L16 6L22 12L16 18L14.6 16.6Z" fill={color} />
  </svg>
);

export const TerminalIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 4H4C2.89 4 2 4.9 2 6V18C2 19.1 2.89 20 4 20H20C21.1 20 22 19.1 22 18V6C22 4.9 21.1 4 20 4ZM20 18H4V8H20V18ZM6 10L7.41 11.41L6 12.83L7.41 14.24L8.83 12.83L10.24 14.24L11.66 12.83L10.24 11.41L11.66 10L10.24 8.59L8.83 10L7.41 8.59L6 10ZM13 10H18V12H13V10ZM13 14H16V16H13V14Z" fill={color} />
  </svg>
);

export const DatabaseIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 3C7 3 3 4.79 3 7V17C3 19.21 7 21 12 21C17 21 21 19.21 21 17V7C21 4.79 17 3 12 3ZM12 18.5C8.13 18.5 5 17.33 5 16V14.77C6.61 15.55 9.13 16 12 16C14.87 16 17.39 15.55 19 14.77V16C19 17.33 15.87 18.5 12 18.5ZM19 12C19 13.33 15.87 14.5 12 14.5C8.13 14.5 5 13.33 5 12V10.77C6.61 11.55 9.13 12 12 12C14.87 12 17.39 11.55 19 10.77V12ZM12 10.5C8.13 10.5 5 9.33 5 8V7C5 5.67 8.13 4.5 12 4.5C15.87 4.5 19 5.67 19 7V8C19 9.33 15.87 10.5 12 10.5Z" fill={color} />
  </svg>
);

export const CloudIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M19.35 10.04C18.67 6.59 15.64 4 12 4C9.11 4 6.6 5.64 5.35 8.04C2.34 8.36 0 10.91 0 14C0 17.31 2.69 20 6 20H19C21.76 20 24 17.76 24 15C24 12.36 21.95 10.22 19.35 10.04Z" fill={color} />
  </svg>
);

export const ShieldIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 1L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 1ZM10 17L6 13L7.41 11.59L10 14.17L16.59 7.58L18 9L10 17Z" fill={color} />
  </svg>
);

export const LightningIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M7 2V13H10V22L17 10H13L17 2H7Z" fill={color} />
  </svg>
);

export const GlobeIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM11 19.93C7.05 19.44 4 16.08 4 12C4 11.38 4.08 10.79 4.21 10.21L9 15V16C9 17.1 9.9 18 11 18V19.93ZM17.9 17.39C17.64 16.58 16.9 16 16 16H15V13C15 12.45 14.55 12 14 12H8V10H10C10.55 10 11 9.55 11 9V7H13C14.1 7 15 6.1 15 5V4.59C17.93 5.78 20 8.65 20 12C20 14.08 19.2 15.97 17.9 17.39Z" fill={color} />
  </svg>
);

export const TeamIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 11C17.66 11 18.99 9.66 18.99 8C18.99 6.34 17.66 5 16 5C14.34 5 13 6.34 13 8C13 9.66 14.34 11 16 11ZM8 11C9.66 11 10.99 9.66 10.99 8C10.99 6.34 9.66 5 8 5C6.34 5 5 6.34 5 8C5 9.66 6.34 11 8 11ZM8 13C5.67 13 1 14.17 1 16.5V19H15V16.5C15 14.17 10.33 13 8 13ZM16 13C15.71 13 15.38 13.02 15.03 13.05C16.19 13.89 17 15.02 17 16.5V19H23V16.5C23 14.17 18.33 13 16 13Z" fill={color} />
  </svg>
);

export const CheckCircleIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z" fill={color} />
  </svg>
);

export const GitBranchIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M7 5C7 3.9 7.9 3 9 3C10.1 3 11 3.9 11 5C11 5.74 10.58 6.38 9.97 6.73L10 7V11.14C10.22 11.06 10.44 11 10.68 11C11.38 11 12.05 11.23 12.6 11.63L14.66 9.57C14.3 9.23 14.08 8.74 14.08 8.19C14.08 7.09 14.98 6.19 16.08 6.19C17.18 6.19 18.08 7.09 18.08 8.19C18.08 9.29 17.18 10.19 16.08 10.19C15.53 10.19 15.04 9.97 14.7 9.61L12.58 11.73C12.98 12.28 13.21 12.95 13.21 13.68C13.21 15.39 11.89 16.79 10.18 16.92V17C10.18 17 10.18 16.97 10.18 17C10.73 17.35 11.14 17.98 11.14 18.71C11.14 19.82 10.24 20.71 9.14 20.71C8.04 20.71 7.14 19.82 7.14 18.71C7.14 17.98 7.55 17.35 8.1 17V7C7.55 6.65 7.14 6.02 7.14 5.29C7.14 4.58 7.54 3.96 8.08 3.61C7.47 3.96 7 4.58 7 5Z" fill={color} />
  </svg>
);

export const BugIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 8H17.19C16.74 7.22 16.12 6.55 15.37 6.04L17 4.41L15.59 3L13.42 5.17C12.96 5.06 12.49 5 12 5C11.51 5 11.04 5.06 10.59 5.17L8.41 3L7 4.41L8.62 6.04C7.88 6.55 7.26 7.22 6.81 8H4V10H6.09C6.04 10.33 6 10.66 6 11V12H4V14H6V15C6 15.34 6.04 15.67 6.09 16H4V18H6.81C7.85 19.79 9.78 21 12 21C14.22 21 16.15 19.79 17.19 18H20V16H17.91C17.96 15.67 18 15.34 18 15V14H20V12H18V11C18 10.66 17.96 10.33 17.91 10H20V8ZM14 16H10V14H14V16ZM14 12H10V10H14V12Z" fill={color} />
  </svg>
);