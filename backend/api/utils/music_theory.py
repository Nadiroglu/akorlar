#!/usr/bin/env python
"""
Professional Music Theory Engine for Akorlar
Handles chord generation, progressions, transposition, and music theory calculations
"""

from typing import List, Dict, Optional

# --- Core Music Theory Definitions ---
# Using dictionaries for flexibility with various string inputs (e.g., 'Db', 'C#')
NOTE_TO_SEMITONE: Dict[str, int] = {
    'C': 0, 'B#': 0,
    'C#': 1, 'DB': 1,
    'D': 2,
    'D#': 3, 'EB': 3,
    'E': 4, 'FB': 4,
    'F': 5, 'E#': 5,
    'F#': 6, 'GB': 6,
    'G': 7,
    'G#': 8, 'AB': 8,
    'A': 9,
    'A#': 10, 'BB': 10,
    'B': 11, 'CB': 11,
}

SEMITONE_TO_NOTE_SHARP: Dict[int, str] = {
    0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
    6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
}

SEMITONE_TO_NOTE_FLAT: Dict[int, str] = {
    0: 'C', 1: 'Db', 2: 'D', 3: 'Eb', 4: 'E', 5: 'F',
    6: 'Gb', 7: 'G', 8: 'Ab', 9: 'A', 10: 'Bb', 11: 'B'
}

# --- Utility Class for Building Chord Names ---
class ChordBuilder:
    """Reusable chord name builder from structured fields."""
    def build_name(self, root: str, quality: str = '', bass: Optional[str] = None) -> str:
        """Constructs a standardized chord symbol."""
        # Convert model quality to display quality (e.g., 'major' -> '', 'minor' -> 'm')
        quality_map = {
            'major': '',
            'minor': 'm',
            'diminished': 'dim',
            'dominant7': '7',
        }
        display_quality = quality_map.get(quality, quality) # Fallback to the quality itself
        
        name = f"{root}{display_quality}"
        if bass:
            name += f"/{bass}"
        return name

class MusicTheoryEngine:
    """A robust music theory engine for chord and key operations."""
    
    # Diatonic chord qualities for major and natural minor scales
    MAJOR_KEY_QUALITIES = ["major", "minor", "minor", "major", "major", "minor", "diminished"]
    MINOR_KEY_QUALITIES = ["minor", "diminished", "major", "minor", "minor", "major", "major"]
    
    # Roman numeral to scale degree index (0-based)
    ROMAN_MAP = {"I": 0, "II": 1, "III": 2, "IV": 3, "V": 4, "VI": 5, "VII": 6}
    
    # Common chord progressions (Roman numerals)
    COMMON_PROGRESSIONS = {
        "pop": ["I", "V", "vi", "IV"],
        "jazz": ["ii", "V", "I", "vi"],
        "blues": ["I", "IV", "V", "I"],
        "turkish_pop": ["i", "VII", "VI", "V"],
    }
    
    def __init__(self):
        self.builder = ChordBuilder()

    def note_to_semitone(self, note_name: str) -> int:
        """Converts any valid note name to its semitone value."""
        standardized = note_name.strip().upper().replace('♭', 'B').replace('♯', '#')
        if standardized in NOTE_TO_SEMITONE:
            return NOTE_TO_SEMITONE[standardized]
        raise ValueError(f"Invalid note name: '{note_name}'")

    def semitone_to_note(self, semitone: int, use_flats: bool = False) -> str:
        """Converts a semitone value back to a note name."""
        semitone %= 12
        return SEMITONE_TO_NOTE_FLAT[semitone] if use_flats else SEMITONE_TO_NOTE_SHARP[semitone]
        
    def get_roman_numeral(self, key: str, chord_root: str, chord_quality: str) -> Dict[str, str]:
        """
        Determines the Roman numeral for a chord within a given key.
        This final version is more resilient to common chromatic alterations.
        """
        key_root_str = key.strip().replace('m', '').replace(' major', '').replace(' minor', '')
        key_is_minor = 'm' in key.lower() or 'minor' in key.lower()
        
        key_root_semitone = self.note_to_semitone(key_root_str)
        chord_root_semitone = self.note_to_semitone(chord_root)

        # Calculate the interval from the key's root to the chord's root
        interval = (chord_root_semitone - key_root_semitone + 12) % 12

        # Define the scale intervals for lookup
        major_scale_intervals = {0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6} # interval -> degree
        minor_scale_intervals = {0: 0, 2: 1, 3: 2, 5: 3, 7: 4, 8: 5, 10: 6}

        scale_to_check = minor_scale_intervals if key_is_minor else major_scale_intervals
        
        degree = None
        accidental = ""

        # Check for a direct diatonic match first
        if interval in scale_to_check:
            degree = scale_to_check[interval]
        else:
            # Check for common chromatic alterations (e.g., bVII in a major key)
            flat_interval = (interval + 1) % 12
            if flat_interval in scale_to_check:
                degree = scale_to_check[flat_interval]
                accidental = "b"

        if degree is None:
            raise ValueError(f"Chord root '{chord_root}' is not diatonic or a simple alteration in the key of {key}")

        # Determine the expected diatonic quality and the numeral
        qualities_to_check = self.MINOR_KEY_QUALITIES if key_is_minor else self.MAJOR_KEY_QUALITIES
        expected_quality = qualities_to_check[degree]
        
        numeral = list(self.ROMAN_MAP.keys())[degree]

        # Set case based on the actual chord quality, not the diatonic expectation
        if chord_quality in ['minor', 'diminished']:
            numeral = numeral.lower()
        
        return {"roman_numeral": accidental + numeral, "expected_quality": expected_quality}

    def roman_numeral_to_chord(self, roman_numeral: str, key: str, key_is_minor: bool) -> Dict[str, str]:
        """
        Converts a Roman numeral to a chord components dictionary within a given key.
        """
        numeral_upper = roman_numeral.upper()
        if numeral_upper not in self.ROMAN_MAP:
            raise ValueError(f"Invalid Roman numeral: {roman_numeral}")
        degree = self.ROMAN_MAP[numeral_upper]
        
        key_root_semitone = self.note_to_semitone(key)
        major_scale_intervals = [0, 2, 4, 5, 7, 9, 11]
        root_semitone = (key_root_semitone + major_scale_intervals[degree]) % 12
        
        if key_is_minor:
            # Adjust for the flattened 3rd, 6th, and 7th of a natural minor scale
            if degree in [2, 5, 6]:
                root_semitone = (root_semitone - 1 + 12) % 12
            quality = self.MINOR_KEY_QUALITIES[degree]
        else:
            quality = self.MAJOR_KEY_QUALITIES[degree]
            
        # The V chord in a minor key is almost always raised to be major (dominant)
        if key_is_minor and degree == 4:
            quality = "major"
        
        return {
            "root": self.semitone_to_note(root_semitone),
            "quality": quality,
        }

    def generate_progression(self, key: str, progression_type: str) -> List[Dict]:
        """Generates a list of chord data from a key and progression type."""
        if progression_type not in self.COMMON_PROGRESSIONS:
            raise ValueError(f"Unknown progression type: {progression_type}")
            
        key_root = key.replace('m', '')
        key_is_minor = 'm' in key
        pattern = self.COMMON_PROGRESSIONS[progression_type]
        
        progression = []
        for i, numeral in enumerate(pattern):
            try:
                chord_components = self.roman_numeral_to_chord(numeral, key_root, key_is_minor)
                progression.append({
                    'chord_name': self.builder.build_name(**chord_components),
                    'bar': (i // 4) + 1,
                    'beat': (i % 4) + 1,
                    'roman_numeral': numeral,
                    **chord_components,
                })
            except ValueError:
                continue # Skip if numeral is invalid
        return progression

    def calculate_semitones_between_keys(self, from_key: str, to_key: str) -> int:
        """Calculates the semitone difference between two keys."""
        from_base = from_key.replace(' major', '').replace(' minor', '').replace('m', '')
        to_base = to_key.replace(' major', '').replace(' minor', '').replace('m', '')
        
        from_semitone = self.note_to_semitone(from_base)
        to_semitone = self.note_to_semitone(to_base)
        
        diff = to_semitone - from_semitone
        if diff > 6:
            return diff - 12
        if diff < -6:
            return diff + 12
        return diff

# Global instance for easy access
music_engine = MusicTheoryEngine()

