// API base URL - can be configured per environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

/**
 * Fetch chords for a specific song
 * @param {string|number} songId - The song ID
 * @param {Object} options - Chord options
 * @param {string} options.key - Musical key (C, D, E, etc.)
 * @param {string} options.difficulty - Difficulty level (beginner, intermediate, advanced)
 * @returns {Promise<Object>} Chord data for the song
 */
export const fetchChordsForSong = async (songId, options = {}) => {
  try {
    const params = new URLSearchParams()
    
    if (options.key) params.append('key', options.key)
    if (options.difficulty) params.append('difficulty', options.difficulty)
    
    const response = await fetch(`${API_BASE_URL}/songs/${songId}/chords?${params}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`Error fetching chords for song ${songId}:`, error)
    throw error
  }
}

/**
 * Fetch chord diagrams for specific chords
 * @param {Array<string>} chordNames - Array of chord names
 * @param {Object} options - Diagram options
 * @param {string} options.position - Fretboard position (open, barre, etc.)
 * @param {string} options.tuning - Guitar tuning (standard, drop D, etc.)
 * @returns {Promise<Array>} Array of chord diagrams
 */
export const fetchChordDiagrams = async (chordNames, options = {}) => {
  try {
    const params = new URLSearchParams()
    
    chordNames.forEach(chord => params.append('chords', chord))
    if (options.position) params.append('position', options.position)
    if (options.tuning) params.append('tuning', options.tuning)
    
    const response = await fetch(`${API_BASE_URL}/chords/diagrams?${params}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('Error fetching chord diagrams:', error)
    throw error
  }
}

/**
 * Fetch chord progression for a song
 * @param {string|number} songId - The song ID
 * @param {string} key - Musical key
 * @returns {Promise<Object>} Chord progression data
 */
export const fetchChordProgression = async (songId, key) => {
  try {
    const response = await fetch(`${API_BASE_URL}/songs/${songId}/progression?key=${key}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`Error fetching chord progression for song ${songId}:`, error)
    throw error
  }
}

/**
 * Fetch available keys for a song
 * @param {string|number} songId - The song ID
 * @returns {Promise<Array>} Array of available keys
 */
export const fetchAvailableKeys = async (songId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/songs/${songId}/keys`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`Error fetching available keys for song ${songId}:`, error)
    throw error
  }
}

/**
 * Transpose chords to a different key
 * @param {Array<string>} chords - Array of chord names
 * @param {string} fromKey - Original key
 * @param {string} toKey - Target key
 * @returns {Promise<Array>} Transposed chords
 */
export const transposeChords = async (chords, fromKey, toKey) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chords/transpose`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chords,
        fromKey,
        toKey
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('Error transposing chords:', error)
    throw error
  }
}

/**
 * Fetch chord theory information
 * @param {string} chordName - Chord name
 * @returns {Promise<Object>} Chord theory data
 */
export const fetchChordTheory = async (chordName) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chords/${chordName}/theory`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error(`Error fetching theory for chord ${chordName}:`, error)
    throw error
  }
}
