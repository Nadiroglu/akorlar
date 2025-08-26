# Akorlar - Turkish Music App

A modern React application for discovering Turkish music, songs, and chords with an engaging user interface and smooth animations.

## 🏗️ Project Structure

```
src/
├── api/                    # API layer for data fetching
│   ├── songs.js           # Song-related API calls
│   ├── chords.js          # Chord-related API calls
│   └── ads.js             # Advertisement API calls
├── assets/                 # Static files
│   ├── images/            # Image files
│   ├── icons/             # Icon files
│   └── fonts/             # Font files
├── components/             # Reusable UI components
│   ├── Buttons/           # Button components
│   ├── Loaders/           # Loading states
│   ├── Ads/               # Advertisement components
│   └── Layout/            # Layout components
├── features/               # Feature-specific components
│   ├── Hero/              # Hero section components
│   ├── Marquee/           # Scrolling banner components
│   ├── Songs/             # Song-related components
│   └── Chords/            # Chord-related components
├── hooks/                  # Custom React hooks
│   └── useSongs.js        # Song data management
├── pages/                  # Page components
│   ├── Home.jsx           # Homepage
│   ├── SongPage.jsx       # Individual song page
│   ├── ChordPage.jsx      # Chord details page
│   ├── SearchPage.jsx     # Search results page
│   ├── GenrePage.jsx      # Genre-specific page
│   └── NotFound.jsx       # 404 error page
├── routes/                 # Routing configuration
│   └── AppRoutes.jsx      # Main routing setup
├── styles/                 # Global styles and CSS
├── utils/                  # Utility functions
│   └── constants.js       # App constants and config
├── App.jsx                 # Main app component
├── main.jsx               # App entry point
└── index.css              # Global CSS
```

## 🚀 Features

- **Animated Hero Section**: Pink overlay reveal with staggered letter animations
- **Dynamic Search**: Real-time search with debouncing and suggestions
- **Smooth Marquee**: Scrolling banner for popular genres
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Performance Optimized**: 60fps animations with hardware acceleration
- **Google Ads Integration**: Responsive ad slots with fallback content
- **Modern Routing**: React Router v6 with nested routes

## 🛠️ Development

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation
```bash
npm install
```

### Development Server
```bash
npm run dev
```

### Build
```bash
npm run build
```

### Preview Build
```bash
npm run preview
```

## 🎨 Design System

### Colors
- **Primary**: Pink (#EC4899)
- **Secondary**: Violet (#8B5CF6)
- **Success**: Emerald (#10B981)
- **Warning**: Amber (#F59E0B)
- **Error**: Red (#EF4444)

### Typography
- **Primary Font**: Inter (system-ui fallback)
- **Secondary Font**: Georgia (serif)
- **Monospace**: JetBrains Mono

### Breakpoints
- **SM**: 640px
- **MD**: 768px
- **LG**: 1024px
- **XL**: 1280px
- **2XL**: 1536px

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the client directory:

```env
VITE_API_URL=http://localhost:8000/api
```

### API Configuration
The app is configured to work with a Django backend API. Update the API base URL in `src/utils/constants.js` or via environment variables.

## 📱 Responsive Design

The application is built with a mobile-first approach using Tailwind CSS. All components are designed to work seamlessly across different screen sizes.

## 🎭 Animation System

- **Hero Reveal**: 2-second stepped block animation
- **Letter Fly-In**: Randomized bird-like entrance for title text
- **Ninja Strike**: Swift search bar entrance with bounce effect
- **Marquee**: Smooth 30-second scrolling animation
- **Performance**: Hardware-accelerated transforms for 60fps

## 🎵 Music Features

- **Song Discovery**: Browse by genre, artist, or search
- **Chord Display**: Interactive chord diagrams and progressions
- **Multiple Keys**: Transpose songs to different musical keys
- **Difficulty Levels**: Beginner, intermediate, and advanced arrangements
- **Instrument Support**: Guitar, piano, ukulele, bass, and more

## 📊 Advertisement Integration

- **Google Ads**: Responsive ad slots with proper configuration
- **Fallback Content**: Graceful degradation when ads are unavailable
- **Performance Tracking**: Impression and click tracking
- **Refresh Timing**: Configurable ad refresh intervals

## 🧪 Testing

```bash
npm run test
```

## 📦 Build & Deployment

The application builds to the `dist/` directory and can be deployed to any static hosting service like:

- Vercel
- Netlify
- GitHub Pages
- AWS S3
- Firebase Hosting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support, email support@akorlar.com or create an issue in the repository.
