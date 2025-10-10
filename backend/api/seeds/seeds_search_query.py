#!/usr/bin/env python
"""
Seed file for SearchQuery model
Run with: python manage.py shell < seeds/seeds_search_query.py
"""

from api.models import SearchQuery
from datetime import datetime, timedelta
import random

def seed_search_queries():
    """Seed search queries with sample analytics data"""
    
    print("🔍 Seeding Search Queries...")

    # Sample search terms
    search_terms = [
        'Barış Manço', 'Dağlar Dağlar', 'Gül Pembe', 'Türk Halk Müziği',
        'Gitar akorları', 'Am akoru', 'C akoru', 'Pop şarkıları', 'Rock müzik',
        'Sezen Aksu', 'Tarkan', 'Şımarık', 'Kuzu Kuzu', 'Neşet Ertaş',
        'Bağlama', 'Türk Sanat Müziği', 'Makam', 'Jazz', 'Blues', 'Country'
    ]
    
    # Generate random search queries over the last 30 days
    end_date = datetime.now()
    
    created_count = 0
    updated_count = 0

    for _ in range(100):  # Create 100 sample search queries
        # Random search term
        query = random.choice(search_terms)
        
        # Random timestamp within last 30 days
        random_seconds = random.randint(0, 30 * 24 * 60 * 60)
        timestamp = end_date - timedelta(seconds=random_seconds)
        
        # Random results count
        results_count = random.randint(5, 50)
        
        # Random IP address (for demo purposes)
        ip_address = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        # Use update_or_create to prevent duplicates if script is run multiple times
        # A real analytics system might handle this differently, but for seeding this is robust.
        obj, created = SearchQuery.objects.update_or_create(
            query=query,
            timestamp=timestamp, # Using timestamp in the lookup makes each entry unique
            defaults={
                'results_count': results_count,
                'ip_address': ip_address
            }
        )
        
        if created:
            created_count += 1
        else:
            updated_count += 1

    print(f"   ✅ Created: {created_count}, Updated: {updated_count}")
    return created_count

if __name__ == 'django.core.management.commands.shell':
    seed_search_queries()
