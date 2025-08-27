#!/usr/bin/env python
"""
Professional Chord Seeder for Akorlar
Uses music theory engine to generate chord progressions dynamically
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Song, Chord
from api.utils.music_theory import music_engine


def seed_chords_professional():
    """
    Seed chords using the professional music theory engine
    Generates chord progressions dynamically based on song metadata
    """
    print("🎼 Starting professional chord seeding...")
    
    # Clear existing chords
    Chord.objects.all().delete()
    print("🧹 Cleared existing chords")
    
    # Song progression definitions (just the metadata, not hardcoded chords)
    song_progressions = {
        # Barış Manço Songs
        "Dağlar Dağlar": {
            "key": "Am",
            "progression_type": "turkish_pop",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 120,
            "style": "Turkish Rock"
        },
        "Gül Pembe": {
            "key": "C",
            "progression_type": "pop",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 110,
            "style": "Turkish Pop"
        },
        
        # Tarkan Songs
        "Şımarık": {
            "key": "G",
            "progression_type": "pop",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 128,
            "style": "Turkish Pop"
        },
        "Kuzu Kuzu": {
            "key": "D",
            "progression_type": "pop",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 115,
            "style": "Turkish Pop"
        },
        
        # Neşet Ertaş Songs
        "Neredesin Sen": {
            "key": "Em",
            "progression_type": "turkish_folk",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 90,
            "style": "Turkish Folk"
        },
        "Çoban": {
            "key": "Am",
            "progression_type": "turkish_folk",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 85,
            "style": "Turkish Folk"
        },
        
        # Sezen Aksu Songs
        "Gülümse": {
            "key": "F",
            "progression_type": "pop",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 118,
            "style": "Turkish Pop"
        },
        "Kırlarda": {
            "key": "Dm",
            "progression_type": "folk",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 95,
            "style": "Turkish Folk"
        },
        
        # Erkan Oğur Songs
        "Bir Düş": {
            "key": "Cm",
            "progression_type": "jazz",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 75,
            "style": "Turkish Jazz"
        },
        "Gül": {
            "key": "Gm",
            "progression_type": "turkish_folk",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 88,
            "style": "Turkish Folk"
        },
        
        # Müzeyyen Senar Songs
        "Gül Yüzünde": {
            "key": "Bm",
            "progression_type": "turkish_sanat",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 70,
            "style": "Turkish Classical"
        },
        "Sessiz Gemi": {
            "key": "F#m",
            "progression_type": "turkish_sanat",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 65,
            "style": "Turkish Classical"
        },
        
        # Ahmet Kaya Songs
        "Ağlama Bebek": {
            "key": "Em",
            "progression_type": "arabesk",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 80,
            "style": "Arabesk"
        },
        "Kum Gibi": {
            "key": "Am",
            "progression_type": "arabesk",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 85,
            "style": "Arabesk"
        },
        
        # Zeki Müren Songs
        "Gözlerinin İçine": {
            "key": "C",
            "progression_type": "turkish_sanat",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 72,
            "style": "Turkish Classical"
        },
        "Senede Bir Gün": {
            "key": "G",
            "progression_type": "turkish_sanat",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 68,
            "style": "Turkish Classical"
        },
        
        # Additional Songs for variety
        "Yalnız": {
            "key": "Dm",
            "progression_type": "blues",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 92,
            "style": "Turkish Blues"
        },
        "Uzak": {
            "key": "Bm",
            "progression_type": "jazz",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 78,
            "style": "Turkish Jazz"
        },
        "Son": {
            "key": "F#m",
            "progression_type": "turkish_folk",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 87,
            "style": "Turkish Folk"
        },
        "Başka": {
            "key": "Cm",
            "progression_type": "pop",
            "bars": 4,
            "beats_per_bar": 4,
            "tempo": 125,
            "style": "Turkish Pop"
        }
    }
    
    total_chords_created = 0
    
    # Process each song
    for song_title, progression_data in song_progressions.items():
        try:
            # Find the song in the database
            song = Song.objects.filter(title__icontains=song_title).first()
            
            if not song:
                print(f"⚠️  Song not found: {song_title}")
                continue
            
            print(f"🎵 Processing: {song.title} by {song.artist.name}")
            
            # Generate chord progression using music theory engine
            try:
                progression = music_engine.generate_progression(
                    key=progression_data["key"],
                    progression_type=progression_data["progression_type"],
                    bars=progression_data["bars"],
                    beats_per_bar=progression_data["beats_per_bar"]
                )
                
                # Create Chord objects for each chord in the progression
                for chord_data in progression:
                    chord = Chord.objects.create(
                        song=song,
                        chord_name=chord_data["chord_name"],
                        position=chord_data["bar"] * 100 + chord_data["beat"],  # Position as bar*100 + beat
                        bar=chord_data["bar"],
                        beat=chord_data["beat"],
                        duration=chord_data["duration"],
                        roman_numeral=chord_data["roman_numeral"]
                    )
                    total_chords_created += 1
                
                print(f"   ✅ Created {len(progression)} chords for {song.title}")
                
            except Exception as e:
                print(f"   ❌ Error generating progression for {song.title}: {str(e)}")
                # Fallback: create basic chord
                chord = Chord.objects.create(
                    song=song,
                    chord_name=progression_data["key"],
                    position=100,  # Bar 1, Beat 1
                    bar=1,
                    beat=1,
                    duration=4,
                    roman_numeral="I"
                )
                total_chords_created += 1
                print(f"   ⚠️  Created fallback chord for {song.title}")
                
        except Exception as e:
            print(f"❌ Error processing song {song_title}: {str(e)}")
            continue
    
    print(f"\n🎉 Professional chord seeding completed!")
    print(f"📊 Total chords created: {total_chords_created}")
    
    return total_chords_created


if __name__ == "__main__":
    seed_chords_professional()
