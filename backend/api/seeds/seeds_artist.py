#!/usr/bin/env python
"""
Seed file for the Artist model.
Uses update_or_create to ensure data is always fresh and correct.
Run with: python manage.py shell < seeds/seeds_artist.py
"""

from api.models import Artist
from datetime import date

def seed_artists():
    """Seed artists with famous Turkish musicians."""
    
    print("🎤 Starting artist seeding...")

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
    updated_count = 0

    for artist_data in artists_data:
        # Use update_or_create to keep records fresh.
        # It finds an artist by 'name'. If found, it updates the other fields.
        # If not found, it creates a new artist.
        obj, created = Artist.objects.update_or_create(
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
            print(f"✅ Created artist: {obj.name}")
        else:
            updated_count += 1
            print(f"🔄 Updated artist: {obj.name}")
    
    print("\n🎉 Artist seeding completed!")
    print(f"📊 Total created: {created_count}, Total updated: {updated_count}")
    return created_count

# This check ensures the script can be run directly from the manage.py shell
if __name__ == 'django.core.management.commands.shell':
    seed_artists()
