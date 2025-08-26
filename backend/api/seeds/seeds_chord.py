#!/usr/bin/env python
"""
Comprehensive seed file for Chord model
Creates chord progressions for all songs with proper musical structure
Run with: python manage.py shell < seeds_chord.py
"""

from api.models import Chord, Song
from decimal import Decimal

def seed_chords():
    """Seed chords with comprehensive chord progressions for all songs"""
    
    print("🎼 Starting chord seeding...")
    
    # Get all existing songs
    try:
        songs = {
            'Dağlar Dağlar': Song.objects.get(title='Dağlar Dağlar'),
            'Gül Pembe': Song.objects.get(title='Gül Pembe'),
            'Şımarık': Song.objects.get(title='Şımarık'),
            'Kuzu Kuzu': Song.objects.get(title='Kuzu Kuzu'),
            'Neredesin Sen': Song.objects.get(title='Neredesin Sen'),
            'Kiss Kiss': Song.objects.get(title='Kiss Kiss'),
            'Gül Pembe (Ajda)': Song.objects.get(title='Gül Pembe', artist__name='Ajda Pekkan'),
            'Çağrı': Song.objects.get(title='Çağrı'),
            'Beni Affet': Song.objects.get(title='Beni Affet'),
            'Yar Gurbette': Song.objects.get(title='Yar Gurbette'),
            'Batsın Bu Dünya': Song.objects.get(title='Batsın Bu Dünya'),
            'Gitme': Song.objects.get(title='Gitme'),
            'Yanarım': Song.objects.get(title='Yanarım'),
            'Everyway That I Can': Song.objects.get(title='Everyway That I Can'),
            'Holigan': Song.objects.get(title='Holigan'),
            'Seni Kendime Sakladım': Song.objects.get(title='Seni Kendime Sakladım'),
            'Cennet': Song.objects.get(title='Cennet'),
            'Vazgeçtim': Song.objects.get(title='Vazgeçtim'),
            'Sensiz Olmuyor': Song.objects.get(title='Sensiz Olmuyor')
        }
    except Song.DoesNotExist as e:
        print(f"❌ Error: {e}")
        print("Please run the song seeds first!")
        return 0
    
    # Define chord progressions for each song
    song_progressions = {
        'Dağlar Dağlar': {
            'key': 'Am',
            'progression': [
                ('Am', 4), ('G', 4), ('F', 4), ('E', 4),  # Verse 1
                ('Am', 4), ('G', 4), ('F', 4), ('E', 4),  # Verse 2
                ('Am', 4), ('G', 4), ('F', 4), ('E', 4),  # Chorus
                ('Am', 4), ('G', 4), ('F', 4), ('E', 4),  # Chorus repeat
            ]
        },
        'Gül Pembe': {
            'key': 'C',
            'progression': [
                ('C', 4), ('Am', 4), ('F', 4), ('G', 4),  # Verse 1
                ('C', 4), ('Am', 4), ('F', 4), ('G', 4),  # Verse 2
                ('F', 4), ('G', 4), ('C', 4), ('Am', 4),  # Chorus
                ('F', 4), ('G', 4), ('C', 4), ('Am', 4),  # Chorus repeat
            ]
        },
        'Şımarık': {
            'key': 'G',
            'progression': [
                ('G', 4), ('Em', 4), ('C', 4), ('D', 4),  # Verse 1
                ('G', 4), ('Em', 4), ('C', 4), ('D', 4),  # Verse 2
                ('Em', 4), ('C', 4), ('G', 4), ('D', 4),  # Chorus
                ('Em', 4), ('C', 4), ('G', 4), ('D', 4),  # Chorus repeat
            ]
        },
        'Kuzu Kuzu': {
            'key': 'D',
            'progression': [
                ('D', 4), ('Bm', 4), ('G', 4), ('A', 4),  # Verse 1
                ('D', 4), ('Bm', 4), ('G', 4), ('A', 4),  # Verse 2
                ('G', 4), ('A', 4), ('D', 4), ('Bm', 4),  # Chorus
                ('G', 4), ('A', 4), ('D', 4), ('Bm', 4),  # Chorus repeat
            ]
        },
        'Neredesin Sen': {
            'key': 'Em',
            'progression': [
                ('Em', 4), ('Am', 4), ('D', 4), ('G', 4),  # Verse 1
                ('Em', 4), ('Am', 4), ('D', 4), ('G', 4),  # Verse 2
                ('Am', 4), ('D', 4), ('Em', 4), ('G', 4),  # Chorus
                ('Am', 4), ('D', 4), ('Em', 4), ('G', 4),  # Chorus repeat
            ]
        },
        'Kiss Kiss': {
            'key': 'F',
            'progression': [
                ('F', 4), ('Dm', 4), ('Bb', 4), ('C', 4),  # Verse 1
                ('F', 4), ('Dm', 4), ('Bb', 4), ('C', 4),  # Verse 2
                ('Dm', 4), ('Bb', 4), ('F', 4), ('C', 4),  # Chorus
                ('Dm', 4), ('Bb', 4), ('F', 4), ('C', 4),  # Chorus repeat
            ]
        },
        'Gül Pembe (Ajda)': {
            'key': 'C',
            'progression': [
                ('C', 4), ('Am', 4), ('F', 4), ('G', 4),  # Verse 1
                ('C', 4), ('Am', 4), ('F', 4), ('G', 4),  # Verse 2
                ('F', 4), ('G', 4), ('C', 4), ('Am', 4),  # Chorus
                ('F', 4), ('G', 4), ('C', 4), ('Am', 4),  # Chorus repeat
            ]
        },
        'Çağrı': {
            'key': 'Am',
            'progression': [
                ('Am', 4), ('F', 4), ('C', 4), ('G', 4),  # Verse 1
                ('Am', 4), ('F', 4), ('C', 4), ('G', 4),  # Verse 2
                ('F', 4), ('C', 4), ('Am', 4), ('G', 4),  # Chorus
                ('F', 4), ('C', 4), ('Am', 4), ('G', 4),  # Chorus repeat
            ]
        },
        'Beni Affet': {
            'key': 'Dm',
            'progression': [
                ('Dm', 4), ('Bb', 4), ('F', 4), ('C', 4),  # Verse 1
                ('Dm', 4), ('Bb', 4), ('F', 4), ('C', 4),  # Verse 2
                ('Bb', 4), ('F', 4), ('Dm', 4), ('C', 4),  # Chorus
                ('Bb', 4), ('F', 4), ('Dm', 4), ('C', 4),  # Chorus repeat
            ]
        },
        'Yar Gurbette': {
            'key': 'Em',
            'progression': [
                ('Em', 4), ('Am', 4), ('D', 4), ('G', 4),  # Verse 1
                ('Em', 4), ('Am', 4), ('D', 4), ('G', 4),  # Verse 2
                ('Am', 4), ('D', 4), ('Em', 4), ('G', 4),  # Chorus
                ('Am', 4), ('D', 4), ('Em', 4), ('G', 4),  # Chorus repeat
            ]
        },
        'Batsın Bu Dünya': {
            'key': 'Am',
            'progression': [
                ('Am', 4), ('G', 4), ('F', 4), ('E', 4),  # Verse 1
                ('Am', 4), ('G', 4), ('F', 4), ('E', 4),  # Verse 2
                ('G', 4), ('F', 4), ('Am', 4), ('E', 4),  # Chorus
                ('G', 4), ('F', 4), ('Am', 4), ('E', 4),  # Chorus repeat
            ]
        },
        'Gitme': {
            'key': 'Dm',
            'progression': [
                ('Dm', 4), ('Bb', 4), ('F', 4), ('C', 4),  # Verse 1
                ('Dm', 4), ('Bb', 4), ('F', 4), ('C', 4),  # Verse 2
                ('Bb', 4), ('F', 4), ('Dm', 4), ('C', 4),  # Chorus
                ('Bb', 4), ('F', 4), ('Dm', 4), ('C', 4),  # Chorus repeat
            ]
        },
        'Yanarım': {
            'key': 'G',
            'progression': [
                ('G', 4), ('Em', 4), ('C', 4), ('D', 4),  # Verse 1
                ('G', 4), ('Em', 4), ('C', 4), ('D', 4),  # Verse 2
                ('Em', 4), ('C', 4), ('G', 4), ('D', 4),  # Chorus
                ('Em', 4), ('C', 4), ('G', 4), ('D', 4),  # Chorus repeat
            ]
        },
        'Everyway That I Can': {
            'key': 'C',
            'progression': [
                ('C', 4), ('Am', 4), ('F', 4), ('G', 4),  # Verse 1
                ('C', 4), ('Am', 4), ('F', 4), ('G', 4),  # Verse 2
                ('F', 4), ('G', 4), ('C', 4), ('Am', 4),  # Chorus
                ('F', 4), ('G', 4), ('C', 4), ('Am', 4),  # Chorus repeat
            ]
        },
        'Holigan': {
            'key': 'E',
            'progression': [
                ('E', 2), ('G', 2), ('A', 2), ('B', 2),   # Fast progression
                ('E', 2), ('G', 2), ('A', 2), ('B', 2),   # Fast progression
                ('E', 2), ('G', 2), ('A', 2), ('B', 2),   # Fast progression
                ('E', 2), ('G', 2), ('A', 2), ('B', 2),   # Fast progression
            ]
        },
        'Seni Kendime Sakladım': {
            'key': 'Am',
            'progression': [
                ('Am', 4), ('F', 4), ('C', 4), ('G', 4),  # Verse 1
                ('Am', 4), ('F', 4), ('C', 4), ('G', 4),  # Verse 2
                ('F', 4), ('C', 4), ('Am', 4), ('G', 4),  # Chorus
                ('F', 4), ('C', 4), ('Am', 4), ('G', 4),  # Chorus repeat
            ]
        },
        'Cennet': {
            'key': 'G',
            'progression': [
                ('G', 4), ('Em', 4), ('C', 4), ('D', 4),  # Verse 1
                ('G', 4), ('Em', 4), ('C', 4), ('D', 4),  # Verse 2
                ('Em', 4), ('C', 4), ('G', 4), ('D', 4),  # Chorus
                ('Em', 4), ('C', 4), ('G', 4), ('D', 4),  # Chorus repeat
            ]
        },
        'Vazgeçtim': {
            'key': 'Dm',
            'progression': [
                ('Dm', 4), ('Bb', 4), ('F', 4), ('C', 4),  # Verse 1
                ('Dm', 4), ('Bb', 4), ('F', 4), ('C', 4),  # Verse 2
                ('Bb', 4), ('F', 4), ('Dm', 4), ('C', 4),  # Chorus
                ('Bb', 4), ('F', 4), ('Dm', 4), ('C', 4),  # Chorus repeat
            ]
        },
        'Sensiz Olmuyor': {
            'key': 'Em',
            'progression': [
                ('Em', 4), ('Am', 4), ('D', 4), ('G', 4),  # Verse 1
                ('Em', 4), ('Am', 4), ('D', 4), ('G', 4),  # Verse 2
                ('Am', 4), ('D', 4), ('Em', 4), ('G', 4),  # Chorus
                ('Am', 4), ('D', 4), ('Em', 4), ('G', 4),  # Chorus repeat
            ]
        }
    }
    
    created_count = 0
    total_chords = 0
    
    for song_title, song_data in song_progressions.items():
        if song_title in songs:
            song = songs[song_title]
            progression = song_data['progression']
            key = song_data['key']
            
            print(f"🎵 Creating chords for '{song_title}' (Key: {key})...")
            
            # Clear existing chords for this song
            Chord.objects.filter(song=song).delete()
            
            position = 1
            bar = 1
            
            for chord_name, duration in progression:
                chord = Chord.objects.create(
                    song=song,
                    chord_name=chord_name,
                    position=position,
                    bar=bar,
                    beat=1,
                    duration=Decimal(str(duration))
                )
                created_count += 1
                position += 1
                
                # Move to next bar if duration is 4 beats
                if duration == 4:
                    bar += 1
                elif duration == 2:
                    # For 2-beat chords, we might need to handle differently
                    if position % 2 == 1:  # Every 2nd chord
                        bar += 1
            
            total_chords += len(progression)
            print(f"   ✅ Created {len(progression)} chords for {song_title}")
        else:
            print(f"⚠️  Song '{song_title}' not found, skipping...")
    
    print(f"\n🎉 Chord seeding completed!")
    print(f"📊 Total chords created: {created_count}")
    print(f"🎵 Total songs processed: {len([s for s in song_progressions.keys() if s in songs])}")
    
    return created_count

if __name__ == "__main__":
    seed_chords()
