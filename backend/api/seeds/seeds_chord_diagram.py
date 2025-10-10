#!/usr/bin/env python
"""
Comprehensive seed file for ChordDiagram model
Creates guitar chord diagrams for all chords used in Turkish songs
Run with: python manage.py shell < seeds/seeds_chord_diagram.py
"""

from api.models import ChordDiagram

def seed_chord_diagrams():
    """Seed chord diagrams for common guitar chords used in Turkish music"""
    
    print("🎸 Starting chord diagram seeding...")
    
    # Define chord diagrams for common guitar chords
    chord_diagrams_data = [
        # Major Chords
        {
            'chord_name': 'C', 'tuning': 'EADGBE',
            'frets': ['x', 3, 2, 0, 1, 0], 'fingers': ['x', 3, 2, 0, 1, 0],
            'difficulty': 'beginner', 'capo_friendly': True
        },
        {
            'chord_name': 'D', 'tuning': 'EADGBE',
            'frets': ['x', 'x', 0, 2, 3, 2], 'fingers': ['x', 'x', 0, 1, 3, 2],
            'difficulty': 'beginner', 'capo_friendly': True
        },
        {
            'chord_name': 'E', 'tuning': 'EADGBE',
            'frets': [0, 2, 2, 1, 0, 0], 'fingers': [0, 2, 3, 1, 0, 0],
            'difficulty': 'beginner', 'capo_friendly': True
        },
        {
            'chord_name': 'F', 'tuning': 'EADGBE',
            'frets': [1, 3, 3, 2, 1, 1], 'fingers': [1, 3, 4, 2, 1, 1],
            'difficulty': 'intermediate', 'capo_friendly': True
        },
        {
            'chord_name': 'G', 'tuning': 'EADGBE',
            'frets': [3, 2, 0, 0, 0, 3], 'fingers': [2, 1, 0, 0, 0, 3],
            'difficulty': 'beginner', 'capo_friendly': True
        },
        {
            'chord_name': 'A', 'tuning': 'EADGBE',
            'frets': ['x', 0, 2, 2, 2, 0], 'fingers': ['x', 0, 1, 2, 3, 0],
            'difficulty': 'beginner', 'capo_friendly': True
        },
        
        # Minor Chords
        {
            'chord_name': 'Am', 'tuning': 'EADGBE',
            'frets': ['x', 0, 2, 2, 1, 0], 'fingers': ['x', 0, 2, 3, 1, 0],
            'difficulty': 'beginner', 'capo_friendly': True
        },
        {
            'chord_name': 'Bm', 'tuning': 'EADGBE',
            'frets': ['x', 2, 4, 4, 3, 2], 'fingers': ['x', 1, 3, 4, 2, 1],
            'difficulty': 'intermediate', 'capo_friendly': True
        },
        {
            'chord_name': 'Dm', 'tuning': 'EADGBE',
            'frets': ['x', 'x', 0, 2, 3, 1], 'fingers': ['x', 'x', 0, 2, 3, 1],
            'difficulty': 'beginner', 'capo_friendly': True
        },
        {
            'chord_name': 'Em', 'tuning': 'EADGBE',
            'frets': [0, 2, 2, 0, 0, 0], 'fingers': [0, 2, 3, 0, 0, 0],
            'difficulty': 'beginner', 'capo_friendly': True
        },

        # 7th Chords
        {
            'chord_name': 'G7', 'tuning': 'EADGBE',
            'frets': [3, 2, 0, 0, 0, 1], 'fingers': [2, 1, 0, 0, 0, 3],
            'difficulty': 'beginner', 'capo_friendly': True
        },
        {
            'chord_name': 'E7', 'tuning': 'EADGBE',
            'frets': [0, 2, 0, 1, 0, 0], 'fingers': [0, 2, 0, 1, 0, 0],
            'difficulty': 'beginner', 'capo_friendly': True
        },
        {
            'chord_name': 'A7', 'tuning': 'EADGBE',
            'frets': ['x', 0, 2, 0, 2, 0], 'fingers': ['x', 0, 1, 0, 2, 0],
            'difficulty': 'beginner', 'capo_friendly': True
        },

        # Flat Chords
        {
            'chord_name': 'Bb', 'tuning': 'EADGBE',
            'frets': ['x', 1, 3, 3, 3, 1], 'fingers': ['x', 1, 3, 4, 2, 1], # Common shape
            'difficulty': 'intermediate', 'capo_friendly': True
        },
    ]
    
    created_count = 0
    updated_count = 0
    
    for diagram_data in chord_diagrams_data:
        # Use update_or_create to simplify the logic.
        # It finds a diagram based on the unique fields (chord_name, tuning).
        # If found, it updates it with the 'defaults'. If not found, it creates it.
        obj, created = ChordDiagram.objects.update_or_create(
            chord_name=diagram_data['chord_name'],
            tuning=diagram_data['tuning'],
            defaults={
                'frets': diagram_data['frets'],
                'fingers': diagram_data['fingers'],
                'difficulty': diagram_data['difficulty'],
                'capo_friendly': diagram_data.get('capo_friendly', False)
            }
        )
        
        if created:
            created_count += 1
            print(f"✅ Created chord diagram: {obj.chord_name}")
        else:
            updated_count += 1
            print(f"🔄 Updated chord diagram: {obj.chord_name}")

    print(f"\n🎉 Chord diagram seeding completed!")
    print(f"📊 Total created: {created_count}")
    print(f"🔄 Total updated: {updated_count}")
    print(f"🎸 Total chord diagrams in database: {ChordDiagram.objects.count()}")
    
    return created_count + updated_count

# This check ensures the script can be run directly from the manage.py shell
if __name__ == 'django.core.management.commands.shell':
    seed_chord_diagrams()
