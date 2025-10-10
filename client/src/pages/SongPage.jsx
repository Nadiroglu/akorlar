import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getSongById } from '../api/songs'
import Spinner from '../components/Loaders/Spinner'

const SongPage = () => {
  const { songId } = useParams()
  const [song, setSong] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchSong = async () => {
      try {
        setLoading(true)
        setError(null)
        console.log(`Fetching song with Id: ${songId}...`)
        const response = await getSongById(songId)
        console.log('Song data received:', response)
        console.log('Song data received:', response)
        console.log('Chords data:', response.chords)
        console.log('Lyrics data:', response.lyrics)
        console.log('Lyrics length:', response.lyrics?.length)
        setSong(response)
      } catch (err) {
        console.error('Error fetching song:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    if (songId) {
      fetchSong()
    }
  }, [songId])

  // Loading State
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Spinner type="equalizer" size="xl" color="pink" className="mx-auto mb-4" />
          <p className="text-gray-600 text-lg">Loading song...</p>
        </div>
      </div>
    )
  }

  // Error State
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Error Loading Song</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-pink-600 text-white px-6 py-2 rounded-lg hover:bg-pink-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  // Not Found State
  if (!song) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-400 text-6xl mb-4">🎵</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Song Not Found</h2>
          <p className="text-gray-600">The song you're looking for doesn't exist.</p>
        </div>
      </div>
    )
  }

  // Main Song Display
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          
          {/* Song Header */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
              <div className="mb-4 md:mb-0">
                <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                  {song.title}
                </h1>
                <p className="text-xl text-gray-600">
                  by {song.artist?.name || 'Unknown Artist'}
                </p>
              </div>
              
              {/* Song Metadata Badges */}
              <div className="flex flex-wrap gap-2">
                <span className="bg-pink-100 text-pink-800 px-3 py-1 rounded-full text-sm font-medium">
                  Key: {song.key || 'Unknown'}
                </span>
                <span className="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                  {song.difficulty || 'Unknown'}
                </span>
                {song.genre && (
                  <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                    {song.genre.name}
                  </span>
                )}
              </div>
            </div>

            {/* Additional Song Info Grid */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm text-gray-600 border-t pt-4">
              <div>
                <span className="font-medium">Year:</span> {song.year || 'Unknown'}
              </div>
              <div>
                <span className="font-medium">Tempo:</span> {song.tempo ? `${song.tempo} BPM` : 'Unknown'}
              </div>
              <div>
                <span className="font-medium">Duration:</span> {song.duration ? `${song.duration}s` : 'Unknown'}
              </div>
            </div>
          </div>

          {/* Tone Adjustment Section */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">🎸 Tone Adjustment</h2>
            <p className="text-gray-600 mb-4">
              Current Key: <span className="font-bold text-pink-600 text-lg">{song.key}</span>
            </p>
            <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <p className="text-gray-500 text-lg">🎵 Key selector buttons will be added here</p>
              <p className="text-gray-400 text-sm mt-2">Click a key to instantly transpose all chords</p>
            </div>
          </div>

          {/* Chords & Lyrics Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">📝 Chords & Lyrics</h2>
            
            {/* Display chords if available */}
            {song.chords && song.chords.length > 0 ? (
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Chord Progression:</h3>
                <div className="flex flex-wrap gap-2 mb-4">
                  {song.chords.map((chord, index) => (
                    <span 
                      key={index}
                      className="bg-pink-100 text-pink-800 px-3 py-1 rounded-md text-sm font-mono font-medium"
                    >
                      {chord.chord_name}
                    </span>
                  ))}
                </div>
              </div>
            ) : null}

            {/* Display lyrics */}
            {song.lyrics ? (
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Lyrics:</h3>
                <div className="whitespace-pre-line text-gray-700 leading-relaxed font-mono text-sm md:text-base bg-gray-50 p-4 rounded-lg">
                  {song.lyrics}
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500 italic text-lg">No lyrics available for this song.</p>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  )
}

export default SongPage