#!/usr/bin/env python3
"""
Database setup script for Akorlar Django application
This script helps set up PostgreSQL database and initial data
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_database():
    """Set up the database with initial data"""
    print("Setting up Akorlar database...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()
    
    # Run migrations
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser if needed
    print("Creating superuser...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@akorlar.com', 'admin123')
            print("Superuser created: admin/admin123")
        else:
            print("Superuser already exists")
    except Exception as e:
        print(f"Error creating superuser: {e}")
    
    # Create initial genres
    print("Creating initial genres...")
    try:
        from api.models import Genre
        genres = [
            'Pop', 'Rock', 'Folk', 'Jazz', 'Classical', 
            'Electronic', 'Hip Hop', 'R&B', 'Country', 'Blues',
            'Reggae', 'Metal', 'Punk', 'Indie', 'Alternative'
        ]
        
        for genre_name in genres:
            Genre.objects.get_or_create(name=genre_name)
        print(f"Created {len(genres)} genres")
    except Exception as e:
        print(f"Error creating genres: {e}")
    
    print("Database setup completed!")

if __name__ == '__main__':
    setup_database()
