#!/usr/bin/env python
"""
Professional seed file for the Chord model.
This script is robust, declarative, and ensures data integrity from the start.
Run with: python manage.py shell < seeds/seeds_chord.py
"""

import sys
from decimal import Decimal
from api.models import Chord, Song
from api.utils.music_theory import music_engine

def seed_chords():
    """
    Seeds the database with musically correct chord progressions for all songs.
    This script is declarative and avoids fragile string parsing.
    """
    print("🎼 Starting robust chord seeding...")

    # --- 1. Define Chord Progressions with Structured Data ---
    # This declarative approach eliminates the need for a fragile parser.
    # Format: {'root': str, 'quality': str, 'duration': int_beats}
    song_progressions = {
        'Dağlar Dağlar': {
            'key': 'Am',
            'progression': [
                {'root': 'A', 'quality': 'minor', 'duration': 4}, {'root': 'G', 'quality': 'major', 'duration': 4},
                {'root': 'F', 'quality': 'major', 'duration': 4}, {'root': 'E', 'quality': 'major', 'duration': 4},
            ] * 4 # Repeat the progression 4 times
        },
        'Gül Pembe': {
            'key': 'C',
            'progression': [
                {'root': 'C', 'quality': 'major', 'duration': 4}, {'root': 'A', 'quality': 'minor', 'duration': 4},
                {'root': 'F', 'quality': 'major', 'duration': 4}, {'root': 'G', 'quality': 'major', 'duration': 4},
            ] * 2 + [
                {'root': 'F', 'quality': 'major', 'duration': 4}, {'root': 'G', 'quality': 'major', 'duration': 4},
                {'root': 'C', 'quality': 'major', 'duration': 4}, {'root': 'A', 'quality': 'minor', 'duration': 4},
            ] * 2
        },
        'Şımarık': {
            'key': 'G',
            'progression': [
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'E', 'quality': 'minor', 'duration': 4},
                {'root': 'C', 'quality': 'major', 'duration': 4}, {'root': 'D', 'quality': 'major', 'duration': 4},
            ] * 2 + [
                {'root': 'E', 'quality': 'minor', 'duration': 4}, {'root': 'C', 'quality': 'major', 'duration': 4},
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'D', 'quality': 'major', 'duration': 4},
            ] * 2
        },
        'Kuzu Kuzu': {
            'key': 'D',
            'progression': [
                {'root': 'D', 'quality': 'major', 'duration': 4}, {'root': 'B', 'quality': 'minor', 'duration': 4},
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'A', 'quality': 'major', 'duration': 4},
            ] * 2 + [
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'A', 'quality': 'major', 'duration': 4},
                {'root': 'D', 'quality': 'major', 'duration': 4}, {'root': 'B', 'quality': 'minor', 'duration': 4},
            ] * 2
        },
        'Neredesin Sen': {
            'key': 'Em',
            'progression': [
                {'root': 'E', 'quality': 'minor', 'duration': 4}, {'root': 'A', 'quality': 'minor', 'duration': 4},
                {'root': 'D', 'quality': 'major', 'duration': 4}, {'root': 'G', 'quality': 'major', 'duration': 4},
            ] * 4
        },
        'Hal Hal': {
            'key': 'F',
            'progression': [
                {'root': 'F', 'quality': 'major', 'duration': 4}, {'root': 'D', 'quality': 'minor', 'duration': 4},
                {'root': 'Bb', 'quality': 'major', 'duration': 4}, {'root': 'C', 'quality': 'major', 'duration': 4},
            ] * 4
        },
        'Ben Bilmem': {
            'key': 'Am',
            'progression': [
                {'root': 'Am', 'quality': 'minor', 'duration': 4}, {'root': 'F', 'quality': 'major', 'duration': 4},
                {'root': 'C', 'quality': 'major', 'duration': 4}, {'root': 'G', 'quality': 'major', 'duration': 4},
            ] * 3 + [
                {'root': 'Am', 'quality': 'minor', 'duration': 4}, {'root': 'F', 'quality': 'major', 'duration': 4},
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'Am', 'quality': 'minor', 'duration': 4},
            ]
        },
        'Dönence': {
            'key': 'Dm',
            'progression': [
                {'root': 'Dm', 'quality': 'minor', 'duration': 4}, {'root': 'Bb', 'quality': 'major', 'duration': 4},
                {'root': 'F', 'quality': 'major', 'duration': 4}, {'root': 'C', 'quality': 'major', 'duration': 4},
            ] * 4
        },
        'Sarı Çizmeli Mehmet Ağa': {
            'key': 'G',
            'progression': [
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'D', 'quality': 'major', 'duration': 4},
                {'root': 'Em', 'quality': 'minor', 'duration': 4}, {'root': 'C', 'quality': 'major', 'duration': 4},
            ] * 2 + [
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'Em', 'quality': 'minor', 'duration': 4},
                {'root': 'C', 'quality': 'major', 'duration': 4}, {'root': 'D', 'quality': 'major', 'duration': 4},
            ] * 2
        },
        'Kara Sevda': {
            'key': 'Em',
            'progression': [
                {'root': 'Em', 'quality': 'minor', 'duration': 4}, {'root': 'C', 'quality': 'major', 'duration': 4},
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'D', 'quality': 'major', 'duration': 4},
            ] * 4
        },
        'Yalnızlar Rıhtımı': {
            'key': 'Am',
            'progression': [
                {'root': 'Am', 'quality': 'minor', 'duration': 4}, {'root': 'G', 'quality': 'major', 'duration': 4},
                {'root': 'F', 'quality': 'major', 'duration': 4}, {'root': 'E', 'quality': 'major', 'duration': 4},
            ] * 2 + [
                {'root': 'Am', 'quality': 'minor', 'duration': 4}, {'root': 'F', 'quality': 'major', 'duration': 4},
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'Am', 'quality': 'minor', 'duration': 4},
            ] * 2
        },
        'Gözlerin Doğuyor Gecelerime': {
            'key': 'C',
            'progression': [
                {'root': 'C', 'quality': 'major', 'duration': 4}, {'root': 'Am', 'quality': 'minor', 'duration': 4},
                {'root': 'F', 'quality': 'major', 'duration': 4}, {'root': 'G', 'quality': 'major', 'duration': 4},
            ] * 3 + [
                {'root': 'C', 'quality': 'major', 'duration': 4}, {'root': 'F', 'quality': 'major', 'duration': 4},
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'C', 'quality': 'major', 'duration': 4},
            ]
        },
        'Ayrılık': {
            'key': 'F',
            'progression': [
                {'root': 'F', 'quality': 'major', 'duration': 4}, {'root': 'Dm', 'quality': 'minor', 'duration': 4},
                {'root': 'Bb', 'quality': 'major', 'duration': 4}, {'root': 'C', 'quality': 'major', 'duration': 4},
            ] * 2 + [
                {'root': 'F', 'quality': 'major', 'duration': 4}, {'root': 'Bb', 'quality': 'major', 'duration': 4},
                {'root': 'C', 'quality': 'major', 'duration': 4}, {'root': 'F', 'quality': 'major', 'duration': 4},
            ] * 2
        },
        'Sevda Kuşun Kanadında': {
            'key': 'Gm',
            'progression': [
                {'root': 'Gm', 'quality': 'minor', 'duration': 4}, {'root': 'Eb', 'quality': 'major', 'duration': 4},
                {'root': 'Bb', 'quality': 'major', 'duration': 4}, {'root': 'F', 'quality': 'major', 'duration': 4},
            ] * 4
        },
        'İstanbul Hatırası': {
            'key': 'D',
            'progression': [
                {'root': 'D', 'quality': 'major', 'duration': 4}, {'root': 'Bm', 'quality': 'minor', 'duration': 4},
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'A', 'quality': 'major', 'duration': 4},
            ] * 2 + [
                {'root': 'D', 'quality': 'major', 'duration': 4}, {'root': 'G', 'quality': 'major', 'duration': 4},
                {'root': 'A', 'quality': 'major', 'duration': 4}, {'root': 'D', 'quality': 'major', 'duration': 4},
            ] * 2
        },
        'Yıldızların Altında': {
            'key': 'Em',
            'progression': [
                {'root': 'Em', 'quality': 'minor', 'duration': 4}, {'root': 'Am', 'quality': 'minor', 'duration': 4},
                {'root': 'C', 'quality': 'major', 'duration': 4}, {'root': 'G', 'quality': 'major', 'duration': 4},
            ] * 3 + [
                {'root': 'Em', 'quality': 'minor', 'duration': 4}, {'root': 'C', 'quality': 'major', 'duration': 4},
                {'root': 'G', 'quality': 'major', 'duration': 4}, {'root': 'Em', 'quality': 'minor', 'duration': 4},
            ]
        }
    }

    # --- 2. Fetch Songs ---
    try:
        songs = {song.title: song for song in Song.objects.all()}
    except Exception as e:
        print(f"❌ Error fetching songs: {e}")
        return 0

    # --- 3. Process and Create Chords ---
    created_count = 0
    skipped_count = 0
    
    # Ensure idempotency by deleting old chords for the songs we are about to seed
    songs_to_seed = [s for s in song_progressions if s in songs]
    song_pks_to_seed = [songs[title].pk for title in songs_to_seed]
    Chord.objects.filter(song_id__in=song_pks_to_seed).delete()
    print(f"🧹 Cleared old chords for {len(song_pks_to_seed)} songs to be seeded.")

    for song_title, data in song_progressions.items():
        if song_title in songs:
            song_object = songs[song_title]
            key = data['key']
            progression = data['progression']
            
            print(f"🎵 Processing '{song_title}' (Key: {key})...")
            
            # Use a simple beat counter for robust timing
            total_beats_processed = 0
            chords_to_create = []

            for chord_data in progression:
                measure = (total_beats_processed // 4) + 1
                beat = (total_beats_processed % 4) + 1
                
                # Calculate Roman numeral using the robust engine
                try:
                    numeral_info = music_engine.get_roman_numeral(
                        key=key,
                        chord_root=chord_data['root'],
                        chord_quality=chord_data['quality']
                    )
                    roman_numeral = numeral_info['roman_numeral']
                except ValueError:
                    roman_numeral = '' # This chord is not diatonic to the key

                chord_instance = Chord(
                    song=song_object,
                    measure=measure,
                    beat=Decimal(beat),
                    sub_beat=Decimal('0.00'),
                    root=chord_data['root'],
                    quality=chord_data['quality'],
                    extensions=chord_data.get('extensions', ''),
                    duration_in_beats=Decimal(chord_data['duration']),
                    key_context=key,
                    roman_numeral=roman_numeral
                )
                chords_to_create.append(chord_instance)
                
                total_beats_processed += chord_data['duration']

            # Use bulk_create for high performance
            Chord.objects.bulk_create(chords_to_create)
            created_count += len(chords_to_create)
            print(f"   ✅ Created {len(chords_to_create)} chords for '{song_title}'.")
        else:
            print(f"⚠️  Song '{song_title}' not found in database, skipping.")
            skipped_count += 1
            
    print("\n🎉 Chord seeding completed!")
    print(f"📊 Total chords created: {created_count}")
    print(f"🎵 Songs processed: {len(song_progressions) - skipped_count}")
    print(f"🚫 Songs skipped: {skipped_count}")

    return created_count

# This allows the script to be run directly from the shell
if __name__ == 'django.core.management.commands.shell':
    seed_chords()