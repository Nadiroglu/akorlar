#!/usr/bin/env python3
"""
Demonstration script showing how song creation with chords works in Akorlar
This script shows the complete workflow from song creation to chord addition
"""

import requests
import json
import time
from urllib.parse import urljoin

BASE_URL = "http://localhost:8000"

def create_demo_song():
    """Create a demo song to show the workflow"""
    print("🎵 Creating Demo Song")
    print("=" * 40)
    
    # Song data
    song_data = {
        "title": "Demo Song - C Major Progression",
        "artist": 1,  # Assuming artist with ID 1 exists
        "genre": 1,   # Assuming genre with ID 1 exists
        "key": "C",
        "difficulty": "beginner",
        "year": 2024,
        "lyrics": "This is a demo song to show chord progression...",
        "chords_available": True,
        "tabs_available": False,
        "is_popular": False,
        "time_signature": "4/4",
        "duration": "02:30"
    }
    
    # Create song
    response = requests.post(
        f"{BASE_URL}/api/admin/songs/",
        json=song_data,
        auth=('admin', 'admin123')
    )
    
    if response.status_code == 201:
        song = response.json()
        print(f"✅ Song created: {song['title']} (ID: {song['id']})")
        return song['id']
    else:
        print(f"❌ Failed to create song: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def add_chords_to_song(song_id):
    """Add chords to the demo song"""
    print(f"\n🎼 Adding Chords to Song {song_id}")
    print("=" * 40)
    
    # Chord progression: C - Am - F - G (I - vi - IV - V)
    chord_progression = [
        {
            "song": song_id,
            "root": "C",
            "quality": "major",
            "inversion": "root",
            "measure": 1,
            "beat": 1.0,
            "sub_beat": 0.0,
            "duration_in_beats": 4.0,
            "key_context": "C major",
            "roman_numeral": "I"
        },
        {
            "song": song_id,
            "root": "A",
            "quality": "minor",
            "inversion": "root",
            "measure": 1,
            "beat": 5.0,
            "sub_beat": 0.0,
            "duration_in_beats": 4.0,
            "key_context": "C major",
            "roman_numeral": "vi"
        },
        {
            "song": song_id,
            "root": "F",
            "quality": "major",
            "inversion": "root",
            "measure": 2,
            "beat": 1.0,
            "sub_beat": 0.0,
            "duration_in_beats": 4.0,
            "key_context": "C major",
            "roman_numeral": "IV"
        },
        {
            "song": song_id,
            "root": "G",
            "quality": "major",
            "inversion": "root",
            "measure": 2,
            "beat": 5.0,
            "sub_beat": 0.0,
            "duration_in_beats": 4.0,
            "key_context": "C major",
            "roman_numeral": "V"
        }
    ]
    
    created_chords = []
    
    for i, chord_data in enumerate(chord_progression, 1):
        print(f"Adding chord {i}/4: {chord_data['root']}{chord_data['quality']}")
        
        response = requests.post(
            f"{BASE_URL}/api/admin/chords/",
            json=chord_data,
            auth=('admin', 'admin123')
        )
        
        if response.status_code == 201:
            chord = response.json()
            created_chords.append(chord)
            print(f"  ✅ {chord['chord_name']} (M{chord['measure']}, B{chord['beat']})")
        else:
            print(f"  ❌ Failed: {response.status_code} - {response.text}")
    
    return created_chords

def demonstrate_chord_retrieval(song_id):
    """Show how to retrieve song with chords"""
    print(f"\n🔍 Retrieving Song {song_id} with Chords")
    print("=" * 40)
    
    # Get song with chords
    response = requests.get(f"{BASE_URL}/api/songs/{song_id}/")
    
    if response.status_code == 200:
        song = response.json()
        print(f"Song: {song['title']}")
        print(f"Key: {song['key']}")
        print(f"Time Signature: {song['time_signature']}")
        print(f"Chords Available: {song['chords_available']}")
        print(f"\nChord Progression:")
        
        for chord in song['chords']:
            print(f"  {chord['chord_name']} (M{chord['measure']}, B{chord['beat']}) - {chord['roman_numeral']}")
        
        return song
    else:
        print(f"❌ Failed to retrieve song: {response.status_code}")
        return None

def demonstrate_chord_filtering(song_id):
    """Show chord filtering capabilities"""
    print(f"\n🎯 Chord Filtering Examples")
    print("=" * 40)
    
    # Filter by root note
    print("Chords with root C:")
    response = requests.get(f"{BASE_URL}/api/chords/?song={song_id}&root=C")
    if response.status_code == 200:
        chords = response.json()
        for chord in chords:
            print(f"  {chord['chord_name']} - {chord['roman_numeral']}")
    
    # Filter by measure
    print("\nChords in measure 1:")
    response = requests.get(f"{BASE_URL}/api/chords/?song={song_id}&measure=1")
    if response.status_code == 200:
        chords = response.json()
        for chord in chords:
            print(f"  {chord['chord_name']} (Beat {chord['beat']})")
    
    # Filter by quality
    print("\nMajor chords:")
    response = requests.get(f"{BASE_URL}/api/chords/?song={song_id}&quality=major")
    if response.status_code == 200:
        chords = response.json()
        for chord in chords:
            print(f"  {chord['chord_name']} - {chord['roman_numeral']}")

def demonstrate_transposition(song_id):
    """Show chord transposition capability"""
    print(f"\n🎹 Chord Transposition Example")
    print("=" * 40)
    
    # Get chords for the song
    response = requests.get(f"{BASE_URL}/api/chords/?song={song_id}")
    if response.status_code == 200:
        chords = response.json()
        
        print("Original progression in C:")
        for chord in chords:
            print(f"  {chord['chord_name']}", end=" ")
        print()
        
        print("\nTransposed to G (up 5 semitones):")
        for chord in chords:
            # Simulate transposition (in real app, this would use the transpose method)
            root_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            try:
                current_index = root_notes.index(chord['root'])
                new_index = (current_index + 5) % 12
                transposed_root = root_notes[new_index]
                print(f"  {transposed_root}{chord['quality']}", end=" ")
            except ValueError:
                print(f"  {chord['chord_name']}", end=" ")
        print()

def cleanup_demo_data(song_id):
    """Clean up demo data"""
    print(f"\n🧹 Cleaning Up Demo Data")
    print("=" * 40)
    
    # Delete the demo song (this will cascade delete chords)
    response = requests.delete(
        f"{BASE_URL}/api/admin/songs/{song_id}/",
        auth=('admin', 'admin123')
    )
    
    if response.status_code == 204:
        print(f"✅ Demo song {song_id} deleted")
    else:
        print(f"⚠️  Could not delete demo song: {response.status_code}")

def main():
    """Main demonstration function"""
    print("🎵 Akorlar Song Creation with Chords Demo")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Backend server not running. Start with 'python manage.py runserver'")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running. Start with 'python manage.py runserver'")
        return
    
    print("✅ Backend server is running")
    
    # Step 1: Create song
    song_id = create_demo_song()
    if not song_id:
        return
    
    # Step 2: Add chords
    chords = add_chords_to_song(song_id)
    if not chords:
        print("❌ No chords were created")
        return
    
    # Step 3: Demonstrate retrieval
    song = demonstrate_chord_retrieval(song_id)
    if not song:
        return
    
    # Step 4: Demonstrate filtering
    demonstrate_chord_filtering(song_id)
    
    # Step 5: Demonstrate transposition
    demonstrate_transposition(song_id)
    
    # Step 6: Cleanup
    cleanup_choice = input("\nDelete demo data? (y/N): ").lower()
    if cleanup_choice == 'y':
        cleanup_demo_data(song_id)
    else:
        print(f"Demo song {song_id} kept for further testing")
    
    print("\n🎉 Demo completed!")
    print("\nKey takeaways:")
    print("1. Songs are created first with basic metadata")
    print("2. Chords are added individually with precise timing")
    print("3. The system automatically generates chord names")
    print("4. Chords are ordered by musical timing")
    print("5. Advanced filtering and transposition are available")

if __name__ == "__main__":
    main()




