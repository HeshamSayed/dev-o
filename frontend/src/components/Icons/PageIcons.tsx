import React from 'react';

interface IconProps {
  className?: string;
  size?: number;
  color?: string;
}

// Sparkle Icon (replaces ✨)
export const SparkleIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L13.09 8.26L18 6L15.74 10.91L22 12L15.74 13.09L18 18L13.09 15.74L12 22L10.91 15.74L6 18L8.26 13.09L2 12L8.26 10.91L6 6L10.91 8.26L12 2Z" fill={color} stroke={color} strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Lightbulb Icon (replaces 💡)
export const LightbulbIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M9 21H15M12 3C8.13 3 5 6.13 5 10C5 12.38 6.19 14.47 8 15.74V17C8 17.55 8.45 18 9 18H15C15.55 18 16 17.55 16 17V15.74C17.81 14.47 19 12.38 19 10C19 6.13 15.87 3 12 3Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M9 18V19C9 20.1 9.9 21 11 21H13C14.1 21 15 20.1 15 19V18" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Chat Bubble Icon (replaces 💬)
export const ChatBubbleIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M21 11.5C21.0034 12.8199 20.6951 14.1219 20.1 15.3C19.3944 16.7118 18.3098 17.8992 16.9674 18.7293C15.6251 19.5594 14.0782 19.9994 12.5 20C11.1801 20.0035 9.87812 19.6951 8.7 19.1L3 21L4.9 15.3C4.30493 14.1219 3.99656 12.8199 4 11.5C4.00061 9.92179 4.44061 8.37488 5.27072 7.03258C6.10083 5.69028 7.28825 4.6056 8.7 3.90003C9.87812 3.30496 11.1801 2.99659 12.5 3.00003H13C15.0843 3.11502 17.053 3.99479 18.5291 5.47089C20.0052 6.94699 20.885 8.91568 21 11V11.5Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Package Icon (replaces 📦)
export const PackageIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M16.5 9.4L7.5 4.21M21 16V8C20.9996 7.6493 20.9071 7.3048 20.7315 7.00017C20.556 6.69555 20.3037 6.44158 20 6.264L13 2.264C12.696 2.08654 12.3511 1.99341 12 1.99341C11.6489 1.99341 11.304 2.08654 11 2.264L4 6.264C3.69626 6.44158 3.44398 6.69555 3.26846 7.00017C3.09294 7.3048 3.00036 7.6493 3 8V16C3.00036 16.3507 3.09294 16.6952 3.26846 16.9998C3.44398 17.3045 3.69626 17.5584 4 17.736L11 21.736C11.304 21.9135 11.6489 22.0066 12 22.0066C12.3511 22.0066 12.696 21.9135 13 21.736L20 17.736C20.3037 17.5584 20.556 17.3045 20.7315 16.9998C20.9071 16.6952 20.9996 16.3507 21 16Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M3.27 6.96L12 12.01L20.73 6.96M12 22.08V12" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Timer Icon (replaces ⏱️)
export const TimerIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="13" r="8" stroke={color} strokeWidth="2"/>
    <path d="M12 9V13L14.5 15.5" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M9 2H15" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M12 2V4" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

// Star Icon (replaces ⭐)
export const StarIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" fill={color} stroke={color} strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Gift Icon (replaces 🎁)
export const GiftIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 12V22H4V12" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M22 7H2V12H22V7Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 22V7" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 7H7.5C6.83696 7 6.20107 6.73661 5.73223 6.26777C5.26339 5.79893 5 5.16304 5 4.5C5 3.83696 5.26339 3.20107 5.73223 2.73223C6.20107 2.26339 6.83696 2 7.5 2C11 2 12 7 12 7Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 7H16.5C17.163 7 17.7989 6.73661 18.2678 6.26777C18.7366 5.79893 19 5.16304 19 4.5C19 3.83696 18.7366 3.20107 18.2678 2.73223C17.7989 2.26339 17.163 2 16.5 2C13 2 12 7 12 7Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Rocket Icon (replaces 🚀)
export const RocketIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4.5 16.5C3 18.26 2 21 2 21S4.74 20 6.5 18.5C7.16 17.87 7.16 16.81 6.5 16.17C5.87 15.5 4.81 15.5 4.5 16.5Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 15L9 12L13.5 5.5C14.5 4 16.5 2.5 19 2C18.5 4.5 17 6.5 15.5 7.5L9 12" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M15 9L12 15M9 12L4 10C4 10 5.5 6 9 6C9 6 10 10 9 12Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M15 9C15 9 19 7.5 19 4C19 4 21 8 18 11L15 9Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Chart Up Icon (replaces 📈)
export const ChartUpIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M23 6L13.5 15.5L8.5 10.5L1 18" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M17 6H23V12" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Building Icon (replaces 🏢)
export const BuildingIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M3 21H21" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M5 21V7L13 3V21" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M19 21V11L13 7" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M9 9H9.01M9 13H9.01M9 17H9.01" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Alert Icon (replaces 🚨)
export const AlertIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 9V13M12 17H12.01" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M5.07 19H18.93C20.14 19 20.93 17.68 20.32 16.6L13.39 3.98C12.78 2.9 11.22 2.9 10.61 3.98L3.68 16.6C3.07 17.68 3.86 19 5.07 19Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Bar Chart Icon (replaces 📊)
export const BarChartIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M18 20V10" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 20V4" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M6 20V14" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Construction Icon (replaces 🏗️)
export const ConstructionIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M2 20H22" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M6 20V10L12 4L18 10V20" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 4V7" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M9 20V16H15V20" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M3 10L12 4L21 10" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Gear Icon (replaces ⚙️)
export const GearIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="3" stroke={color} strokeWidth="2"/>
    <path d="M19.4 15C19.2669 15.3016 19.2272 15.6362 19.286 15.9606C19.3448 16.285 19.4995 16.5843 19.73 16.82L19.79 16.88C19.976 17.0657 20.1235 17.2863 20.2241 17.5291C20.3248 17.7719 20.3766 18.0322 20.3766 18.295C20.3766 18.5578 20.3248 18.8181 20.2241 19.0609C20.1235 19.3037 19.976 19.5243 19.79 19.71C19.6043 19.896 19.3837 20.0435 19.1409 20.1441C18.8981 20.2448 18.6378 20.2966 18.375 20.2966C18.1122 20.2966 17.8519 20.2448 17.6091 20.1441C17.3663 20.0435 17.1457 19.896 16.96 19.71L16.9 19.65C16.6643 19.4195 16.365 19.2648 16.0406 19.206C15.7162 19.1472 15.3816 19.1869 15.08 19.32C14.7842 19.4468 14.532 19.6572 14.3543 19.9255C14.1766 20.1938 14.0813 20.5082 14.08 20.83V21C14.08 21.5304 13.8693 22.0391 13.4942 22.4142C13.1191 22.7893 12.6104 23 12.08 23C11.5496 23 11.0409 22.7893 10.6658 22.4142C10.2907 22.0391 10.08 21.5304 10.08 21V20.91C10.0723 20.579 9.96512 20.258 9.77251 19.9887C9.5799 19.7194 9.31074 19.5143 9 19.4C8.69838 19.2669 8.36381 19.2272 8.03941 19.286C7.71502 19.3448 7.41568 19.4995 7.18 19.73L7.12 19.79C6.93425 19.976 6.71368 20.1235 6.47088 20.2241C6.22808 20.3248 5.96783 20.3766 5.705 20.3766C5.44217 20.3766 5.18192 20.3248 4.93912 20.2241C4.69632 20.1235 4.47575 19.976 4.29 19.79C4.10405 19.6043 3.95653 19.3837 3.85588 19.1409C3.75523 18.8981 3.70343 18.6378 3.70343 18.375C3.70343 18.1122 3.75523 17.8519 3.85588 17.6091C3.95653 17.3663 4.10405 17.1457 4.29 16.96L4.35 16.9C4.58054 16.6643 4.73519 16.365 4.794 16.0406C4.85282 15.7162 4.81312 15.3816 4.68 15.08C4.55324 14.7842 4.34276 14.532 4.07447 14.3543C3.80618 14.1766 3.49179 14.0813 3.17 14.08H3C2.46957 14.08 1.96086 13.8693 1.58579 13.4942C1.21071 13.1191 1 12.6104 1 12.08C1 11.5496 1.21071 11.0409 1.58579 10.6658C1.96086 10.2907 2.46957 10.08 3 10.08H3.09C3.42099 10.0723 3.742 9.96512 4.0113 9.77251C4.28059 9.5799 4.48572 9.31074 4.6 9C4.73312 8.69838 4.77282 8.36381 4.714 8.03941C4.65519 7.71502 4.50054 7.41568 4.27 7.18L4.21 7.12C4.02405 6.93425 3.87653 6.71368 3.77588 6.47088C3.67523 6.22808 3.62343 5.96783 3.62343 5.705C3.62343 5.44217 3.67523 5.18192 3.77588 4.93912C3.87653 4.69632 4.02405 4.47575 4.21 4.29C4.39575 4.10405 4.61632 3.95653 4.85912 3.85588C5.10192 3.75523 5.36217 3.70343 5.625 3.70343C5.88783 3.70343 6.14808 3.75523 6.39088 3.85588C6.63368 3.95653 6.85425 4.10405 7.04 4.29L7.1 4.35C7.33568 4.58054 7.63502 4.73519 7.95941 4.794C8.28381 4.85282 8.61838 4.81312 8.92 4.68H9C9.29577 4.55324 9.54802 4.34276 9.72569 4.07447C9.90337 3.80618 9.99872 3.49179 10 3.17V3C10 2.46957 10.2107 1.96086 10.5858 1.58579C10.9609 1.21071 11.4696 1 12 1C12.5304 1 13.0391 1.21071 13.4142 1.58579C13.7893 1.96086 14 2.46957 14 3V3.09C14.0013 3.41179 14.0966 3.72618 14.2743 3.99447C14.452 4.26276 14.7042 4.47324 15 4.6C15.3016 4.73312 15.6362 4.77282 15.9606 4.714C16.285 4.65519 16.5843 4.50054 16.82 4.27L16.88 4.21C17.0657 4.02405 17.2863 3.87653 17.5291 3.77588C17.7719 3.67523 18.0322 3.62343 18.295 3.62343C18.5578 3.62343 18.8181 3.67523 19.0609 3.77588C19.3037 3.87653 19.5243 4.02405 19.71 4.21C19.896 4.39575 20.0435 4.61632 20.1441 4.85912C20.2448 5.10192 20.2966 5.36217 20.2966 5.625C20.2966 5.88783 20.2448 6.14808 20.1441 6.39088C20.0435 6.63368 19.896 6.85425 19.71 7.04L19.65 7.1C19.4195 7.33568 19.2648 7.63502 19.206 7.95941C19.1472 8.28381 19.1869 8.61838 19.32 8.92V9C19.4468 9.29577 19.6572 9.54802 19.9255 9.72569C20.1938 9.90337 20.5082 9.99872 20.83 10H21C21.5304 10 22.0391 10.2107 22.4142 10.5858C22.7893 10.9609 23 11.4696 23 12C23 12.5304 22.7893 13.0391 22.4142 13.4142C22.0391 13.7893 21.5304 14 21 14H20.91C20.5882 14.0013 20.2738 14.0966 20.0055 14.2743C19.7372 14.452 19.5268 14.7042 19.4 15Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Control Knobs Icon (replaces 🎛️)
export const ControlKnobsIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="6" cy="8" r="2" stroke={color} strokeWidth="2"/>
    <circle cx="12" cy="16" r="2" stroke={color} strokeWidth="2"/>
    <circle cx="18" cy="8" r="2" stroke={color} strokeWidth="2"/>
    <path d="M6 2V6M6 10V22M12 2V14M12 18V22M18 2V6M18 10V22" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

// Checkmark Icon (replaces ✓)
export const CheckmarkIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 6L9 17L4 12" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Lightning Icon (replaces ⚡)
export const LightningIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" fill={color} stroke={color} strokeWidth="1" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Users Icon (replaces 👥)
export const UsersIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="9" cy="7" r="4" stroke={color} strokeWidth="2"/>
    <path d="M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Globe Icon (replaces 🌍)
export const GlobeIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="10" stroke={color} strokeWidth="2"/>
    <path d="M2 12H22" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M12 2C14.5013 4.73835 15.9228 8.29203 16 12C15.9228 15.708 14.5013 19.2616 12 22C9.49872 19.2616 8.07725 15.708 8 12C8.07725 8.29203 9.49872 4.73835 12 2Z" stroke={color} strokeWidth="2"/>
  </svg>
);

// Clipboard Icon (replaces 📋)
export const ClipboardIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 4H18C18.5304 4 19.0391 4.21071 19.4142 4.58579C19.7893 4.96086 20 5.46957 20 6V20C20 20.5304 19.7893 21.0391 19.4142 21.4142C19.0391 21.7893 18.5304 22 18 22H6C5.46957 22 4.96086 21.7893 4.58579 21.4142C4.21071 21.0391 4 20.5304 4 20V6C4 5.46957 4.21071 4.96086 4.58579 4.58579C4.96086 4.21071 5.46957 4 6 4H8" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M15 2H9C8.44772 2 8 2.44772 8 3V5C8 5.55228 8.44772 6 9 6H15C15.5523 6 16 5.55228 16 5V3C16 2.44772 15.5523 2 15 2Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Handshake Icon (replaces 🤝)
export const HandshakeIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20.42 4.58C19.9183 4.07658 19.2222 3.7974 18.5 3.7974C17.7778 3.7974 17.0817 4.07658 16.58 4.58L12 9.16L7.42 4.58C6.91825 4.07658 6.22222 3.7974 5.5 3.7974C4.77778 3.7974 4.08175 4.07658 3.58 4.58C3.07658 5.08175 2.79741 5.77778 2.79741 6.5C2.79741 7.22222 3.07658 7.91825 3.58 8.42L8.16 13L3.58 17.58C3.07658 18.0817 2.79741 18.7778 2.79741 19.5C2.79741 20.2222 3.07658 20.9183 3.58 21.42C4.08175 21.9234 4.77778 22.2026 5.5 22.2026C6.22222 22.2026 6.91825 21.9234 7.42 21.42L12 16.84L16.58 21.42C17.0817 21.9234 17.7778 22.2026 18.5 22.2026C19.2222 22.2026 19.9183 21.9234 20.42 21.42C20.9234 20.9183 21.2026 20.2222 21.2026 19.5C21.2026 18.7778 20.9234 18.0817 20.42 17.58L15.84 13L20.42 8.42C20.9234 7.91825 21.2026 7.22222 21.2026 6.5C21.2026 5.77778 20.9234 5.08175 20.42 4.58Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Link Icon (replaces 🔗)
export const LinkIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M10 13C10.4295 13.5741 10.9774 14.0492 11.6066 14.3929C12.2357 14.7367 12.9315 14.9411 13.6467 14.9923C14.3618 15.0435 15.0796 14.9404 15.7513 14.6898C16.4231 14.4392 17.0331 14.0471 17.54 13.54L20.54 10.54C21.4508 9.59695 21.9548 8.33394 21.9434 7.02296C21.932 5.71198 21.4061 4.45791 20.479 3.53087C19.552 2.60383 18.2979 2.07799 16.987 2.0666C15.676 2.0552 14.413 2.55918 13.47 3.47L11.75 5.18" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M14 11C13.5705 10.4259 13.0226 9.95083 12.3934 9.60707C11.7643 9.26331 11.0685 9.05889 10.3533 9.00768C9.63816 8.95646 8.92037 9.05964 8.24861 9.31023C7.57685 9.56082 6.96684 9.95294 6.46 10.46L3.46 13.46C2.54918 14.403 2.04519 15.6661 2.05659 16.977C2.06798 18.288 2.59383 19.5421 3.52087 20.4691C4.44791 21.3962 5.70198 21.922 7.01296 21.9334C8.32394 21.9448 9.58695 21.4408 10.53 20.53L12.24 18.82" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Brain Icon (replaces 🧠)
export const BrainIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M9.5 2C10.3 2 11 2.4 11.5 3C11.8 2.4 12.5 2 13.5 2C14.9 2 16 3.1 16 4.5C16 5.2 15.7 5.8 15.3 6.2C16.3 6.5 17 7.4 17 8.5C17 9.2 16.7 9.8 16.2 10.3C17.3 10.7 18 11.7 18 13C18 14.3 17.2 15.4 16 15.8V19C16 20.1 15.1 21 14 21H10C8.9 21 8 20.1 8 19V15.8C6.8 15.4 6 14.3 6 13C6 11.7 6.7 10.7 7.8 10.3C7.3 9.8 7 9.2 7 8.5C7 7.4 7.7 6.5 8.7 6.2C8.3 5.8 8 5.2 8 4.5C8 3.1 9.1 2 10.5 2" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 6V10M12 14V18" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

// Warning Icon (replaces ⚠️)
export const WarningIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 9V13M12 17H12.01" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M10.29 3.86L1.82 18C1.64 18.3 1.55 18.65 1.55 19C1.56 19.35 1.66 19.69 1.84 19.99C2.02 20.29 2.28 20.53 2.59 20.69C2.9 20.85 3.25 20.93 3.6 20.93H20.4C20.75 20.93 21.1 20.85 21.41 20.69C21.72 20.53 21.98 20.29 22.16 19.99C22.34 19.69 22.44 19.35 22.45 19C22.45 18.65 22.36 18.3 22.18 18L13.71 3.86C13.53 3.56 13.27 3.32 12.96 3.15C12.65 2.98 12.3 2.9 11.95 2.9C11.6 2.9 11.25 2.98 10.94 3.15C10.63 3.32 10.37 3.56 10.19 3.86H10.29Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Book Icon (replaces 📚)
export const BookIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M6.5 2H20V22H6.5A2.5 2.5 0 0 1 4 19.5V4.5A2.5 2.5 0 0 1 6.5 2Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Tools Icon (replaces 🛠️)
export const ToolsIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M14.7 6.3C14.5168 6.1169 14.3 5.97011 14.0614 5.86812C13.8229 5.76612 13.5671 5.71086 13.3083 5.70554C13.0495 5.70022 12.7916 5.74495 12.5491 5.83714C12.3065 5.92933 12.084 6.06724 11.8938 6.24345C11.7035 6.41966 11.549 6.63069 11.4387 6.86476C11.3284 7.09883 11.2646 7.35137 11.2507 7.60989C11.2367 7.86841 11.2728 8.12737 11.3568 8.37212C11.4408 8.61686 11.571 8.84258 11.74 9.038L3 17.78V21H6.22L14.962 12.26C15.1574 12.429 15.3831 12.5592 15.6279 12.6432C15.8726 12.7272 16.1316 12.7633 16.3901 12.7493C16.6486 12.7354 16.9012 12.6716 17.1352 12.5613C17.3693 12.451 17.5803 12.2965 17.7566 12.1062C17.9328 11.916 18.0707 11.6935 18.1629 11.4509C18.2551 11.2084 18.2998 10.9505 18.2945 10.6917C18.2891 10.4329 18.2339 10.1771 18.1319 9.93855C18.0299 9.70003 17.8831 9.48321 17.7 9.3L14.7 6.3Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M8.5 8.5L3 3" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M21 21L15.5 15.5" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M18 12L21 15C21.5304 15.5304 21.8071 16.2609 21.7634 17.0051C21.7196 17.7493 21.3588 18.4439 20.7678 18.9142C20.1768 19.3845 19.4111 19.5876 18.6689 19.4727C17.9267 19.3577 17.2732 18.9346 16.86 18.3" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

// Shield Icon (replaces 🛡️)
export const ShieldIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 22S20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M9 12L11 14L15 10" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Microscope Icon (replaces 🔬)
export const MicroscopeIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M6 18H8" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M3 22H21" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M14 22V11C14 10.4696 13.7893 9.96086 13.4142 9.58579C13.0391 9.21071 12.5304 9 12 9C11.4696 9 10.9609 9.21071 10.5858 9.58579C10.2107 9.96086 10 10.4696 10 11V18C10 19.0609 9.57857 20.0783 8.82843 20.8284C8.07828 21.5786 7.06087 22 6 22" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <circle cx="12" cy="5" r="3" stroke={color} strokeWidth="2"/>
  </svg>
);

// Memo Icon (replaces 📝)
export const MemoIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M14 2V8H20M16 13H8M16 17H8M10 9H8" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Microphone Icon (replaces 🎤)
export const MicrophoneIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2C11.2044 2 10.4413 2.31607 9.87868 2.87868C9.31607 3.44129 9 4.20435 9 5V12C9 12.7956 9.31607 13.5587 9.87868 14.1213C10.4413 14.6839 11.2044 15 12 15C12.7956 15 13.5587 14.6839 14.1213 14.1213C14.6839 13.5587 15 12.7956 15 12V5C15 4.20435 14.6839 3.44129 14.1213 2.87868C13.5587 2.31607 12.7956 2 12 2Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M19 10V12C19 13.8565 18.2625 15.637 16.9497 16.9497C15.637 18.2625 13.8565 19 12 19C10.1435 19 8.36301 18.2625 7.05025 16.9497C5.7375 15.637 5 13.8565 5 12V10" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 19V23M8 23H16" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Suit Icon (replaces 👔)
export const SuitIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2L8 6V8L12 6L16 8V6L12 2Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M8 6L4 8V22H20V8L16 6" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M12 6V22" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M10 10H8M16 10H14M10 14H8M16 14H14" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

// Wrench Icon (replaces 🔧)
export const WrenchIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M14.7 6.3C14.3 5.9 13.8 5.6 13.3 5.4C12.8 5.2 12.2 5.1 11.7 5.1C10.4 5.1 9.2 5.6 8.3 6.5C7.4 7.4 6.9 8.6 6.9 9.9C6.9 10.4 7 10.9 7.2 11.4C7.4 11.9 7.7 12.4 8.1 12.8L2 18.9V22H5.1L11.2 15.9C11.6 16.3 12.1 16.6 12.6 16.8C13.1 17 13.6 17.1 14.1 17.1C15.4 17.1 16.6 16.6 17.5 15.7C18.4 14.8 18.9 13.6 18.9 12.3C18.9 11.8 18.8 11.3 18.6 10.8C18.4 10.3 18.1 9.8 17.7 9.4L14.7 6.3Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Laptop Icon (replaces 💻)
export const LaptopIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 16V6C20 5.46957 19.7893 4.96086 19.4142 4.58579C19.0391 4.21071 18.5304 4 18 4H6C5.46957 4 4.96086 4.21071 4.58579 4.58579C4.21071 4.96086 4 5.46957 4 6V16" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M2 18C2 18.5304 2.21071 19.0391 2.58579 19.4142C2.96086 19.7893 3.46957 20 4 20H20C20.5304 20 21.0391 19.7893 21.4142 19.4142C21.7893 19.0391 22 18.5304 22 18V17H2V18Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Tag Icon (replaces 🏷️)
export const TagIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20.59 13.41L13.42 20.58C13.2343 20.766 13.0137 20.9135 12.7709 21.0141C12.5281 21.1148 12.2678 21.1666 12.005 21.1666C11.7422 21.1666 11.4819 21.1148 11.2391 21.0141C10.9963 20.9135 10.7757 20.766 10.59 20.58L2 12V2H12L20.59 10.59C20.9625 10.9647 21.1716 11.4716 21.1716 12C21.1716 12.5284 20.9625 13.0353 20.59 13.41Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M7 7H7.01" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Email Icon (replaces 📧)
export const EmailIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 4H20C21.1 4 22 4.9 22 6V18C22 19.1 21.1 20 20 20H4C2.9 20 2 19.1 2 18V6C2 4.9 2.9 4 4 4Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M22 6L12 13L2 6" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Folder Icon (replaces 📁)
export const FolderIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M22 19C22 19.5304 21.7893 20.0391 21.4142 20.4142C21.0391 20.7893 20.5304 21 20 21H4C3.46957 21 2.96086 20.7893 2.58579 20.4142C2.21071 20.0391 2 19.5304 2 19V5C2 4.46957 2.21071 3.96086 2.58579 3.58579C2.96086 3.21071 3.46957 3 4 3H9L11 6H20C20.5304 6 21.0391 6.21071 21.4142 6.58579C21.7893 6.96086 22 7.46957 22 8V19Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// File Icon (replaces 📄)
export const FileIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M14 2V8H20" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Status Dot Connected (replaces 🟢)
export const StatusConnectedIcon: React.FC<IconProps> = ({ className, size = 24, color = '#10B981' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="8" fill={color}/>
    <circle cx="12" cy="12" r="10" stroke={color} strokeWidth="2" strokeOpacity="0.3"/>
  </svg>
);

// Status Dot Disconnected (replaces 🔴)
export const StatusDisconnectedIcon: React.FC<IconProps> = ({ className, size = 24, color = '#EF4444' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="8" fill={color}/>
    <circle cx="12" cy="12" r="10" stroke={color} strokeWidth="2" strokeOpacity="0.3"/>
  </svg>
);

// Check Circle Icon (replaces ✅)
export const CheckCircleIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="10" stroke={color} strokeWidth="2"/>
    <path d="M9 12L11 14L15 10" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Refresh Icon (replaces 🔄)
export const RefreshIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M23 4V10H17" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M1 20V14H7" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M3.51 9C4.01717 7.56678 4.87913 6.28523 6.01547 5.27207C7.15182 4.2589 8.52547 3.5488 10.0083 3.20755C11.4911 2.8663 13.0348 2.90473 14.4994 3.31949C15.964 3.73424 17.3023 4.51197 18.39 5.58L23 10M1 14L5.61 18.42C6.69766 19.488 8.03597 20.2658 9.50061 20.6805C10.9652 21.0953 12.5089 21.1337 13.9917 20.7924C15.4745 20.4512 16.8482 19.7411 17.9845 18.7279C19.1209 17.7148 19.9828 16.4332 20.49 15" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Cross Icon (replaces ❌)
export const CrossIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="10" stroke={color} strokeWidth="2"/>
    <path d="M15 9L9 15M9 9L15 15" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Party Icon (replaces 🎉)
export const PartyIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M5.8 13.4L11.6 19.2C12 19.6 12.6 19.6 13 19.2L19.2 13C19.6 12.6 19.6 12 19.2 11.6L13.4 5.8C13 5.4 12.4 5.4 12 5.8L5.8 12C5.4 12.4 5.4 13 5.8 13.4Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M3 3L7 7M21 3L17 7M3 21L7 17M14 3V5M21 10H19M10 21V19M3 14H5" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

// Hourglass Icon (replaces ⏳)
export const HourglassIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M6 2H18" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M6 22H18" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M6 2V8L12 12L18 8V2" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M6 22V16L12 12L18 16V22" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Briefcase Icon (replaces 💼)
export const BriefcaseIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20 7H4C2.89543 7 2 7.89543 2 9V19C2 20.1046 2.89543 21 4 21H20C21.1046 21 22 20.1046 22 19V9C22 7.89543 21.1046 7 20 7Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M16 21V5C16 4.46957 15.7893 3.96086 15.4142 3.58579C15.0391 3.21071 14.5304 3 14 3H10C9.46957 3 8.96086 3.21071 8.58579 3.58579C8.21071 3.96086 8 4.46957 8 5V21" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Wave Icon (replaces 👋)
export const WaveIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M18.5 9.5L19 9C20.1046 7.89543 20.1046 6.10457 19 5C17.8954 3.89543 16.1046 3.89543 15 5L14.5 5.5" stroke={color} strokeWidth="2" strokeLinecap="round"/>
    <path d="M14.5 5.5L12 8L9.5 5.5L10 5C11.1046 3.89543 11.1046 2.10457 10 1C8.89543 -0.104569 7.10457 -0.104569 6 1L5.5 1.5L2.5 4.5C0.5 6.5 0.5 9.5 2.5 11.5L7 16L12.5 21.5C14.5 23.5 17.5 23.5 19.5 21.5L21.5 19.5C23.5 17.5 23.5 14.5 21.5 12.5L18.5 9.5Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Book Open Icon (replaces 📖)
export const BookOpenIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M2 3H8C9.06087 3 10.0783 3.42143 10.8284 4.17157C11.5786 4.92172 12 5.93913 12 7V21C12 20.2044 11.6839 19.4413 11.1213 18.8787C10.5587 18.3161 9.79565 18 9 18H2V3Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M22 3H16C14.9391 3 13.9217 3.42143 13.1716 4.17157C12.4214 4.92172 12 5.93913 12 7V21C12 20.2044 12.3161 19.4413 12.8787 18.8787C13.4413 18.3161 14.2044 18 15 18H22V3Z" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

// Working Gear Icon (spinning state indicator)
export const WorkingGearIcon: React.FC<IconProps> = ({ className, size = 24, color = 'currentColor' }) => (
  <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="12" cy="12" r="3" stroke={color} strokeWidth="2"/>
    <path d="M12 1V4M12 20V23M4.22 4.22L6.34 6.34M17.66 17.66L19.78 19.78M1 12H4M20 12H23M4.22 19.78L6.34 17.66M17.66 6.34L19.78 4.22" stroke={color} strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

export default {
  SparkleIcon,
  LightbulbIcon,
  ChatBubbleIcon,
  PackageIcon,
  TimerIcon,
  StarIcon,
  GiftIcon,
  RocketIcon,
  ChartUpIcon,
  BuildingIcon,
  AlertIcon,
  BarChartIcon,
  ConstructionIcon,
  GearIcon,
  ControlKnobsIcon,
  CheckmarkIcon,
  LightningIcon,
  UsersIcon,
  GlobeIcon,
  ClipboardIcon,
  HandshakeIcon,
  LinkIcon,
  BrainIcon,
  WarningIcon,
  BookIcon,
  ToolsIcon,
  ShieldIcon,
  MicroscopeIcon,
  MemoIcon,
  MicrophoneIcon,
  SuitIcon,
  WrenchIcon,
  LaptopIcon,
  TagIcon,
  EmailIcon,
  FolderIcon,
  FileIcon,
  StatusConnectedIcon,
  StatusDisconnectedIcon,
  CheckCircleIcon,
  RefreshIcon,
  CrossIcon,
  PartyIcon,
  HourglassIcon,
  BriefcaseIcon,
  WaveIcon,
  BookOpenIcon,
  WorkingGearIcon,
};
