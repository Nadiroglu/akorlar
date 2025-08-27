#!/usr/bin/env python
"""
Seed file for Artist model
Run with: python manage.py shell < seeds_artist.py
"""

from api.models import Artist
from datetime import date

def seed_artists():
    """Seed artists with famous Turkish musicians"""
    artists_data = [
        {
            'name': 'Barış Manço',
            'bio': 'Legendary Turkish rock musician, composer, and TV personality',
            'country': 'Turkey',
            'birth_date': date(1943, 1, 2),
            'image': 'https://example.com/baris-manco.jpg',
            'website': 'https://barismanco.com'
        },
        {
            'name': 'Sezen Aksu',
            'bio': 'Queen of Turkish pop music, singer-songwriter',
            'country': 'Turkey',
            'birth_date': date(1954, 7, 13),
            'image': 'https://example.com/sezen-aksu.jpg',
            'website': 'https://sezenaksu.com'
        },
        {
            'name': 'Tarkan',
            'bio': 'International Turkish pop star and singer',
            'country': 'Turkey',
            'birth_date': date(1972, 10, 17),
            'image': 'https://example.com/tarkan.jpg',
            'website': 'https://tarkan.com'
        },
        {
            'name': 'Erkan Oğur',
            'bio': 'Turkish musician and composer, inventor of fretless guitar',
            'country': 'Turkey',
            'birth_date': date(1954, 4, 17),
            'image': 'https://example.com/erkan-ogur.jpg',
            'website': ''
        },
        {
            'name': 'Müzeyyen Senar',
            'bio': 'Legendary Turkish classical singer',
            'country': 'Turkey',
            'birth_date': date(1918, 7, 16),
            'image': 'https://example.com/muzeyyen-senar.jpg',
            'website': ''
        },
        {
            'name': 'Neşet Ertaş',
            'bio': 'Famous Turkish folk singer and bağlama player',
            'country': 'Turkey',
            'birth_date': date(1938, 7, 25),
            'image': 'https://example.com/neset-ertas.jpg',
            'website': ''
        },
        {
            'name': 'Ahmet Kaya',
            'bio': 'Turkish folk singer and songwriter',
            'country': 'Turkey',
            'birth_date': date(1957, 10, 28),
            'image': 'https://example.com/ahmet-kaya.jpg',
            'website': ''
        },
        {
            'name': 'Zeki Müren',
            'bio': 'Turkish classical singer, composer, and actor',
            'country': 'Turkey',
            'birth_date': date(1931, 12, 6),
            'image': 'https://example.com/zeki-muren.jpg',
            'website': ''
        }
    ]
    
    created_count = 0
    for artist_data in artists_data:
        artist, created = Artist.objects.get_or_create(
            name=artist_data['name'],
            defaults={
                'bio': artist_data['bio'],
                'country': artist_data['country'],
                'birth_date': artist_data['birth_date'],
                'image': artist_data['image'],
                'website': artist_data['website']
            }
        )
        if created:
            created_count += 1
            print(f"Created artist: {artist.name}")
        else:
            print(f"Artist already exists: {artist.name}")
    
    print(f"\nTotal artists created: {created_count}")
    return created_count

if __name__ == "__main__":
    seed_artists()
