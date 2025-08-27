#!/bin/bash

# WSL Setup Script for Akorlar Django Backend
# This script sets up the database with all seeds

echo "🚀 Starting Akorlar Django Backend Setup in WSL..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the backend directory."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔧 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
fi

# Run migrations
echo "🔄 Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Run the master seeds
echo "🌱 Running master seeds..."
python run_seeds.py

echo "🎉 Setup completed! Your database should now be populated with:"
echo "   • 20+ Genres"
echo "   • 20 Artists"
echo "   • 20 Songs"
echo "   • 25+ Chord Diagrams"
echo "   • Chord progressions for all songs"
echo ""
echo "🚀 You can now start the Django server with:"
echo "   python manage.py runserver"
echo ""
echo "🌐 Your API will be available at: http://localhost:8000/api/"
