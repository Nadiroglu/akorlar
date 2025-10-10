#!/usr/bin/env python
"""
Seed file for the Song model.
Uses update_or_create to ensure data is always fresh and correct.
Run with: python manage.py shell < seeds/seeds_song.py
"""

from api.models import Song, Artist, Genre
from datetime import timedelta

def seed_songs():
    """Seed songs with popular Turkish music."""
    
    print("🎵 Starting song seeding...")

    try:
        # Get existing artists and genres
        baris_manco = Artist.objects.get(name='Barış Manço')
        sezen_aksu = Artist.objects.get(name='Sezen Aksu')
        tarkan = Artist.objects.get(name='Tarkan')
        neset_ertas = Artist.objects.get(name='Neşet Ertaş')
        erkan_ogur = Artist.objects.get(name='Erkan Oğur')
        muzeyyen_senar = Artist.objects.get(name='Müzeyyen Senar')
        ahmet_kaya = Artist.objects.get(name='Ahmet Kaya')
        zeki_muren = Artist.objects.get(name='Zeki Müren')
        
        pop_genre = Genre.objects.get(name='Pop')
        rock_genre = Genre.objects.get(name='Rock')
        folk_genre = Genre.objects.get(name='Türk Halk Müziği')
        sanat_genre = Genre.objects.get(name='Türk Sanat Müziği')
        arabesk_genre = Genre.objects.get(name='Arabesk')
        jazz_genre = Genre.objects.get(name='Jazz')
        blues_genre = Genre.objects.get(name='Blues')
    except (Artist.DoesNotExist, Genre.DoesNotExist) as e:
        print(f"❌ Error: {e}. Please run the artist and genre seeders first.")
        return 0

    songs_data = [
        {
            'title': 'Dağlar Dağlar', 'artist': baris_manco, 'genre': rock_genre,
            'lyrics': 'Dağlar dağlar, dağlar dağlar...', 'difficulty': 'intermediate', 'year': 1970,
            'duration': timedelta(minutes=4, seconds=30), 'key': 'Am', 'tempo': 120,
            'chords_available': True, 'tabs_available': True, 'is_popular': True,
            'play_count': 15000, 'rating': 4.8
        },
        {
            'title': 'Gül Pembe', 'artist': baris_manco, 'genre': rock_genre,
            'lyrics': 'Gül pembe, gül pembe...', 'difficulty': 'beginner', 'year': 1975,
            'duration': timedelta(minutes=3, seconds=45), 'key': 'C', 'tempo': 110,
            'chords_available': True, 'tabs_available': True, 'is_popular': True,
            'play_count': 12000, 'rating': 4.6
        },
        {
            'title': 'Şımarık', 'artist': tarkan, 'genre': pop_genre,
            'lyrics': 'Şımarık, şımarık...', 'difficulty': 'intermediate', 'year': 1997,
            'duration': timedelta(minutes=3, seconds=50), 'key': 'G', 'tempo': 128,
            'chords_available': True, 'tabs_available': False, 'is_popular': True,
            'play_count': 25000, 'rating': 4.9
        },
        {
            'title': 'Kuzu Kuzu', 'artist': tarkan, 'genre': pop_genre, # Corrected artist
            'lyrics': 'Kuzu kuzu, kuzu kuzu...', 'difficulty': 'beginner', 'year': 2001,
            'duration': timedelta(minutes=4, seconds=15), 'key': 'D', 'tempo': 115,
            'chords_available': True, 'tabs_available': True, 'is_popular': True,
            'play_count': 18000, 'rating': 4.7
        },
        {
            'title': 'Neredesin Sen', 'artist': neset_ertas, 'genre': folk_genre,
            'lyrics': 'Neredesin sen, neredesin...', 'difficulty': 'advanced', 'year': 1965,
            'duration': timedelta(minutes=5, seconds=20), 'key': 'Em', 'tempo': 90,
            'chords_available': True, 'tabs_available': False, 'is_popular': True,
            'play_count': 8000, 'rating': 4.5
        },
        {
            'title': 'Gülümse', 'artist': sezen_aksu, 'genre': pop_genre,
            'lyrics': 'Hadi gülümse bulutlar gitsin...', 'difficulty': 'intermediate', 'year': 1991,
            'duration': timedelta(minutes=5, seconds=29), 'key': 'F', 'tempo': 118,
            'chords_available': True, 'tabs_available': True, 'is_popular': True,
            'play_count': 16000, 'rating': 4.8
        },
        {
            'title': 'Kum Gibi', 'artist': ahmet_kaya, 'genre': arabesk_genre,
            'lyrics': 'Martılar ağlardı çöplüklerde...', 'difficulty': 'intermediate', 'year': 1994,
            'duration': timedelta(minutes=4, seconds=35), 'key': 'Am', 'tempo': 85,
            'chords_available': True, 'tabs_available': False, 'is_popular': True,
            'play_count': 11000, 'rating': 4.5
        },
        {
            'title': 'Senede Bir Gün', 'artist': zeki_muren, 'genre': sanat_genre,
            'lyrics': 'Senede bir gün, o da bugün...', 'difficulty': 'advanced', 'year': 1965,
            'duration': timedelta(minutes=4, seconds=55), 'key': 'G', 'tempo': 68,
            'chords_available': True, 'tabs_available': False, 'is_popular': True,
            'play_count': 9000, 'rating': 4.6
        },
    ]
    
    created_count = 0
    updated_count = 0

    for song_data in songs_data:
        # Use update_or_create to keep records fresh.
        # It finds a song by its unique combination of 'title' and 'artist'.
        obj, created = Song.objects.update_or_create(
            title=song_data['title'],
            artist=song_data['artist'],
            defaults={
                'genre': song_data['genre'],
                'lyrics': song_data['lyrics'],
                'difficulty': song_data['difficulty'],
                'year': song_data['year'],
                'duration': song_data['duration'],
                'key': song_data['key'],
                'tempo': song_data['tempo'],
                'chords_available': song_data['chords_available'],
                'tabs_available': song_data['tabs_available'],
                'is_popular': song_data['is_popular'],
                'play_count': song_data['play_count'],
                'rating': song_data['rating']
            }
        )
        if created:
            created_count += 1
            print(f"✅ Created song: {obj.title} - {obj.artist.name}")
        else:
            updated_count += 1
            print(f"🔄 Updated song: {obj.title} - {obj.artist.name}")
    
    print("\n🎉 Song seeding completed!")
    print(f"📊 Total created: {created_count}, Total updated: {updated_count}")
    return created_count

# This check ensures the script can be run directly from the manage.py shell
if __name__ == 'django.core.management.commands.shell':
    seed_songs()
