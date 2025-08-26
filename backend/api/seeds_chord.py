#!/usr/bin/env python
"""
Seed file for Chord model
Run with: python manage.py shell < seeds_chord.py
"""

from api.models import Chord, Song
from decimal import Decimal

def seed_chords():
    """Seed chords with chord progressions for songs"""
    
    # Get existing songs
    daglar_daglar = Song.objects.get(title='Dağlar Dağlar')
    gul_pembe = Song.objects.get(title='Gül Pembe')
    simarik = Song.objects.get(title='Şımarık')
    
    chords_data = [
        # Dağlar Dağlar - Am key
        {
            'song': daglar_daglar,
            'chord_name': 'Am',
            'position': 1,
            'bar': 1,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        {
            'song': daglar_daglar,
            'chord_name': 'F',
            'position': 2,
            'bar': 2,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        {
            'song': daglar_daglar,
            'chord_name': 'C',
            'position': 3,
            'bar': 3,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        {
            'song': daglar_daglar,
            'chord_name': 'G',
            'position': 4,
            'bar': 4,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        
        # Gül Pembe - C key
        {
            'song': gul_pembe,
            'chord_name': 'C',
            'position': 1,
            'bar': 1,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        {
            'song': gul_pembe,
            'chord_name': 'Am',
            'position': 2,
            'bar': 2,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        {
            'song': gul_pembe,
            'chord_name': 'F',
            'position': 3,
            'bar': 3,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        {
            'song': gul_pembe,
            'chord_name': 'G',
            'position': 4,
            'bar': 4,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        
        # Şımarık - G key
        {
            'song': simarik,
            'chord_name': 'G',
            'position': 1,
            'bar': 1,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        {
            'song': simarik,
            'chord_name': 'Em',
            'position': 2,
            'bar': 2,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        {
            'song': simarik,
            'chord_name': 'C',
            'position': 3,
            'bar': 3,
            'beat': 1,
            'duration': Decimal('4.0')
        },
        {
            'song': simarik,
            'chord_name': 'D',
            'position': 4,
            'bar': 4,
            'beat': 1,
            'duration': Decimal('4.0')
        }
    ]
    
    created_count = 0
    for chord_data in chords_data:
        chord, created = Chord.objects.get_or_create(
            song=chord_data['song'],
            position=chord_data['position'],
            bar=chord_data['bar'],
            beat=chord_data['beat'],
            defaults={
                'chord_name': chord_data['chord_name'],
                'duration': chord_data['duration']
            }
        )
        if created:
            created_count += 1
            print(f"Created chord: {chord.chord_name} for {chord.song.title}")
        else:
            print(f"Chord already exists: {chord.chord_name} for {chord.song.title}")
    
    print(f"\nTotal chords created: {created_count}")
    return created_count

if __name__ == "__main__":
    seed_chords()
