#!/usr/bin/env python
"""
Seed file for ChordDiagram model
Run with: python manage.py shell < seeds_chord_diagram.py
"""

from api.models import ChordDiagram

def seed_chord_diagrams():
    """Seed chord diagrams with common guitar chords"""
    
    chords_data = [
        {
            'chord_name': 'C',
            'tuning': 'EADGBE',
            'frets': [0, 3, 2, 0, 1, 0],
            'fingers': [0, 3, 2, 0, 1, 0],
            'difficulty': 'beginner'
        },
        {
            'chord_name': 'G',
            'tuning': 'EADGBE',
            'frets': [3, 2, 0, 0, 0, 3],
            'fingers': [2, 1, 0, 0, 0, 3],
            'difficulty': 'beginner'
        },
        {
            'chord_name': 'Am',
            'tuning': 'EADGBE',
            'frets': [0, 0, 2, 2, 1, 0],
            'fingers': [0, 0, 2, 3, 1, 0],
            'difficulty': 'beginner'
        },
        {
            'chord_name': 'F',
            'tuning': 'EADGBE',
            'frets': [1, 3, 3, 2, 1, 1],
            'fingers': [1, 3, 4, 2, 1, 1],
            'difficulty': 'intermediate'
        },
        {
            'chord_name': 'D',
            'tuning': 'EADGBE',
            'frets': [2, 3, 2, 0, 0, 0],
            'fingers': [1, 3, 2, 0, 0, 0],
            'difficulty': 'beginner'
        },
        {
            'chord_name': 'Em',
            'tuning': 'EADGBE',
            'frets': [0, 0, 2, 2, 0, 0],
            'fingers': [0, 0, 2, 3, 0, 0],
            'difficulty': 'beginner'
        },
        {
            'chord_name': 'Bm',
            'tuning': 'EADGBE',
            'frets': [2, 2, 4, 4, 3, 2],
            'fingers': [1, 1, 3, 4, 2, 1],
            'difficulty': 'intermediate'
        },
        {
            'chord_name': 'A',
            'tuning': 'EADGBE',
            'frets': [0, 2, 2, 2, 0, 0],
            'fingers': [0, 2, 3, 4, 0, 0],
            'difficulty': 'beginner'
        },
        {
            'chord_name': 'E',
            'tuning': 'EADGBE',
            'frets': [0, 0, 1, 1, 1, 0],
            'fingers': [0, 0, 1, 2, 3, 0],
            'difficulty': 'beginner'
        },
        {
            'chord_name': 'Dm',
            'tuning': 'EADGBE',
            'frets': [1, 3, 3, 1, 1, 1],
            'fingers': [1, 3, 4, 1, 1, 1],
            'difficulty': 'intermediate'
        }
    ]
    
    created_count = 0
    for chord_data in chords_data:
        chord, created = ChordDiagram.objects.get_or_create(
            chord_name=chord_data['chord_name'],
            tuning=chord_data['tuning'],
            defaults={
                'frets': chord_data['frets'],
                'fingers': chord_data['fingers'],
                'difficulty': chord_data['difficulty']
            }
        )
        if created:
            created_count += 1
            print(f"Created chord diagram: {chord.chord_name} ({chord.tuning})")
        else:
            print(f"Chord diagram already exists: {chord.chord_name} ({chord.tuning})")
    
    print(f"\nTotal chord diagrams created: {created_count}")
    return created_count

if __name__ == "__main__":
    seed_chord_diagrams()
