import React from 'react'
import { useSearchParams } from 'react-router-dom'

const SearchPage = () => {
  const [searchParams] = useSearchParams()
  const query = searchParams.get('q') || ''

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Search Results
        </h1>
        {query && (
          <p className="text-lg text-gray-600 mb-6">
            Results for: <span className="font-semibold">"{query}"</span>
          </p>
        )}
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-gray-500">
            This page will display search results for songs, artists, and chords based on your query.
          </p>
        </div>
      </div>
    </div>
  )
}

export default SearchPage
