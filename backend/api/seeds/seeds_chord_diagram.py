#!/usr/bin/env python
"""
Comprehensive seed file for ChordDiagram model
Creates guitar chord diagrams for all chords used in Turkish songs
Run with: python manage.py shell < seeds_chord_diagram.py
"""

from api.models import ChordDiagram

def seed_chord_diagrams():
    """Seed chord diagrams for common guitar chords used in Turkish music"""
    
    print("🎸 Starting chord diagram seeding...")
    
    # Define chord diagrams for common guitar chords
    chord_diagrams = [
        # Major Chords
        {
            'chord_name': 'C',
            'tuning': 'EADGBE',
            'frets': [['x', 3, 2, 0, 1, 0]],
            'fingers': [['x', 2, 1, 0, 3, 0]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'D',
            'tuning': 'EADGBE',
            'frets': [['x', 'x', 0, 2, 3, 2]],
            'fingers': [['x', 'x', 0, 1, 3, 2]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'E',
            'tuning': 'EADGBE',
            'frets': [[0, 2, 2, 1, 0, 0]],
            'fingers': [[0, 2, 3, 1, 0, 0]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'F',
            'tuning': 'EADGBE',
            'frets': [[1, 3, 3, 2, 1, 1]],
            'fingers': [[1, 3, 4, 2, 1, 1]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        },
        {
            'chord_name': 'G',
            'tuning': 'EADGBE',
            'frets': [[3, 2, 0, 0, 0, 3]],
            'fingers': [[2, 1, 0, 0, 0, 3]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'A',
            'tuning': 'EADGBE',
            'frets': [['x', 0, 2, 2, 2, 0]],
            'fingers': [['x', 0, 1, 2, 3, 0]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'B',
            'tuning': 'EADGBE',
            'frets': [[2, 4, 4, 3, 2, 2]],
            'fingers': [[1, 3, 4, 2, 1, 1]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        },
        
        # Minor Chords
        {
            'chord_name': 'Am',
            'tuning': 'EADGBE',
            'frets': [['x', 0, 2, 2, 1, 0]],
            'fingers': [['x', 0, 2, 3, 1, 0]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'Bm',
            'tuning': 'EADGBE',
            'frets': [['x', 2, 4, 4, 3, 2]],
            'fingers': [['x', 1, 3, 4, 2, 1]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        },
        {
            'chord_name': 'Dm',
            'tuning': 'EADGBE',
            'frets': [['x', 'x', 0, 2, 3, 1]],
            'fingers': [['x', 'x', 0, 2, 3, 1]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'Em',
            'tuning': 'EADGBE',
            'frets': [[0, 2, 2, 0, 0, 0]],
            'fingers': [[0, 2, 3, 0, 0, 0]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'Fm',
            'tuning': 'EADGBE',
            'frets': [[1, 3, 3, 1, 1, 1]],
            'fingers': [[1, 3, 4, 1, 1, 1]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        },
        {
            'chord_name': 'Gm',
            'tuning': 'EADGBE',
            'frets': [[3, 5, 5, 3, 3, 3]],
            'fingers': [[1, 3, 4, 1, 1, 1]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        },
        
        # 7th Chords
        {
            'chord_name': 'G7',
            'tuning': 'EADGBE',
            'frets': [[3, 2, 0, 0, 0, 1]],
            'fingers': [[2, 1, 0, 0, 0, 3]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'C7',
            'tuning': 'EADGBE',
            'frets': [['x', 3, 2, 3, 1, 0]],
            'fingers': [['x', 2, 1, 3, 1, 0]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        },
        {
            'chord_name': 'D7',
            'tuning': 'EADGBE',
            'frets': [['x', 'x', 0, 2, 1, 2]],
            'fingers': [['x', 'x', 0, 2, 1, 3]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'E7',
            'tuning': 'EADGBE',
            'frets': [[0, 2, 0, 1, 0, 0]],
            'fingers': [[0, 2, 0, 1, 0, 0]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        {
            'chord_name': 'A7',
            'tuning': 'EADGBE',
            'frets': [['x', 0, 2, 0, 2, 0]],
            'fingers': [['x', 0, 1, 0, 2, 0]],
            'difficulty': 'beginner',
            'capo_friendly': True
        },
        
        # Flat chords (common in Turkish music)
        {
            'chord_name': 'Bb',
            'tuning': 'EADGBE',
            'frets': [[1, 1, 3, 3, 3, 1]],
            'fingers': [[1, 1, 2, 3, 4, 1]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        },
        {
            'chord_name': 'Eb',
            'tuning': 'EADGBE',
            'frets': [[6, 6, 8, 8, 8, 6]],
            'fingers': [[1, 1, 2, 3, 4, 1]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        },
        
        # Sharp chords
        {
            'chord_name': 'F#',
            'tuning': 'EADGBE',
            'frets': [[2, 4, 4, 3, 2, 2]],
            'fingers': [[1, 3, 4, 2, 1, 1]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        },
        {
            'chord_name': 'C#',
            'tuning': 'EADGBE',
            'frets': [[4, 6, 6, 5, 4, 4]],
            'fingers': [[1, 3, 4, 2, 1, 1]],
            'difficulty': 'intermediate',
            'capo_friendly': True
        }
    ]
    
    created_count = 0
    updated_count = 0
    
    for chord_data in chord_diagrams:
        # Check if chord diagram already exists
        existing = ChordDiagram.objects.filter(
            chord_name=chord_data['chord_name'],
            tuning=chord_data['tuning']
        ).first()
        
        if existing:
            # Update existing diagram
            existing.frets = chord_data['frets']
            existing.fingers = chord_data['fingers']
            existing.difficulty = chord_data['difficulty']
            existing.capo_friendly = chord_data.get('capo_friendly', False)
            existing.save()
            updated_count += 1
            print(f"🔄 Updated chord diagram: {chord_data['chord_name']}")
        else:
            # Create new diagram
            ChordDiagram.objects.create(
                chord_name=chord_data['chord_name'],
                tuning=chord_data['tuning'],
                frets=chord_data['frets'],
                fingers=chord_data['fingers'],
                difficulty=chord_data['difficulty'],
                capo_friendly=chord_data.get('capo_friendly', False)
            )
            created_count += 1
            print(f"✅ Created chord diagram: {chord_data['chord_name']}")
    
    print(f"\n🎉 Chord diagram seeding completed!")
    print(f"📊 Total created: {created_count}")
    print(f"🔄 Total updated: {updated_count}")
    print(f"🎸 Total chord diagrams: {created_count + updated_count}")
    
    return created_count + updated_count

if __name__ == "__main__":
    seed_chord_diagrams()
