// DEV-O Brand Identity Design System
export const theme = {
  colors: {
    // Brand / Primary Colors
    primary: {
      900: '#050816',
      700: '#0B1220',
      500: '#2563EB',
      300: '#60A5FA',
      // Gradients
      gradient: 'linear-gradient(135deg, #2563EB 0%, #60A5FA 100%)',
    },
    // Accent Colors
    accent: {
      cyberTeal: '#06B6D4',
      signalPurple: '#A855F7',
      // Gradients
      tealGradient: 'linear-gradient(135deg, #06B6D4 0%, #2563EB 100%)',
      purpleGradient: 'linear-gradient(135deg, #A855F7 0%, #2563EB 100%)',
      mixedGradient: 'linear-gradient(135deg, #06B6D4 0%, #A855F7 100%)',
    },
    // Status Colors
    status: {
      success: '#22C55E',
      warning: '#F97316',
      error: '#EF4444',
    },
    // Neutral / Typography
    background: {
      dark: '#020617',
      surface: '#0F172A',
      card: 'rgba(15, 23, 42, 0.6)',
      cardHover: 'rgba(15, 23, 42, 0.8)',
    },
    text: {
      primary: '#F9FAFB',
      secondary: '#9CA3AF',
      muted: '#6B7280',
    },
    border: {
      divider: '#1E293B',
      subtle: 'rgba(30, 41, 59, 0.5)',
    },
    // Special Gradients for UI
    gradient: {
      primary: 'linear-gradient(135deg, #2563EB 0%, #60A5FA 100%)',
      accent: 'linear-gradient(135deg, #06B6D4 0%, #A855F7 100%)',
      hero: 'linear-gradient(180deg, #020617 0%, #0B1220 100%)',
      card: 'linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%)',
    },
  },
  spacing: {
    xs: '0.5rem',
    sm: '1rem',
    md: '1.5rem',
    lg: '2rem',
    xl: '3rem',
    xxl: '4rem',
  },
  borderRadius: {
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    full: '9999px',
  },
  fontSize: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
    '3xl': '1.875rem',
    '4xl': '2.25rem',
    '5xl': '3rem',
    '6xl': '3.75rem',
  },
  animation: {
    glow: 'glow-scale 4s ease-in-out infinite',
    float: 'float 6s ease-in-out infinite',
    cursor: 'cursor-move 8s ease-in-out infinite',
  },
  shadows: {
    glow: '0 0 150px rgba(37, 99, 235, 0.3)',
    glowTeal: '0 0 150px rgba(6, 182, 212, 0.3)',
    glowPurple: '0 0 150px rgba(168, 85, 247, 0.3)',
    card: '0 8px 32px rgba(2, 6, 23, 0.4)',
  },
} as const;

export type Theme = typeof theme;
