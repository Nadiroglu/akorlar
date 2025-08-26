#!/usr/bin/env python
"""
Seed file for SearchQuery model
Run with: python manage.py shell < seeds_search_query.py
"""

from api.models import SearchQuery
from datetime import datetime, timedelta
import random

def seed_search_queries():
    """Seed search queries with sample analytics data"""
    
    # Sample search terms
    search_terms = [
        'Barış Manço',
        'Dağlar Dağlar',
        'Gül Pembe',
        'Türk Halk Müziği',
        'Gitar akorları',
        'Am akoru',
        'C akoru',
        'Pop şarkıları',
        'Rock müzik',
        'Sezen Aksu',
        'Tarkan',
        'Şımarık',
        'Kuzu Kuzu',
        'Neşet Ertaş',
        'Bağlama',
        'Türk Sanat Müziği',
        'Makam',
        'Jazz',
        'Blues',
        'Country'
    ]
    
    # Generate random search queries over the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    created_count = 0
    for _ in range(100):  # Create 100 sample search queries
        # Random search term
        query = random.choice(search_terms)
        
        # Random timestamp within last 30 days
        random_days = random.randint(0, 30)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        timestamp = end_date - timedelta(
            days=random_days,
            hours=random_hours,
            minutes=random_minutes
        )
        
        # Random results count
        results_count = random.randint(5, 50)
        
        # Random IP address (for demo purposes)
        ip_address = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        search_query, created = SearchQuery.objects.get_or_create(
            query=query,
            timestamp=timestamp,
            defaults={
                'results_count': results_count,
                'ip_address': ip_address
            }
        )
        
        if created:
            created_count += 1
            print(f"Created search query: '{query}' at {timestamp}")
        else:
            print(f"Search query already exists: '{query}' at {timestamp}")
    
    print(f"\nTotal search queries created: {created_count}")
    return created_count

if __name__ == "__main__":
    seed_search_queries()
