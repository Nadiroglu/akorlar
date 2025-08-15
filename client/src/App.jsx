import { useState } from 'react'


function App() {

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="p-8 rounded-2xl shadow-lg bg-white text-center">
        <h1 className="text-4xl font-bold text-blue-600 mb-4">
          Tailwind is Working 🎉
        </h1>
        <p className="text-gray-600">
          If you see this styled box with blue text, Tailwind is installed correctly.
        </p>
        <button className="mt-6 px-4 py-2 rounded-lg bg-blue-500 text-white font-semibold hover:bg-blue-600 transition">
          Click Me
        </button>
      </div>
    </div>
  );
}


export default App
