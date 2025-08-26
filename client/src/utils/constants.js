// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  TIMEOUT: 10000, // 10 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
}

// App Configuration
export const APP_CONFIG = {
  NAME: 'Akorlar',
  VERSION: '1.0.0',
  DESCRIPTION: 'Turkish Music – Discover Songs & Chords',
  AUTHOR: 'Akorlar Team',
  SUPPORT_EMAIL: 'support@akorlar.com',
}

// Music Constants
export const MUSIC_CONSTANTS = {
  KEYS: ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
  DIFFICULTY_LEVELS: ['beginner', 'intermediate', 'advanced'],
  GENRES: [
    'Pop', 'Rock', 'Folk', 'Jazz', 'Classical', 
    'Electronic', 'Hip Hop', 'R&B', 'Country', 'Blues',
    'Reggae', 'Metal', 'Punk', 'Indie', 'Alternative'
  ],
  INSTRUMENTS: ['guitar', 'piano', 'ukulele', 'bass', 'drums', 'violin'],
  TUNINGS: {
    guitar: ['E', 'A', 'D', 'G', 'B', 'E'],
    ukulele: ['G', 'C', 'E', 'A'],
    bass: ['E', 'A', 'D', 'G']
  }
}

// UI Constants
export const UI_CONSTANTS = {
  BREAKPOINTS: {
    SM: 640,
    MD: 768,
    LG: 1024,
    XL: 1280,
    '2XL': 1536
  },
  ANIMATION_DURATIONS: {
    FAST: 150,
    NORMAL: 300,
    SLOW: 500,
    VERY_SLOW: 1000
  },
  Z_INDEX: {
    DROPDOWN: 1000,
    STICKY: 1020,
    FIXED: 1030,
    MODAL_BACKDROP: 1040,
    MODAL: 1050,
    POPOVER: 1060,
    TOOLTIP: 1070
  }
}

// Ad Configuration
export const AD_CONFIG = {
  REFRESH_INTERVALS: {
    HERO: 30000, // 30 seconds
    SIDEBAR: 60000, // 1 minute
    FOOTER: 120000, // 2 minutes
  },
  SLOTS: {
    HERO: 'hero-ad-slot',
    SIDEBAR: 'sidebar-ad-slot',
    FOOTER: 'footer-ad-slot',
    INLINE: 'inline-ad-slot'
  },
  SIZES: {
    BANNER: [728, 90],
    SKYSCRAPER: [160, 600],
    MEDIUM_RECTANGLE: [300, 250],
    LARGE_RECTANGLE: [336, 280],
    LEADERBOARD: [970, 90]
  }
}

// Search Configuration
export const SEARCH_CONFIG = {
  MIN_QUERY_LENGTH: 2,
  MAX_SUGGESTIONS: 10,
  DEBOUNCE_DELAY: 300, // milliseconds
  RECENT_SEARCHES_LIMIT: 10,
  POPULAR_SEARCHES: [
    'Sezen Aksu',
    'Tarkan',
    'Barış Manço',
    'Ajda Pekkan',
    'Ferdi Tayfur'
  ]
}

// Pagination Configuration
export const PAGINATION_CONFIG = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
  MAX_VISIBLE_PAGES: 5
}

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  SERVER_ERROR: 'Server error. Please try again later.',
  NOT_FOUND: 'The requested resource was not found.',
  UNAUTHORIZED: 'You are not authorized to access this resource.',
  FORBIDDEN: 'Access to this resource is forbidden.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  GENERIC_ERROR: 'Something went wrong. Please try again.'
}

// Success Messages
export const SUCCESS_MESSAGES = {
  SONG_SAVED: 'Song saved to your favorites!',
  CHORD_LOADED: 'Chords loaded successfully!',
  SEARCH_COMPLETED: 'Search completed successfully!',
  PROFILE_UPDATED: 'Profile updated successfully!',
  SETTINGS_SAVED: 'Settings saved successfully!'
}

// Local Storage Keys
export const STORAGE_KEYS = {
  USER_PREFERENCES: 'akorlar_user_preferences',
  RECENT_SEARCHES: 'akorlar_recent_searches',
  FAVORITE_SONGS: 'akorlar_favorite_songs',
  THEME_PREFERENCE: 'akorlar_theme_preference',
  LANGUAGE_PREFERENCE: 'akorlar_language_preference'
}

// Theme Configuration
export const THEME_CONFIG = {
  COLORS: {
    PRIMARY: '#EC4899', // pink-500
    SECONDARY: '#8B5CF6', // violet-500
    SUCCESS: '#10B981', // emerald-500
    WARNING: '#F59E0B', // amber-500
    ERROR: '#EF4444', // red-500
    INFO: '#3B82F6', // blue-500
  },
  FONTS: {
    PRIMARY: 'Inter, system-ui, sans-serif',
    SECONDARY: 'Georgia, serif',
    MONOSPACE: 'JetBrains Mono, monospace'
  }
}
