#!/usr/bin/env python
"""
Professional Music Theory Engine for Akorlar
Handles chord generation, progressions, transposition, and music theory calculations
"""

import re
from typing import List, Dict, Tuple, Optional
from enum import Enum


class Note(Enum):
    """Musical notes with their semitone values"""
    C = 0
    C_SHARP = 1
    D = 2
    D_SHARP = 3
    E = 4
    F = 5
    F_SHARP = 6
    G = 7
    G_SHARP = 8
    A = 9
    A_SHARP = 10
    B = 11


class ChordType(Enum):
    """Chord types with their interval patterns"""
    MAJOR = [0, 4, 7]           # Root, Major Third, Perfect Fifth
    MINOR = [0, 3, 7]            # Root, Minor Third, Perfect Fifth
    DIMINISHED = [0, 3, 6]       # Root, Minor Third, Diminished Fifth
    AUGMENTED = [0, 4, 8]        # Root, Major Third, Augmented Fifth
    MAJOR_7TH = [0, 4, 7, 11]   # Root, Major Third, Perfect Fifth, Major Seventh
    MINOR_7TH = [0, 3, 7, 10]   # Root, Minor Third, Perfect Fifth, Minor Seventh
    DOMINANT_7TH = [0, 4, 7, 10] # Root, Major Third, Perfect Fifth, Minor Seventh
    DIMINISHED_7TH = [0, 3, 6, 9] # Root, Minor Third, Diminished Fifth, Diminished Seventh


class MusicTheoryEngine:
    """Professional music theory engine for chord operations"""
    
    # Note names for display
    NOTE_NAMES = {
        0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
        6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
    }
    
    # Flat note names
    FLAT_NOTE_NAMES = {
        0: 'C', 1: 'Db', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F',
        6: 'Gb', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'
    }
    
    # Major scale intervals
    MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
    
    # Common chord progressions (Roman numerals)
    COMMON_PROGRESSIONS = {
        "pop": ["I", "vi", "IV", "V"],
        "folk": ["I", "V", "vi", "IV"],
        "jazz": ["ii", "V", "I", "vi"],
        "blues": ["I", "IV", "I", "V", "IV", "I"],
        "turkish_pop": ["i", "VII", "VI", "V"],
        "turkish_folk": ["i", "v", "VI", "III"],
        "arabesk": ["i", "VII", "VI", "V", "i"]
    }
    
    def __init__(self):
        self._note_to_semitone = {note.name: note.value for note in Note}
        self._semitone_to_note = {note.value: note.name for note in Note}
    
    def note_to_semitone(self, note_name: str) -> int:
        """Convert note name to semitone value"""
        # Handle both sharp and flat notations
        note_name = note_name.upper().replace('B', 'Bb').replace('#', 'SHARP')
        
        if note_name in self._note_to_semitone:
            return self._note_to_semitone[note_name]
        
        # Handle enharmonic equivalents
        enharmonic_map = {
            'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 'G#': 'Ab', 'A#': 'Bb'
        }
        
        if note_name in enharmonic_map:
            return self._note_to_semitone[enharmonic_map[note_name]]
        
        raise ValueError(f"Invalid note name: {note_name}")
    
    def semitone_to_note(self, semitone: int, use_flats: bool = False) -> str:
        """Convert semitone value to note name"""
        semitone = semitone % 12
        if use_flats:
            return self.FLAT_NOTE_NAMES[semitone]
        return self.NOTE_NAMES[semitone]
    
    def transpose_note(self, note_name: str, semitones: int, use_flats: bool = False) -> str:
        """Transpose a note by given semitones"""
        original_semitone = self.note_to_semitone(note_name)
        new_semitone = (original_semitone + semitones) % 12
        return self.semitone_to_note(new_semitone, use_flats)
    
    def build_chord(self, root_note: str, chord_type: ChordType) -> List[str]:
        """Build a chord from root note and chord type"""
        root_semitone = self.note_to_semitone(root_note)
        chord_notes = []
        
        for interval in chord_type.value:
            note_semitone = (root_semitone + interval) % 12
            note_name = self.semitone_to_note(note_semitone)
            chord_notes.append(note_name)
        
        return chord_notes
    
    def roman_numeral_to_chord(self, roman_numeral: str, key: str) -> str:
        """Convert Roman numeral to actual chord in given key"""
        # Parse Roman numeral
        numeral = roman_numeral.upper()
        quality = "major"  # Default
        
        if numeral.startswith('i'):
            quality = "minor"
            numeral = numeral[1:]
        elif numeral.startswith('v'):
            quality = "minor"
            numeral = numeral[1:]
        
        # Get scale degree
        degree_map = {"I": 0, "II": 1, "III": 2, "IV": 3, "V": 4, "VI": 5, "VII": 6}
        if numeral not in degree_map:
            raise ValueError(f"Invalid Roman numeral: {roman_numeral}")
        
        scale_degree = degree_map[numeral]
        
        # Get the note at this scale degree
        key_semitone = self.note_to_semitone(key)
        scale_note_semitone = (key_semitone + self.MAJOR_SCALE[scale_degree]) % 12
        scale_note = self.semitone_to_note(scale_note_semitone)
        
        # Determine chord quality based on scale degree and key
        if key.upper() in ['C', 'G', 'D', 'A', 'E', 'B', 'F#']:  # Sharp keys
            if scale_degree in [1, 2, 5]:  # ii, iii, vi are minor in major keys
                quality = "minor"
            elif scale_degree == 6:  # vii is diminished
                quality = "diminished"
        else:  # Flat keys
            if scale_degree in [1, 2, 5]:
                quality = "minor"
            elif scale_degree == 6:
                quality = "diminished"
        
        return f"{scale_note}{'m' if quality == 'minor' else ''}"
    
    def generate_progression(self, key: str, progression_type: str, bars: int = 4, beats_per_bar: int = 4) -> List[Dict]:
        """Generate a complete chord progression with timing"""
        if progression_type not in self.COMMON_PROGRESSIONS:
            raise ValueError(f"Unknown progression type: {progression_type}")
        
        pattern = self.COMMON_PROGRESSIONS[progression_type]
        progression = []
        
        # Calculate how many times to repeat the pattern to fill the bars
        total_beats = bars * beats_per_bar
        pattern_beats = len(pattern)
        repetitions = total_beats // pattern_beats
        
        for bar in range(bars):
            for beat in range(beats_per_bar):
                pattern_index = (bar * beats_per_bar + beat) % pattern_beats
                roman_numeral = pattern[pattern_index]
                
                try:
                    chord_name = self.roman_numeral_to_chord(roman_numeral, key)
                    progression.append({
                        'chord_name': chord_name,
                        'bar': bar + 1,
                        'beat': beat + 1,
                        'duration': 1,  # 1 beat duration
                        'roman_numeral': roman_numeral
                    })
                except ValueError as e:
                    # Fallback to basic chord if Roman numeral conversion fails
                    progression.append({
                        'chord_name': f"{key}",
                        'bar': bar + 1,
                        'beat': beat + 1,
                        'duration': 1,
                        'roman_numeral': roman_numeral
                    })
        
        return progression
    
    def transpose_progression(self, progression: List[Dict], semitones: int) -> List[Dict]:
        """Transpose an entire chord progression"""
        transposed = []
        
        for chord_data in progression:
            chord_name = chord_data['chord_name']
            
            # Extract root note (first character, handle sharps/flats)
            root_note = chord_name[0]
            if len(chord_name) > 1 and chord_name[1] in ['#', 'b']:
                root_note = chord_name[:2]
            
            # Transpose root note
            new_root = self.transpose_note(root_note, semitones)
            
            # Reconstruct chord name
            if chord_name.startswith(root_note):
                new_chord_name = chord_name.replace(root_note, new_root, 1)
            else:
                new_chord_name = new_root + chord_name[1:]
            
            transposed.append({
                **chord_data,
                'chord_name': new_chord_name
            })
        
        return transposed


# Global instance for easy access
music_engine = MusicTheoryEngine()
