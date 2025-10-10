#!/usr/bin/env python
"""
Master seed file that runs all individual seed files in the correct order
Run with: python manage.py shell < seeds/seeds_master.py
"""

import os
import sys
import django

# Setup Django environment
# Make sure to replace 'backend.settings' with your actual project's settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def run_all_seeds():
    """Run all seed files in the correct order to populate the database."""
    print("🌱 Starting database seeding process...\n")
    
    total_records = 0
    
    try:
        # 1. Seed Genres first (no dependencies)
        # Use absolute imports from the 'api' app to fix the ImportError
        print("📚 Seeding Genres...")
        from api.seeds.seeds_genre import seed_genres
        count = seed_genres()
        total_records += count
        print(f"✅ Genres seeded: {count}\n")
        
        # 2. Seed Artists (no dependencies)
        print("🎤 Seeding Artists...")
        from api.seeds.seeds_artist import seed_artists
        count = seed_artists()
        total_records += count
        print(f"✅ Artists seeded: {count}\n")
        
        # 3. Seed Songs (depends on Genres and Artists)
        print("🎵 Seeding Songs...")
        from api.seeds.seeds_song import seed_songs
        count = seed_songs()
        total_records += count
        print(f"✅ Songs seeded: {count}\n")
        
        # 4. Seed Chord Diagrams (no dependencies)
        print("🎸 Seeding Chord Diagrams...")
        from api.seeds.seeds_chord_diagram import seed_chord_diagrams
        count = seed_chord_diagrams()
        total_records += count
        print(f"✅ Chord Diagrams seeded: {count}\n")
        
        # 5. Seed Chords (depends on Songs)
        # Using the robust, declarative seeder to ensure data integrity
        print("🎼 Seeding Chords...")
        from api.seeds.seeds_chord import seed_chords
        count = seed_chords()
        total_records += count
        print(f"✅ Chords seeded: {count}\n")
        
        # This part is optional if you don't have a search query seeder
        # from .seeds_search_query import seed_search_queries
        # ...
        
        print("-" * 40)
        print("🎉 Database seeding completed successfully!")
        print(f"📊 Total records created or updated: {total_records}")
        print("-" * 40)
        
    except ImportError as e:
        print(f"\n❌ IMPORT ERROR: {e}")
        print("Please make sure all referenced seed files (e.g., seeds_song.py) exist in the 'seeds' directory.")
        return False
    except Exception as e:
        print(f"\n❌ An unexpected error occurred during seeding: {e}")
        return False
    
    return True

if __name__ == 'django.core.management.commands.shell':
    success = run_all_seeds()
    if success:
        print("\n🚀 Your database is now populated with sample data!")
    else:
        print("\n💥 Seeding failed. Please check the error messages above.")

