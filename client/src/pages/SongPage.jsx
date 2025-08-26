import React from 'react'
import { useParams } from 'react-router-dom'

const SongPage = () => {
  const { songId } = useParams()

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Song Details
        </h1>
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-gray-600">
            Song ID: {songId}
          </p>
          <p className="text-gray-500 mt-4">
            This page will display detailed information about the song, including lyrics, chords, and other metadata.
          </p>
        </div>
      </div>
    </div>
  )
}

export default SongPage
