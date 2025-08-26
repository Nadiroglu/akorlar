import React from 'react'
import { useParams } from 'react-router-dom'

const ChordPage = () => {
  const { chordName } = useParams()

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">
          Chord: {chordName}
        </h1>
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-gray-600">
            Chord Name: {chordName}
          </p>
          <p className="text-gray-500 mt-4">
            This page will display detailed chord information, including diagrams, fingerings, and theory.
          </p>
        </div>
      </div>
    </div>
  )
}

export default ChordPage
