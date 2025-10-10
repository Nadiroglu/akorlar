import React, { useState, useEffect, useRef, useMemo, useCallback } from 'react'
import SearchBar from '../components/SearchBar'
import Marquee from '../components/Marquee'

const Home = () => {
  const [songs, setSongs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [animationPhase, setAnimationPhase] = useState('masked')
  const [lettersVisible, setLettersVisible] = useState(false)
  const [searchVisible, setSearchVisible] = useState(false)
  const [marqueeVisible, setMarqueeVisible] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [showRecommendButton, setShowRecommendButton] = useState(false)
  
  const canvasRef = useRef(null)
  const animationRef = useRef(null)
  const hasLoadedRef = useRef(false)

  // DIRECT API CALL - NO HOOKS, NO COMPLEXITY
  useEffect(() => {
    console.log('🏗️ Home component mounted/updated, hasLoadedRef:', hasLoadedRef.current)
    
    if (hasLoadedRef.current) {
      console.log('⏭️ Skipping API call - already loaded')
      return
    }
    
    console.log('🚀 DIRECT API CALL - NO HOOKS')
    hasLoadedRef.current = true
    
    fetch('/api/songs/')
      .then(response => response.json())
      .then(data => {
        console.log('✅ DIRECT API SUCCESS:', data)
        setSongs(Array.isArray(data) ? data : (data.results || []))
        setLoading(false)
      })
      .catch(err => {
        console.error('❌ DIRECT API ERROR:', err)
        setError(err.message)
        setLoading(false)
      })
  }, [])

  console.log(songs)

  // Memoize search results to prevent unnecessary recalculations
  const filteredResults = useMemo(() => {
    if (!searchQuery.trim() || !songs.length) return []
    
    return songs.filter(song => 
      song.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      song.artist?.name?.toLowerCase().includes(searchQuery.toLowerCase())
    )
  }, [searchQuery, songs])

  // Update search results when filtered results change
  useEffect(() => {
    setSearchResults(filteredResults)
    setShowRecommendButton(filteredResults.length === 0 && searchQuery.trim())
  }, [filteredResults, searchQuery])

  // Animation sequence timing - memoized to prevent recreation
  const animationTimeline = useMemo(() => [
    { phase: 'unmasking', delay: 500 },
    { phase: 'letters', delay: 1500 },
    { phase: 'search', delay: 2000 },
    { phase: 'marquee', delay: 5000 }
  ], [])

  // Animation sequence timing
  useEffect(() => {
    animationTimeline.forEach(({ phase, delay }) => {
      setTimeout(() => {
        switch (phase) {
          case 'unmasking':
            setAnimationPhase('unmasking')
            break
          case 'letters':
            setLettersVisible(true)
            break
          case 'search':
            setSearchVisible(true)
            break
          case 'marquee':
            setMarqueeVisible(true)
            break
          default:
            break
        }
      }, delay)
    })
  }, [animationTimeline])

  // Canvas animation for equalizer unmasking
  useEffect(() => {
    if (animationPhase !== 'unmasking') return

    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    const width = window.innerWidth
    const height = window.innerHeight
    
    canvas.width = width
    canvas.height = height

    const bars = 50
    const barWidth = width / bars
    let progress = 0

    const animate = () => {
      ctx.clearRect(0, 0, width, height)
      
      // Draw equalizer bars
      for (let i = 0; i < bars; i++) {
        const x = i * barWidth
        const barHeight = Math.sin(i * 0.3 + progress) * 100 + 50
        const alpha = Math.min(1, (i / bars) / progress)
        
        if (alpha > 0) {
          ctx.fillStyle = `rgba(255, 20, 147, ${alpha})`
          ctx.fillRect(x, height - barHeight, barWidth - 2, barHeight)
        }
      }

      // Create unmasking effect
      const unmaskHeight = height * (1 - progress)
      ctx.fillStyle = 'rgba(0, 0, 0, 0.9)'
      ctx.fillRect(0, 0, width, unmaskHeight)

      progress += 0.0009
      
      if (progress < 1) {
        animationRef.current = requestAnimationFrame(animate)
      } else {
        setAnimationPhase('complete')
      }
    }

    animate()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [animationPhase])

  // Handle search functionality - memoized to prevent recreation
  const handleSearch = useCallback((query) => {
    setSearchQuery(query)
  }, [])

  // Handle song recommendation - memoized to prevent recreation
  const handleRecommendSong = useCallback(async () => {
    try {
      const response = await fetch('/api/song-requests/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: searchQuery,
          artist_name: 'Unknown Artist',
          genre_name: 'Unknown',
          user_email: 'anonymous@example.com',
          user_name: 'Anonymous User',
          additional_notes: `Recommended via search: "${searchQuery}"`
        })
      })

      if (response.ok) {
        alert('Song recommendation submitted successfully!')
        setSearchQuery('')
        setShowRecommendButton(false)
      } else {
        alert('Failed to submit recommendation. Please try again.')
      }
    } catch (error) {
      console.error('Error submitting recommendation:', error)
      alert('Failed to submit recommendation. Please try again.')
    }
  }, [searchQuery])

  // Memoize the main content to prevent unnecessary re-renders
  const mainContent = useMemo(() => (
    <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4">
      {/* Title Section */}
      <div className="text-center mb-16">
        {/* TURKISH MUSIC */}
        <h1 h1 className={`text-4xl sm:text-5xl md:text-6xl lg:text-8xl font-bold mb-6 transition-all duration-1000 ${
          lettersVisible 
            ? 'opacity-100 translate-y-0' 
            : 'opacity-0 translate-y-20'
        }`}>
          {Array.from('TURKISH MUSIC').map((letter, index) => (
            <span
              key={index}
              className={`inline-block animate-fly-in-letter`}
              style={{
                animationDelay: `${index * 100}ms`,
                '--fly-x': `${(Math.random() - 0.5) * 200}px`,
                '--fly-y': `${(Math.random() - 0.5) * 200}px`,
                '--fly-rotate': `${(Math.random() - 0.5) * 180}deg`
              }}
            >
              {letter}
            </span>
          ))}
        </h1>

        {/* DISCOVER SONGS & CHORDS */}
        <h2 className={`text-xl md:text-3xl font-medium text-gray-300 transition-all duration-1000 ${
          lettersVisible 
            ? 'opacity-100 translate-y-0' 
            : 'opacity-0 translate-y-20'
        }`} style={{ animationDelay: '500ms' }}>
          {Array.from('DISCOVER SONGS & CHORDS').map((letter, index) => (
            <span
              key={index}
              className={`inline-block animate-fly-in-letter`}
              style={{
                animationDelay: `${(index * 50) + 800}ms`,
                '--fly-x': `${(Math.random() - 0.5) * 150}px`,
                '--fly-y': `${(Math.random() - 0.5) * 150}px`,
                '--fly-rotate': `${(Math.random() - 0.5) * 120}deg`
              }}
            >
              {letter}
            </span>
          ))}
        </h2>
      </div>

      {/* Search Section */}
      <div className={`w-full max-w-2xl transition-all duration-1000 ${
        searchVisible 
          ? 'opacity-100 translate-y-0' 
          : 'opacity-0 translate-y-20'
      }`}>
        <SearchBar
          value={searchQuery}
          onChange={handleSearch}
          placeholder="Search for songs or artists..."
          className="mb-8"
        />

        {/* Search Results */}
        {searchResults.length > 0 && (
          <div className="bg-gray-900 rounded-lg p-4 mb-4 max-h-60 overflow-y-auto">
            {searchResults.map((song) => (
              <div key={song.id} className="flex items-center justify-between py-2 border-b border-gray-700 last:border-b-0">
                <div>
                  <div className="font-medium">{song.title}</div>
                  <div className="text-sm text-gray-400">{song.artist?.name || 'Unknown Artist'}</div>
                </div>
                <div className="text-xs text-gray-500">
                  {song.genre?.name || 'Unknown Genre'}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Recommendation Button */}
        {showRecommendButton && (
          <div className="text-center">
            <button
              onClick={handleRecommendSong}
              className="inline-flex items-center gap-2 bg-pink-600 hover:bg-pink-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
            >
              <span className="text-xl">+</span>
              Recommend "{searchQuery}"
            </button>
            <p className="text-sm text-gray-400 mt-2">
              This song isn't in our database yet. Help us add it!
            </p>
          </div>
        )}
      </div>

      {/* Marquee Section */}
      <div className={`w-full transition-all duration-1000 ${
        marqueeVisible 
          ? 'opacity-100 translate-y-0' 
          : 'opacity-0 translate-y-20'
      }`}>
        <Marquee songs={songs} />
      </div>
    </div>
  ), [lettersVisible, searchVisible, marqueeVisible, searchQuery, searchResults, showRecommendButton, songs, handleSearch, handleRecommendSong])

  return (
    <div className="min-h-screen bg-black text-white font-roboto-mono overflow-hidden">
      {/* Canvas for unmasking animation */}
      {animationPhase === 'unmasking' && (
        <canvas
          ref={canvasRef}
          className="fixed inset-0 z-50 pointer-events-none"
        />
      )}

      {/* Main content */}
      {mainContent}

      {/* Loading State */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="text-white text-xl">Loading Turkish Music...</div>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="text-red-400 text-xl">Error loading music data</div>
        </div>
      )}
    </div>
  )
}

export default Home