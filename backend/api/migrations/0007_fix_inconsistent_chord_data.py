# Generated manually to fix inconsistent chord data

from django.db import migrations

def fix_chord_data_integrity(apps, schema_editor):
    """Fix inconsistent chord data by regenerating chord_name from root and quality"""
    Chord = apps.get_model('api', 'Chord')
    
    # Quality mapping for chord name generation
    quality_map = {
        'major': '',
        'minor': 'm',
        'diminished': 'dim',
        'augmented': 'aug',
        'dominant7': '7',
        'major7': 'maj7',
        'minor7': 'm7',
        'minor7b5': 'm7b5',
        'diminished7': 'dim7',
        'sus2': 'sus2',
        'sus4': 'sus4',
        'add9': 'add9',
        '6': '6',
        'minor6': 'm6',
        '9': '9',
        '11': '11',
        '13': '13',
        'maj9': 'maj9',
        'min9': 'm9',
        'maj11': 'maj11',
        'min11': 'm11',
    }
    
    print("Fixing inconsistent chord data...")
    fixed_count = 0
    error_count = 0
    
    for chord in Chord.objects.all():
        try:
            # Generate correct chord name from root and quality
            quality_suffix = quality_map.get(chord.quality, '')
            correct_chord_name = f"{chord.root}{quality_suffix}"
            
            # Only update if the chord name is incorrect
            if chord.chord_name != correct_chord_name:
                print(f"Fixing chord ID {chord.id}: {chord.chord_name} -> {correct_chord_name} (Root: {chord.root}, Quality: {chord.quality})")
                chord.chord_name = correct_chord_name
                chord.save()
                fixed_count += 1
            else:
                print(f"Chord ID {chord.id} is already correct: {chord.chord_name}")
                
        except Exception as e:
            print(f"Error fixing chord ID {chord.id}: {e}")
            error_count += 1
    
    print(f"Fixed {fixed_count} chords, {error_count} errors")

def reverse_fix_chord_data_integrity(apps, schema_editor):
    """Reverse migration - no action needed as we're fixing data, not changing structure"""
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_add_enhanced_chord_fields'),
    ]

    operations = [
        migrations.RunPython(fix_chord_data_integrity, reverse_fix_chord_data_integrity),
    ]
