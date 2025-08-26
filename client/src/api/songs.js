const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Global state to prevent multiple API calls
let globalSongsData = null
let globalLoading = false
let globalError = null
let globalPromise = null

class SongsAPI {
  constructor() {
    this.baseURL = `${API_BASE_URL}/api`
    this.cache = new Map()
    this.cacheTimeout = 5 * 60 * 1000 // 5 minutes
  }

  // Helper method to handle API responses
  async handleResponse(response) {
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
    }
    return response.json()
  }

  // Helper method to check cache validity
  isCacheValid(timestamp) {
    return Date.now() - timestamp < this.cacheTimeout
  }

  // Global method to get songs - ensures only one API call ever
  async getSongsGlobal(options = {}) {
    console.log('🌍 getSongsGlobal called with:', { options, globalSongsData, globalLoading, globalPromise })
    
    // If we already have data, return it immediately
    if (globalSongsData) {
      console.log('✅ Returning cached global data')
      return globalSongsData
    }
    
    // If we're already loading, return the existing promise
    if (globalLoading && globalPromise) {
      console.log('⏳ Returning existing loading promise')
      return globalPromise
    }
    
    // If we have a promise but not loading, something went wrong, reset
    if (globalPromise && !globalLoading) {
      console.log('🔄 Resetting global state due to promise without loading')
      globalPromise = null
      globalError = null
    }
    
    // Start loading
    console.log('🚀 Starting new global API call')
    globalLoading = true
    globalError = null
    
    // Create the promise
    globalPromise = this.getSongs(options)
      .then(data => {
        console.log('✅ Global API call successful, storing data')
        globalSongsData = data
        globalLoading = false
        globalPromise = null
        return data
      })
      .catch(error => {
        console.error('❌ Global API call failed:', error)
        globalError = error
        globalLoading = false
        globalPromise = null
        throw error
      })
    
    return globalPromise
  }

  // Get all songs with optional filters
  async getSongs(options = {}) {
    const cacheKey = `songs-${JSON.stringify(options)}`
    const cached = this.cache.get(cacheKey)
    
    if (cached && this.isCacheValid(cached.timestamp)) {
      return cached.data
    }

    try {
      const params = new URLSearchParams()
      
      if (options.search) params.append('search', options.search)
      if (options.genre) params.append('genre', options.genre)
      if (options.artist) params.append('artist', options.artist)
      if (options.difficulty) params.append('difficulty', options.difficulty)
      if (options.is_popular) params.append('is_popular', options.is_popular)
      if (options.page) params.append('page', options.page)
      if (options.page_size) params.append('page_size', options.page_size)

      const response = await fetch(`${this.baseURL}/songs/?${params.toString()}`)
      const data = await this.handleResponse(response)

      // Cache the result
      this.cache.set(cacheKey, {
        data,
        timestamp: Date.now()
      })

      return data
    } catch (error) {
      console.error('Error fetching songs:', error)
      throw error
    }
  }

  // Get a specific song by ID
  async getSongById(id) {
    const cacheKey = `song-${id}`
    const cached = this.cache.get(cacheKey)
    
    if (cached && this.isCacheValid(cached.timestamp)) {
      return cached.data
    }

    try {
      const response = await fetch(`${this.baseURL}/songs/${id}/`)
      const data = await this.handleResponse(response)

      // Cache the result
      this.cache.set(cacheKey, {
        data,
        timestamp: Date.now()
      })

      return data
    } catch (error) {
      console.error(`Error fetching song ${id}:`, error)
      throw error
    }
  }

  // Search songs by query
  async searchSongs(query, options = {}) {
    return this.getSongs({ search: query, ...options })
  }

  // Get popular songs
  async getPopularSongs(limit = 10) {
    return this.getSongs({ is_popular: true, page_size: limit })
  }

  // Get songs by genre
  async getSongsByGenre(genreId, options = {}) {
    return this.getSongs({ genre: genreId, ...options })
  }

  // Get songs by artist
  async getSongsByArtist(artistId, options = {}) {
    return this.getSongs({ artist: artistId, ...options })
  }

  // Get songs by difficulty
  async getSongsByDifficulty(difficulty, options = {}) {
    return this.getSongs({ difficulty, ...options })
  }

  // Clear cache
  clearCache() {
    this.cache.clear()
  }

  // Clear specific cache entry
  clearCacheEntry(key) {
    this.cache.delete(key)
  }

  // Get cache statistics
  getCacheStats() {
    const entries = Array.from(this.cache.entries())
    const validEntries = entries.filter(([_, value]) => this.isCacheValid(value.timestamp))
    const expiredEntries = entries.length - validEntries.length

    return {
      totalEntries: entries.length,
      validEntries: validEntries.length,
      expiredEntries,
      cacheSize: entries.length
    }
  }

  // Reset global state (for testing)
  resetGlobalState() {
    globalSongsData = null
    globalLoading = false
    globalError = null
    globalPromise = null
    console.log('🔄 Global state reset')
  }
}

// Create and export a singleton instance
const songsAPI = new SongsAPI()

export default songsAPI

// Export individual methods for convenience
export const {
  getSongs,
  getSongById,
  searchSongs,
  getPopularSongs,
  getSongsByGenre,
  getSongsByArtist,
  getSongsByDifficulty,
  clearCache,
  clearCacheEntry,
  getCacheStats,
  getSongsGlobal,
  resetGlobalState
} = songsAPI
