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
        },
        # Sezen Aksu Songs
        {
            'title': 'Gülümse',
            'artist': sezen_aksu,
            'genre': pop_genre,
            'lyrics': 'Gülümse, gülümse...',
            'difficulty': 'intermediate',
            'year': 1995,
            'duration': timedelta(minutes=3, seconds=55),
            'key': 'F',
            'tempo': 118,
            'chords_available': True,
            'tabs_available': True,
            'is_popular': True,
            'play_count': 16000,
            'rating': 4.6
        },
        {
            'title': 'Kırlarda',
            'artist': sezen_aksu,
            'genre': folk_genre,
            'lyrics': 'Kırlarda, kırlarda...',
            'difficulty': 'intermediate',
            'year': 1998,
            'duration': timedelta(minutes=4, seconds=25),
            'key': 'Dm',
            'tempo': 95,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': False,
            'play_count': 7000,
            'rating': 4.4
        },
        # Erkan Oğur Songs
        {
            'title': 'Bir Düş',
            'artist': erkan_ogur,
            'genre': jazz_genre,
            'lyrics': 'Bir düş, bir düş...',
            'difficulty': 'advanced',
            'year': 2000,
            'duration': timedelta(minutes=6, seconds=15),
            'key': 'Cm',
            'tempo': 75,
            'chords_available': True,
            'tabs_available': True,
            'is_popular': False,
            'play_count': 3000,
            'rating': 4.7
        },
        {
            'title': 'Gül',
            'artist': erkan_ogur,
            'genre': folk_genre,
            'lyrics': 'Gül, gül...',
            'difficulty': 'intermediate',
            'year': 1995,
            'duration': timedelta(minutes=4, seconds=45),
            'key': 'Gm',
            'tempo': 88,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': False,
            'play_count': 4000,
            'rating': 4.5
        },
        # Müzeyyen Senar Songs
        {
            'title': 'Gül Yüzünde',
            'artist': muzeyyen_senar,
            'genre': sanat_genre,
            'lyrics': 'Gül yüzünde, gül yüzünde...',
            'difficulty': 'advanced',
            'year': 1950,
            'duration': timedelta(minutes=5, seconds=30),
            'key': 'Bm',
            'tempo': 70,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': True,
            'play_count': 12000,
            'rating': 4.8
        },
        {
            'title': 'Sessiz Gemi',
            'artist': muzeyyen_senar,
            'genre': sanat_genre,
            'lyrics': 'Sessiz gemi, sessiz gemi...',
            'difficulty': 'advanced',
            'year': 1955,
            'duration': timedelta(minutes=6, seconds=45),
            'key': 'F#m',
            'tempo': 65,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': True,
            'play_count': 10000,
            'rating': 4.7
        },
        # Ahmet Kaya Songs
        {
            'title': 'Ağlama Bebek',
            'artist': ahmet_kaya,
            'genre': arabesk_genre,
            'lyrics': 'Ağlama bebek, ağlama...',
            'difficulty': 'intermediate',
            'year': 1985,
            'duration': timedelta(minutes=4, seconds=20),
            'key': 'Em',
            'tempo': 80,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': True,
            'play_count': 14000,
            'rating': 4.6
        },
        {
            'title': 'Kum Gibi',
            'artist': ahmet_kaya,
            'genre': arabesk_genre,
            'lyrics': 'Kum gibi, kum gibi...',
            'difficulty': 'intermediate',
            'year': 1988,
            'duration': timedelta(minutes=4, seconds=35),
            'key': 'Am',
            'tempo': 85,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': True,
            'play_count': 11000,
            'rating': 4.5
        },
        # Zeki Müren Songs
        {
            'title': 'Gözlerinin İçine',
            'artist': zeki_muren,
            'genre': sanat_genre,
            'lyrics': 'Gözlerinin içine, gözlerinin içine...',
            'difficulty': 'advanced',
            'year': 1960,
            'duration': timedelta(minutes=5, seconds=15),
            'key': 'C',
            'tempo': 72,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': True,
            'play_count': 13000,
            'rating': 4.7
        },
        {
            'title': 'Senede Bir Gün',
            'artist': zeki_muren,
            'genre': sanat_genre,
            'lyrics': 'Senede bir gün, senede bir gün...',
            'difficulty': 'advanced',
            'year': 1965,
            'duration': timedelta(minutes=4, seconds=55),
            'key': 'G',
            'tempo': 68,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': True,
            'play_count': 9000,
            'rating': 4.6
        },
        # Additional Songs for variety
        {
            'title': 'Yalnız',
            'artist': sezen_aksu,
            'genre': blues_genre,
            'lyrics': 'Yalnız, yalnız...',
            'difficulty': 'intermediate',
            'year': 2000,
            'duration': timedelta(minutes=4, seconds=10),
            'key': 'Dm',
            'tempo': 92,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': False,
            'play_count': 6000,
            'rating': 4.4
        },
        {
            'title': 'Uzak',
            'artist': erkan_ogur,
            'genre': jazz_genre,
            'lyrics': 'Uzak, uzak...',
            'difficulty': 'advanced',
            'year': 2005,
            'duration': timedelta(minutes=7, seconds=20),
            'key': 'Bm',
            'tempo': 78,
            'chords_available': True,
            'tabs_available': True,
            'is_popular': False,
            'play_count': 2500,
            'rating': 4.6
        },
        {
            'title': 'Son',
            'artist': neset_ertas,
            'genre': folk_genre,
            'lyrics': 'Son, son...',
            'difficulty': 'intermediate',
            'year': 1975,
            'duration': timedelta(minutes=4, seconds=15),
            'key': 'F#m',
            'tempo': 87,
            'chords_available': True,
            'tabs_available': False,
            'is_popular': False,
            'play_count': 4500,
            'rating': 4.3
        },
        {
            'title': 'Başka',
            'artist': tarkan,
            'genre': pop_genre,
            'lyrics': 'Başka, başka...',
            'difficulty': 'intermediate',
            'year': 2001,
            'duration': timedelta(minutes=3, seconds=40),
            'key': 'Cm',
            'tempo': 125,
            'chords_available': True,
            'tabs_available': True,
            'is_popular': True,
            'play_count': 20000,
            'rating': 4.8
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
