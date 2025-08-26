import React from 'react'

const Marquee = ({ songs = [] }) => {
  const popularSongs = songs.filter(song => song.is_popular).slice(0, 10)
  
  if (popularSongs.length === 0) {
    return (
      <div className="w-full py-8 text-center">
        <div className="text-gray-500 font-roboto-mono">
          No popular songs available yet
        </div>
      </div>
    )
  }

  return (
    <div className="w-full py-8">
      <div className="text-center mb-6">
        <h3 className="text-2xl font-bold text-white font-roboto-mono">
          Popular Songs
        </h3>
        <div className="w-24 h-1 bg-pink-500 mx-auto mt-2 rounded-full"></div>
      </div>

      <div className="relative overflow-hidden">
        <div className="marquee-container">
          <div className="marquee-content">
            {/* First set of songs */}
            {popularSongs.map((song, index) => (
              <div
                key={`first-${song.id}`}
                className="inline-block mx-8 text-center min-w-[200px]"
              >
                <div className="bg-gray-900 rounded-lg p-4 border border-gray-700 hover:border-pink-500 transition-colors duration-300">
                  <div className="w-16 h-16 bg-pink-600 rounded-full mx-auto mb-3 flex items-center justify-center">
                    <span className="text-white text-2xl">🎵</span>
                  </div>
                  <h4 className="font-medium text-white text-sm mb-1 font-roboto-mono">
                    {song.title}
                  </h4>
                  <p className="text-xs text-gray-400 font-roboto-mono">
                    {song.artist.name}
                  </p>
                  {song.genre && (
                    <span className="inline-block mt-2 px-2 py-1 bg-pink-600 text-white text-xs rounded-full font-roboto-mono">
                      {song.genre.name}
                    </span>
                  )}
                </div>
              </div>
            ))}
            
            {/* Duplicate set for seamless loop */}
            {popularSongs.map((song, index) => (
              <div
                key={`second-${song.id}`}
                className="inline-block mx-8 text-center min-w-[200px]"
              >
                <div className="bg-gray-900 rounded-lg p-4 border border-gray-700 hover:border-pink-500 transition-colors duration-300">
                  <div className="w-16 h-16 bg-pink-600 rounded-full mx-auto mb-3 flex items-center justify-center">
                    <span className="text-white text-2xl">🎵</span>
                  </div>
                  <h4 className="font-medium text-white text-sm mb-1 font-roboto-mono">
                    {song.title}
                  </h4>
                  <p className="text-xs text-gray-400 font-roboto-mono">
                    {song.artist.name}
                  </p>
                  {song.genre && (
                    <span className="inline-block mt-2 px-2 py-1 bg-pink-600 text-white text-xs rounded-full font-roboto-mono">
                      {song.genre.name}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Marquee
