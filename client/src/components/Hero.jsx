import React, { useState, useEffect } from 'react'

const Hero = ({ 
  backgroundImage, 
  title = "Turkish Music – Discover Songs & Chords", 
  subtitle = "Discover the rich sounds and rhythms of Turkey",
  buttonText = "Get Started",
  onButtonClick,
  className = ""
}) => {
  const [isAnimating, setIsAnimating] = useState(true)
  const [showMarquee, setShowMarquee] = useState(false)
  const [showTitle, setShowTitle] = useState(false)
  const [showSearchBar, setShowSearchBar] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    // Pink overlay reveal animation completes after 2 seconds
    const revealTimer = setTimeout(() => {
      setIsAnimating(false)
    }, 2000)

    // Title starts appearing 2.5 seconds after reveal starts
    const titleTimer = setTimeout(() => {
      setShowTitle(true)
    }, 2500)

    // Search bar appears 4 seconds after reveal starts (1.5s after title)
    const searchTimer = setTimeout(() => {
      setShowSearchBar(true)
    }, 4000)

    // Marquee appears 4.5 seconds after reveal starts (0.5s after search bar)
    const marqueeTimer = setTimeout(() => {
      setShowMarquee(true)
    }, 4500)

    return () => {
      clearTimeout(revealTimer)
      clearTimeout(titleTimer)
      clearTimeout(searchTimer)
      clearTimeout(marqueeTimer)
    }
  }, [])

  const popularItems = [
    "Pop", "Rock", "Folk", "Jazz", "Classical", "Electronic", "Hip Hop", "R&B"
  ]

  // Split title into individual characters for staggered animation
  const titleChars = title.split('')

  return (
    <div className={`min-h-screen relative overflow-hidden ${className}`}>
      {/* Hero Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('${backgroundImage}')`
        }}
      />
      
      {/* Dark Gradient Overlay for Better Text Readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-black/80" />
      
      {/* Pink Overlay with Stepped Reveal Animation */}
      <div 
        className={`absolute inset-0 bg-pink-500 transition-all duration-1000 ease-out ${
          isAnimating ? 'opacity-100' : 'opacity-0'
        }`}
        style={{
          clipPath: isAnimating 
            ? 'polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)' 
            : 'polygon(0% 0%, 0% 0%, 0% 100%, 0% 100%)'
        }}
      >
        {/* Stepped Reveal Blocks */}
        <div className="absolute inset-0">
          {/* Top row of blocks */}
          <div className={`absolute top-0 left-0 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '0ms' }} />
          <div className={`absolute top-0 left-1/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '200ms' }} />
          <div className={`absolute top-0 left-2/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '400ms' }} />
          <div className={`absolute top-0 left-3/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '600ms' }} />
          
          {/* Second row */}
          <div className={`absolute top-1/4 left-0 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '100ms' }} />
          <div className={`absolute top-1/4 left-1/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '300ms' }} />
          <div className={`absolute top-1/4 left-2/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '500ms' }} />
          <div className={`absolute top-1/4 left-3/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '700ms' }} />
          
          {/* Third row */}
          <div className={`absolute top-2/4 left-0 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '200ms' }} />
          <div className={`absolute top-2/4 left-1/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '400ms' }} />
          <div className={`absolute top-2/4 left-2/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '600ms' }} />
          <div className={`absolute top-2/4 left-3/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '800ms' }} />
          
          {/* Bottom row */}
          <div className={`absolute top-3/4 left-0 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '300ms' }} />
          <div className={`absolute top-1/4 left-1/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '500ms' }} />
          <div className={`absolute top-3/4 left-2/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '700ms' }} />
          <div className={`absolute top-3/4 left-3/4 w-1/4 h-1/4 bg-pink-500 transition-all duration-300 ${
            isAnimating ? 'translate-x-0' : '-translate-x-full'
          }`} style={{ transitionDelay: '900ms' }} />
        </div>
      </div>
      
      {/* Hero Content - Centered */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen text-white px-4">
        <div className="text-center max-w-4xl mx-auto">
          
          {/* Main Title - Staggered Letter Animation */}
          {showTitle && (
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-8 text-center">
              {titleChars.map((char, index) => (
                <span
                  key={index}
                  className="inline-block animate-letter-fly-in"
                  style={{
                    animationDelay: `${Math.random() * 0.5}s`,
                    animationDuration: '0.8s',
                    animationFillMode: 'both'
                  }}
                >
                  {char === ' ' ? '\u00A0' : char}
                </span>
              ))}
            </h1>
          )}
          
          {/* Search Bar - Ninja Strike Animation */}
          {showSearchBar && (
            <div className="mb-8 animate-ninja-strike">
              <div className="relative max-w-md mx-auto">
                <input
                  type="text"
                  placeholder="Search for music, artists, or genres..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-6 py-4 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full text-white placeholder-white/70 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent transition-all duration-300 shadow-2xl hover:shadow-pink-500/25 hover:bg-white/20"
                />
                <button className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-pink-500 hover:bg-pink-600 text-white px-6 py-2 rounded-full transition-colors duration-300 shadow-lg hover:shadow-xl">
                  Search
                </button>
              </div>
            </div>
          )}
          
          {/* Marquee - Appears Below Search Bar */}
          {showMarquee && (
            <div className="mb-8 animate-fade-in-up">
              <div className="bg-purple-600/90 backdrop-blur-sm rounded-lg py-4 px-6 overflow-hidden">
                <div className="marquee-container">
                  <div className="marquee-content">
                    {popularItems.map((item, index) => (
                      <a
                        key={index}
                        href={`/genre/${item.toLowerCase()}`}
                        className="inline-block mx-6 text-white hover:text-pink-200 transition-colors duration-300 font-medium text-lg whitespace-nowrap"
                      >
                        {item}
                      </a>
                    ))}
                    {/* Duplicate items for seamless loop */}
                    {popularItems.map((item, index) => (
                      <a
                        key={`duplicate-${index}`}
                        href={`/genre/${item.toLowerCase()}`}
                        className="inline-block mx-6 text-white hover:text-pink-200 transition-colors duration-300 font-medium text-lg whitespace-nowrap"
                      >
                        {item}
                      </a>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* CTA Button */}
          <button 
            className="bg-white text-gray-900 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors shadow-lg hover:shadow-xl"
            onClick={onButtonClick}
          >
            {buttonText}
          </button>
        </div>
      </div>
      
      {/* Google Ads Slot - Reserved Space at Bottom */}
      <div className="absolute bottom-0 left-0 right-0 bg-gray-900/80 backdrop-blur-sm py-6 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700/50">
            <p className="text-gray-400 text-sm mb-2">Advertisement</p>
            <div className="bg-gray-700/50 rounded h-16 flex items-center justify-center">
              <span className="text-gray-500 text-sm">Google Ads Slot</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Hero
