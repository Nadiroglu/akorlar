#!/usr/bin/env python
"""
Master seed file that runs all individual seed files in the correct order
Run with: python manage.py shell < seeds_master.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def run_all_seeds():
    """Run all seed files in the correct order"""
    print("🌱 Starting database seeding process...\n")
    
    try:
        # 1. Seed Genres first (no dependencies)
        print("📚 Seeding Genres...")
        from api.seeds.seeds_genre import seed_genres
        genre_count = seed_genres()
        print(f"✅ Genres seeded: {genre_count}\n")
        
        # 2. Seed Artists (no dependencies)
        print("🎤 Seeding Artists...")
        from api.seeds.seeds_artist import seed_artists
        artist_count = seed_artists()
        print(f"✅ Artists seeded: {artist_count}\n")
        
        # 3. Seed Songs (depends on Genres and Artists)
        print("🎵 Seeding Songs...")
        from api.seeds.seeds_song import seed_songs
        song_count = seed_songs()
        print(f"✅ Songs seeded: {song_count}\n")
        
        # 4. Seed Chord Diagrams (no dependencies)
        print("🎸 Seeding Chord Diagrams...")
        from api.seeds.seeds_chord_diagram import seed_chord_diagrams
        chord_diagram_count = seed_chord_diagrams()
        print(f"✅ Chord Diagrams seeded: {chord_diagram_count}\n")
        
        # 5. Seed Chords (depends on Songs)
        print("🎼 Seeding Chords...")
        from api.seeds.seeds_chord_professional import seed_chords_professional
        chord_count = seed_chords_professional()
        print(f"✅ Chords seeded: {chord_count}\n")
        
        # 6. Seed Search Queries (no dependencies)
        print("🔍 Seeding Search Queries...")
        from api.seeds.seeds_search_query import seed_search_queries
        search_query_count = seed_search_queries()
        print(f"✅ Search Queries seeded: {search_query_count}\n")
        
        # Summary
        total_created = genre_count + artist_count + song_count + chord_diagram_count + chord_count + search_query_count
        print("🎉 Database seeding completed successfully!")
        print(f"📊 Total records created: {total_created}")
        print("\n📋 Summary:")
        print(f"   • Genres: {genre_count}")
        print(f"   • Artists: {artist_count}")
        print(f"   • Songs: {song_count}")
        print(f"   • Chord Diagrams: {chord_diagram_count}")
        print(f"   • Chords: {chord_count}")
        print(f"   • Search Queries: {search_query_count}")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        print("Please check that all required models exist and dependencies are met.")
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_seeds()
    if success:
        print("\n🚀 Your database is now populated with sample data!")
        print("You can now test your API endpoints with real data.")
    else:
        print("\n💥 Seeding failed. Please check the error messages above.")
        sys.exit(1)
