#!/usr/bin/env python3
"""
Simple script to fix inconsistent chord data using current model
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Chord
from collections import defaultdict

def fix_chord_data():
    """Fix inconsistent chord data"""
    print("🔧 Fixing chord data integrity issues...")
    
    # Quality mapping for chord name generation
    quality_map = {
        'major': '',
        'minor': 'm',
        'diminished': 'dim',
        'augmented': 'aug',
        'dominant7': '7',
        'major7': 'maj7',
        'minor7': 'm7',
        'minor7b5': 'm7b5',
        'diminished7': 'dim7',
        'sus2': 'sus2',
        'sus4': 'sus4',
        'add9': 'add9',
        '6': '6',
        'minor6': 'm6',
    }
    
    # Step 1: Fix chord names based on root and quality
    print("\n1. Fixing chord names based on root and quality...")
    fixed_names = 0
    
    for chord in Chord.objects.all():
        # Generate correct chord name from root and quality
        quality_suffix = quality_map.get(chord.quality, '')
        correct_chord_name = f"{chord.root}{quality_suffix}"
        
        # Only update if the chord name is incorrect
        if chord.chord_name != correct_chord_name:
            print(f"  Fixing chord ID {chord.id}: '{chord.chord_name}' -> '{correct_chord_name}' (Root: {chord.root}, Quality: {chord.quality})")
            chord.chord_name = correct_chord_name
            chord.save()
            fixed_names += 1
    
    print(f"  ✅ Fixed {fixed_names} chord names")
    
    # Step 2: Fix duplicate timing combinations
    print("\n2. Fixing duplicate timing combinations...")
    
    # Find duplicate timing combinations
    timing_groups = defaultdict(list)
    for chord in Chord.objects.all():
        key = (chord.song_id, chord.measure, chord.beat, chord.sub_beat)
        timing_groups[key].append(chord)
    
    duplicates = {k: v for k, v in timing_groups.items() if len(v) > 1}
    print(f"  Found {len(duplicates)} duplicate timing combinations")
    
    fixed_timing = 0
    for key, chords in duplicates.items():
        song_id, measure, beat, sub_beat = key
        print(f"  Fixing duplicates for Song {song_id}, M{measure}, B{beat}, SB{sub_beat}: {len(chords)} chords")
        
        # Keep the first chord, adjust timing for others
        for i, chord in enumerate(chords[1:], 1):
            # Adjust sub_beat to avoid duplicates
            new_sub_beat = sub_beat + (i * 0.1)
            print(f"    Adjusting chord ID {chord.id}: sub_beat {sub_beat} -> {new_sub_beat}")
            chord.sub_beat = new_sub_beat
            chord.save()
            fixed_timing += 1
    
    print(f"  ✅ Fixed {fixed_timing} timing conflicts")
    
    # Step 3: Show sample of fixed data
    print("\n3. Sample of fixed chord data:")
    for chord in Chord.objects.all()[:10]:
        print(f"  ID {chord.id}: Root={chord.root}, Quality={chord.quality}, Name={chord.chord_name}")
    
    print(f"\n🎉 Data fix complete!")
    print(f"   - Fixed {fixed_names} chord names")
    print(f"   - Fixed {fixed_timing} timing conflicts")

if __name__ == "__main__":
    fix_chord_data()
