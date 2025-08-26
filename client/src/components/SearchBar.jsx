import React, { useState, useEffect } from 'react'

const SearchBar = ({ value, onChange, placeholder, className = '' }) => {
  const [isFocused, setIsFocused] = useState(false)
  const [isAnimating, setIsAnimating] = useState(false)

  useEffect(() => {
    if (value) {
      setIsAnimating(true)
      const timer = setTimeout(() => setIsAnimating(false), 300)
      return () => clearTimeout(timer)
    }
  }, [value])

  return (
    <div className={`relative ${className}`}>
      <div className="relative">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder={placeholder}
          className={`
            w-full px-6 py-4 text-lg bg-gray-900 border-2 rounded-lg
            text-white placeholder-gray-400 font-roboto-mono
            transition-all duration-300 ease-out
            ${isFocused 
              ? 'border-pink-500 bg-gray-800 shadow-lg shadow-pink-500/25' 
              : 'border-gray-700 hover:border-gray-600'
            }
            ${isAnimating ? 'animate-ninja-strike' : ''}
            focus:outline-none focus:ring-0
          `}
        />
        
        {/* Search Icon */}
        <div className={`
          absolute right-4 top-1/2 -translate-y-1/2
          text-gray-400 transition-all duration-300
          ${isFocused ? 'text-pink-500 scale-110' : ''}
        `}>
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        {/* Animated Border */}
        <div className={`
          absolute inset-0 rounded-lg border-2 border-transparent
          transition-all duration-300 pointer-events-none
          ${isFocused ? 'border-pink-500/50 scale-105' : ''}
        `} />
      </div>

      {/* Floating Label Effect */}
      {value && (
        <div className={`
          absolute -top-2 left-4 px-2 text-xs text-pink-500 bg-black
          transition-all duration-300 font-roboto-mono
          ${isFocused ? 'scale-110' : 'scale-100'}
        `}>
          Search Query
        </div>
      )}
    </div>
  )
}

export default SearchBar
