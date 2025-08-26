#!/usr/bin/env python
"""
Seed file for Genre model
Run with: python manage.py shell < seeds_genre.py
"""

from api.models import Genre

def seed_genres():
    """Seed genres with Turkish music styles"""
    genres_data = [
        {
            'name': 'Türk Halk Müziği',
            'description': 'Traditional Turkish folk music with regional variations'
        },
        {
            'name': 'Türk Sanat Müziği',
            'description': 'Classical Turkish art music with makam system'
        },
        {
            'name': 'Arabesk',
            'description': 'Turkish popular music genre with emotional themes'
        },
        {
            'name': 'Pop',
            'description': 'Modern Turkish pop music'
        },
        {
            'name': 'Rock',
            'description': 'Turkish rock music'
        },
        {
            'name': 'Jazz',
            'description': 'Turkish jazz and fusion music'
        },
        {
            'name': 'Blues',
            'description': 'Turkish blues music'
        },
        {
            'name': 'Country',
            'description': 'Turkish country music'
        }
    ]
    
    created_count = 0
    for genre_data in genres_data:
        genre, created = Genre.objects.get_or_create(
            name=genre_data['name'],
            defaults={'description': genre_data['description']}
        )
        if created:
            created_count += 1
            print(f"Created genre: {genre.name}")
        else:
            print(f"Genre already exists: {genre.name}")
    
    print(f"\nTotal genres created: {created_count}")
    return created_count

if __name__ == "__main__":
    seed_genres()
