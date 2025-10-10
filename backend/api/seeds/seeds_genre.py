#!/usr/bin/env python
"""
Seed file for the Genre model.
Uses update_or_create to ensure data is always fresh and correct.
Run with: python manage.py shell < seeds/seeds_genre.py
"""

from api.models import Genre

def seed_genres():
    """Seed genres with Turkish music styles."""
    
    print("🎶 Starting genre seeding...")

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
    updated_count = 0

    for genre_data in genres_data:
        # Use update_or_create to keep records fresh.
        # It finds a genre by 'name'. If found, it updates the description.
        # If not found, it creates a new genre.
        obj, created = Genre.objects.update_or_create(
            name=genre_data['name'],
            defaults={'description': genre_data['description']}
        )
        
        if created:
            created_count += 1
            print(f"✅ Created genre: {obj.name}")
        else:
            updated_count += 1
            print(f"🔄 Updated genre: {obj.name}")
    
    print("\n🎉 Genre seeding completed!")
    print(f"📊 Total created: {created_count}, Total updated: {updated_count}")
    return created_count

# This check ensures the script can be run directly from the manage.py shell
if __name__ == 'django.core.management.commands.shell':
    seed_genres()
