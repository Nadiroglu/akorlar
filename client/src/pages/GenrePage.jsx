import React from 'react'
import { useParams } from 'react-router-dom'

const GenrePage = () => {
  const { genreName } = useParams()

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          {genreName} Music
        </h1>
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-gray-600">
            Genre: {genreName}
          </p>
          <p className="text-gray-500 mt-4">
            This page will display songs, artists, and content related to the {genreName} genre.
          </p>
        </div>
      </div>
    </div>
  )
}

export default GenrePage
