// API base URL - can be configured per environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

/**
 * Fetch ad content for a specific placement
 * @param {string} placement - Ad placement (hero, sidebar, footer, etc.)
 * @param {Object} options - Ad options
 * @param {string} options.category - Content category for contextual ads
 * @param {string} options.size - Ad size (banner, skyscraper, etc.)
 * @param {boolean} options.responsive - Whether to return responsive ad data
 * @returns {Promise<Object>} Ad content and configuration
 */
export const fetchAdContent = async (placement, options = {}) => {
  try {
    const params = new URLSearchParams({ placement })
    
    if (options.category) params.append('category', options.category)
    if (options.size) params.append('size', options.size)
    if (options.responsive) params.append('responsive', options.responsive)
    
    const response = await fetch(`${API_BASE_URL}/ads/content?${params}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`Error fetching ad content for placement ${placement}:`, error)
    throw error
  }
}

/**
 * Fetch Google Ads configuration
 * @param {string} slot - Ad slot ID
 * @param {Object} options - Ad slot options
 * @returns {Promise<Object>} Google Ads configuration
 */
export const fetchGoogleAdsConfig = async (slot, options = {}) => {
  try {
    const params = new URLSearchParams({ slot })
    
    if (options.format) params.append('format', options.format)
    if (options.responsive) params.append('responsive', options.responsive)
    
    const response = await fetch(`${API_BASE_URL}/ads/google?${params}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`Error fetching Google Ads config for slot ${slot}:`, error)
    throw error
  }
}

/**
 * Track ad impression
 * @param {string} adId - The ad ID
 * @param {Object} data - Impression data
 * @returns {Promise<Object>} Tracking confirmation
 */
export const trackAdImpression = async (adId, data = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}/ads/${adId}/impression`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        timestamp: new Date().toISOString(),
        ...data
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`Error tracking impression for ad ${adId}:`, error)
    throw error
  }
}

/**
 * Track ad click
 * @param {string} adId - The ad ID
 * @param {Object} data - Click data
 * @returns {Promise<Object>} Tracking confirmation
 */
export const trackAdClick = async (adId, data = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}/ads/${adId}/click`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        timestamp: new Date().toISOString(),
        ...data
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`Error tracking click for ad ${adId}:`, error)
    throw error
  }
}

/**
 * Fetch ad refresh timing configuration
 * @param {string} placement - Ad placement
 * @returns {Promise<Object>} Refresh timing settings
 */
export const fetchAdRefreshTiming = async (placement) => {
  try {
    const response = await fetch(`${API_BASE_URL}/ads/${placement}/refresh-timing`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`Error fetching refresh timing for placement ${placement}:`, error)
    throw error
  }
}

/**
 * Check if ads are enabled for the current user
 * @param {Object} userContext - User context information
 * @returns {Promise<boolean>} Whether ads are enabled
 */
export const checkAdsEnabled = async (userContext = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}/ads/enabled`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userContext)
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const result = await response.json()
    return result.enabled
  } catch (error) {
    console.error('Error checking if ads are enabled:', error)
    // Default to showing ads if there's an error
    return true
  }
}
