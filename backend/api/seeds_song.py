#!/usr/bin/env python
"""
Seed file for Song model
Run with: python manage.py shell < seeds_song.py
"""

from api.models import Song, Artist, Genre
from datetime import timedelta

def seed_songs():
    """Seed songs with popular Turkish music"""
    
    # Get existing artists and genres
    baris_manco = Artist.objects.get(name='Barış Manço')
    sezen_aksu = Artist.objects.get(name='Sezen Aksu')
    tarkan = Artist.objects.get(name='Tarkan')
    neset_ertas = Artist.objects.get(name='Neşet Ertaş')
    
    pop_genre = Genre.objects.get(name='Pop')
    rock_genre = Genre.objects.get(name='Rock')
    folk_genre = Genre.objects.get(name='Türk Halk Müziği')
    
    songs_data = [
        {
            'title': 'Dağlar Dağlar',
            'artist': baris_manco,
            'genre': rock_genre,
            'lyrics': 'Dağlar dağlar, dağlar dağlar...',
            'difficulty': 'intermediate',
            'year': 1970,
            'duration': timedelta(minutes=4, seconds=30),
            'key': 'Am',
            'tempo': 120,
            'chords_available': True,
            'tabs_available': True,
            'is_popular': True,
            'play_count': 15000,
            'rating': 4.8
        },
        {
            'title': 'Gül Pembe',
            'artist': baris_manco,
            'genre': rock_genre,
            'lyrics': 'Gül pembe, gül pembe...',
            'difficulty': 'beginner',
            'year': 1975,
            'duration': timedelta(minutes=3, seconds=45),
            'key': 'C',
            'tempo': 110,
            'chords_available': True,
            'tabs_available': True,
            'is_popular': True,
            'play_count': 12000,
            'rating': 4.6
        },
        {
            'title': 'Şımarık',
            'artist': tarkan,
            'genre': pop_genre,
            'lyrics': 'Şımarık, şımarık...',
            'difficulty': 'intermediate',
            'year': 1997,
            'duration': timedelta(minutes=3, seconds=50),
            'key': 'G',
            'tempo': 128,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': True,
            'play_count': 25000,
            'rating': 4.9
        },
        {
            'title': 'Kuzu Kuzu',
            'artist': sezen_aksu,
            'genre': pop_genre,
            'lyrics': 'Kuzu kuzu, kuzu kuzu...',
            'difficulty': 'beginner',
            'year': 1993,
            'duration': timedelta(minutes=4, seconds=15),
            'key': 'D',
            'tempo': 115,
            'chords_available': True,
            'tabs_available': True,
            'is_popular': True,
            'play_count': 18000,
            'rating': 4.7
        },
        {
            'title': 'Neredesin Sen',
            'artist': neset_ertas,
            'genre': folk_genre,
            'lyrics': 'Neredesin sen, neredesin...',
            'difficulty': 'advanced',
            'year': 1965,
            'duration': timedelta(minutes=5, seconds=20),
            'key': 'Em',
            'tempo': 90,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': True,
            'play_count': 8000,
            'rating': 4.5
        },
        {
            'title': 'Çoban',
            'artist': neset_ertas,
            'genre': folk_genre,
            'lyrics': 'Çoban, çoban...',
            'difficulty': 'intermediate',
            'year': 1970,
            'duration': timedelta(minutes=4, seconds=10),
            'key': 'Am',
            'tempo': 95,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': False,
            'play_count': 5000,
            'rating': 4.3
        }
    ]
    
    created_count = 0
    for song_data in songs_data:
        song, created = Song.objects.get_or_create(
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
            print(f"Created song: {song.title} - {song.artist.name}")
        else:
            print(f"Song already exists: {song.title} - {song.artist.name}")
    
    print(f"\nTotal songs created: {created_count}")
    return created_count

if __name__ == "__main__":
    seed_songs()
