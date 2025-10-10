from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

# Other models (Genre, Artist) are unchanged...

class Genre(models.Model):
    """Music genre model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Artist(models.Model):
    """Artist/Performer model"""
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.URLField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Song(models.Model):
    """Song model"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='songs')
    lyrics = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    year = models.IntegerField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    key = models.CharField(max_length=10, blank=True)
    tempo = models.IntegerField(null=True, blank=True)
    chords_available = models.BooleanField(default=False)
    tabs_available = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    play_count = models.IntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['title', 'artist']
    
    def __str__(self):
        return f"{self.title} - {self.artist.name}"

    def transpose_to_key(self, target_key: str):
        """
        Atomically transposes the song to a new key, updating the song's key,
        and every associated chord's root, name, context, and Roman numeral.
        Returns a tuple: (success: bool, message: str).
        """
        from api.utils.music_theory import music_engine

        current_key = self.key
        if not current_key or not target_key:
            return False, "Current key or target key is not set."

        try:
            semitones = music_engine.calculate_semitones_between_keys(current_key, target_key)
        except ValueError as e:
            return False, f"Could not calculate semitones: {e}"
        
        if semitones == 0:
            return True, "Song is already in the target key."

        try:
            with transaction.atomic():
                chords_to_update = list(self.chords.all())
                
                key_is_minor = 'm' in target_key.lower() or 'minor' in target_key.lower()
                
                for chord in chords_to_update:
                    # 1. Transpose the root note
                    chord.root = chord.transpose(semitones)
                    
                    # 2. Regenerate the chord name from its components
                    chord.chord_name = chord.generate_chord_name()
                    
                    # 3. CRITICAL: Update the context and Roman numeral
                    chord.key_context = target_key
                    try:
                        # Attempt to recalculate the Roman numeral
                        numeral_data = music_engine.get_roman_numeral(
                            key=target_key, 
                            chord_root=chord.root, 
                            chord_quality=chord.quality
                        )
                        chord.roman_numeral = numeral_data['roman_numeral']
                    except (ValueError, KeyError):
                        # If the chord is non-diatonic, the numeral might not be found.
                        # In this case, we can clear it or leave it. Clearing is safer.
                        chord.roman_numeral = ''

                    # 4. Validate the integrity of the newly transposed chord
                    chord.full_clean()
                
                # 5. Perform a single, efficient bulk update
                fields_to_update = ['root', 'chord_name', 'key_context', 'roman_numeral']
                Chord.objects.bulk_update(chords_to_update, fields_to_update)
                
                # 6. Update the parent song's key
                self.key = target_key
                self.save(update_fields=['key', 'updated_at'])

            return True, f"Song transposed successfully to {target_key}."
        except ValidationError as e:
            return False, f"Transposition failed: A resulting chord was invalid. Details: {e}"
        except Exception as e:
            # Catch any other unexpected errors during the process
            return False, f"An unexpected error occurred during transposition: {e}"


# --- Other models (Chord, ChordDiagram, etc.) are unchanged ---

class Chord(models.Model):
    """Enhanced chord model for songs with separated musical components"""
    
    # Root note choices
    ROOT_CHOICES = [
        ('C', 'C'),
        ('C#', 'C#/D♭'),
        ('Db', 'D♭/C#'),
        ('D', 'D'),
        ('D#', 'D#/E♭'),
        ('Eb', 'E♭/D#'),
        ('E', 'E'),
        ('F', 'F'),
        ('F#', 'F#/G♭'),
        ('Gb', 'G♭/F#'),
        ('G', 'G'),
        ('G#', 'G#/A♭'),
        ('Ab', 'A♭/G#'),
        ('A', 'A'),
        ('A#', 'A#/B♭'),
        ('Bb', 'B♭/A#'),
        ('B', 'B'),
    ]
    
    # Chord quality choices - comprehensive list of musically valid chord types
    QUALITY_CHOICES = [
        # Basic triads
        ('major', 'Major'),
        ('minor', 'Minor'),
        ('diminished', 'Diminished'),
        ('augmented', 'Augmented'),
        
        # 7th chords
        ('dominant7', 'Dominant 7th'),
        ('major7', 'Major 7th'),
        ('minor7', 'Minor 7th'),
        ('minor7b5', 'Minor 7th ♭5'),
        ('diminished7', 'Diminished 7th'),
        ('augmented7', 'Augmented 7th'),
        ('major7#5', 'Major 7th ♯5'),
        
        # Suspended chords
        ('sus2', 'Suspended 2nd'),
        ('sus4', 'Suspended 4th'),
        ('sus2sus4', 'Suspended 2nd & 4th'),
        
        # Added tone chords
        ('add9', 'Add 9th'),
        ('add11', 'Add 11th'),
        ('add13', 'Add 13th'),
        
        # 6th chords
        ('6', '6th'),
        ('minor6', 'Minor 6th'),
        ('major6', 'Major 6th'),
        
        # 9th chords
        ('9', '9th'),
        ('major9', 'Major 9th'),
        ('minor9', 'Minor 9th'),
        ('dominant9', 'Dominant 9th'),
        
        # 11th chords
        ('11', '11th'),
        ('major11', 'Major 11th'),
        ('minor11', 'Minor 11th'),
        
        # 13th chords
        ('13', '13th'),
        ('major13', 'Major 13th'),
        ('minor13', 'Minor 13th'),
        
        # Altered chords
        ('7#5', '7th ♯5'),
        ('7b5', '7th ♭5'),
        ('7#9', '7th ♯9'),
        ('7b9', '7th ♭9'),
        ('7#11', '7th ♯11'),
        ('7b13', '7th ♭13'),
    ]
    
    # Inversion choices
    INVERSION_CHOICES = [
        ('root', 'Root Position'),
        ('first', 'First Inversion'),
        ('second', 'Second Inversion'),
        ('third', 'Third Inversion'),
    ]
    
    # Valid extensions - musically valid chord extensions and alterations
    VALID_EXTENSIONS = [
        # Basic extensions
        'sus2', 'sus4', 'sus2sus4',
        'add9', 'add11', 'add13',
        '6', 'm6', 'maj6',
        '7', 'maj7', 'm7', 'm7b5', 'dim7', 'aug7', 'maj7#5',
        '9', 'maj9', 'm9', 'dom9',
        '11', 'maj11', 'm11',
        '13', 'maj13', 'm13',
        
        # Altered extensions
        '#5', 'b5', '#9', 'b9', '#11', 'b13',
        '7#5', '7b5', '7#9', '7b9', '7#11', '7b13',
        
        # Complex extensions
        'maj7#11', 'maj7#5', 'maj7b5',
        'm7#11', 'm7#5', 'm7b5',
        '9#11', '9b13', 'maj9#11',
        '11b13', 'maj11b13',
        '13#11', '13b9', 'maj13#11',
    ]
    
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='chords')
    
    # Core chord components - these are the source of truth
    root = models.CharField(max_length=3, choices=ROOT_CHOICES, help_text="Base note of the chord (e.g., 'C', 'A')")
    quality = models.CharField(max_length=20, choices=QUALITY_CHOICES, help_text="Chord type (e.g., 'major', 'minor', 'diminished')")
    extensions = models.CharField(max_length=50, blank=True, help_text="Additional chord modifiers (e.g., '7', 'sus4', 'add9')")
    inversion = models.CharField(max_length=10, choices=INVERSION_CHOICES, default='root', help_text="Chord inversion")
    
    # Precise timing system
    measure = models.IntegerField(validators=[MinValueValidator(1)], default=1, help_text="Measure number (1-based)")
    beat = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(1.0)], default=1.0, help_text="Beat within measure")
    sub_beat = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, help_text="Subdivision of beat")
    
    # Duration and context
    duration_in_beats = models.DecimalField(max_digits=4, decimal_places=2, default=1.0, help_text="Duration in beats")
    key_context = models.CharField(max_length=20, blank=True, help_text="Key signature for roman numeral context")
    roman_numeral = models.CharField(max_length=10, blank=True, help_text="Roman numeral (I, ii, V, etc.)")
    
    # Auto-generated chord name - this is derived from the components above
    chord_name = models.CharField(max_length=50, blank=True, help_text="Auto-generated chord name")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['measure', 'beat', 'sub_beat']
        unique_together = ['song', 'measure', 'beat', 'sub_beat']
        verbose_name = "Chord"
        verbose_name_plural = "Chords"
    
    def clean(self):
        """Validate chord data integrity and ensure chord_name matches components"""
        
        # Validate root note - must be a valid musical note
        valid_roots = [choice[0] for choice in self.ROOT_CHOICES]
        if self.root not in valid_roots:
            raise ValidationError(f"Invalid root note: '{self.root}'. Must be one of: {', '.join(valid_roots)}")
        
        # Validate quality - must be a musically valid chord type
        valid_qualities = [choice[0] for choice in self.QUALITY_CHOICES]
        if self.quality not in valid_qualities:
            raise ValidationError(f"Invalid chord quality: '{self.quality}'. Must be one of: {', '.join(valid_qualities)}")
        
        # Validate inversion - must be a valid inversion type
        valid_inversions = [choice[0] for choice in self.INVERSION_CHOICES]
        if self.inversion not in valid_inversions:
            raise ValidationError(f"Invalid inversion: '{self.inversion}'. Must be one of: {', '.join(valid_inversions)}")
        
        # Validate extensions - must be musically valid extensions
        if self.extensions and self.extensions.strip():
            extensions_list = [ext.strip() for ext in self.extensions.split(',') if ext.strip()]
            invalid_extensions = [ext for ext in extensions_list if ext not in self.VALID_EXTENSIONS]
            if invalid_extensions:
                raise ValidationError(
                    f"Invalid extensions: {invalid_extensions}. "
                    f"Valid extensions include: {', '.join(self.VALID_EXTENSIONS[:10])}... (and {len(self.VALID_EXTENSIONS)-10} more)"
                )
        
        # Validate timing constraints
        if self.measure < 1:
            raise ValidationError("Measure must be at least 1")
        if self.beat < 1.0:
            raise ValidationError("Beat must be at least 1.0")
        if self.sub_beat < 0.0:
            raise ValidationError("Sub-beat cannot be negative")
        if self.duration_in_beats <= 0:
            raise ValidationError("Duration must be positive")
        
        # Validate chord name consistency
        if self.chord_name and self.chord_name.strip():
            expected_chord_name = self.generate_chord_name()
            if self.chord_name != expected_chord_name:
                raise ValidationError(
                    f"Chord name '{self.chord_name}' does not match components. "
                    f"Expected: '{expected_chord_name}' (Root: {self.root}, Quality: {self.quality}, Extensions: {self.extensions or 'none'})"
                )
    
    def save(self, *args, **kwargs):
        """Auto-generate chord_name from components and validate data"""

        # Generate chord name from components
        self.chord_name = self.generate_chord_name()

        # Clean the data first
        self.full_clean()
        
        super().save(*args, **kwargs)
    
    def generate_chord_name(self):
        """Generate chord name from root, quality, and extensions with comprehensive mapping"""
        # Comprehensive quality mapping for chord name generation
        quality_map = {
            # Basic triads
            'major': '',           # C, D, E, F, G, A, B
            'minor': 'm',          # Cm, Dm, Em, Fm, Gm, Am, Bm
            'diminished': 'dim',   # Cdim, Ddim, Edim, Fdim, Gdim, Adim, Bdim
            'augmented': 'aug',    # Caug, Daug, Eaug, Faug, Gaug, Aaug, Baug
            
            # 7th chords
            'dominant7': '7',      # C7, D7, E7, F7, G7, A7, B7
            'major7': 'maj7',      # Cmaj7, Dmaj7, Emaj7, Fmaj7, Gmaj7, Amaj7, Bmaj7
            'minor7': 'm7',        # Cm7, Dm7, Em7, Fm7, Gm7, Am7, Bm7
            'minor7b5': 'm7b5',    # Cm7b5, Dm7b5, Em7b5, Fm7b5, Gm7b5, Am7b5, Bm7b5
            'diminished7': 'dim7', # Cdim7, Ddim7, Edim7, Fdim7, Gdim7, Adim7, Bdim7
            'augmented7': 'aug7',  # Caug7, Daug7, Eaug7, Faug7, Gaug7, Aaug7, Baug7
            'major7#5': 'maj7#5',  # Cmaj7#5, Dmaj7#5, Emaj7#5, Fmaj7#5, Gmaj7#5, Amaj7#5, Bmaj7#5
            
            # Suspended chords
            'sus2': 'sus2',        # Csus2, Dsus2, Esus2, Fsus2, Gsus2, Asus2, Bsus2
            'sus4': 'sus4',        # Csus4, Dsus4, Esus4, Fsus4, Gsus4, Asus4, Bsus4
            'sus2sus4': 'sus2sus4', # Csus2sus4, Dsus2sus4, Esus2sus4, Fsus2sus4, Gsus2sus4, Asus2sus4, Bsus2sus4
            
            # Added tone chords
            'add9': 'add9',        # Cadd9, Dadd9, Eadd9, Fadd9, Gadd9, Aadd9, Badd9
            'add11': 'add11',      # Cadd11, Dadd11, Eadd11, Fadd11, Gadd11, Aadd11, Badd11
            'add13': 'add13',      # Cadd13, Dadd13, Eadd13, Fadd13, Gadd13, Aadd13, Badd13
            
            # 6th chords
            '6': '6',              # C6, D6, E6, F6, G6, A6, B6
            'minor6': 'm6',        # Cm6, Dm6, Em6, Fm6, Gm6, Am6, Bm6
            'major6': 'maj6',      # Cmaj6, Dmaj6, Emaj6, Fmaj6, Gmaj6, Amaj6, Bmaj6
            
            # 9th chords
            '9': '9',              # C9, D9, E9, F9, G9, A9, B9
            'major9': 'maj9',      # Cmaj9, Dmaj9, Emaj9, Fmaj9, Gmaj9, Amaj9, Bmaj9
            'minor9': 'm9',        # Cm9, Dm9, Em9, Fm9, Gm9, Am9, Bm9
            'dominant9': 'dom9',   # Cdom9, Ddom9, Edom9, Fdom9, Gdom9, Adom9, Bdom9
            
            # 11th chords
            '11': '11',            # C11, D11, E11, F11, G11, A11, B11
            'major11': 'maj11',    # Cmaj11, Dmaj11, Emaj11, Fmaj11, Gmaj11, Amaj11, Bmaj11
            'minor11': 'm11',      # Cm11, Dm11, Em11, Fm11, Gm11, Am11, Bm11
            
            # 13th chords
            '13': '13',            # C13, D13, E13, F13, G13, A13, B13
            'major13': 'maj13',    # Cmaj13, Dmaj13, Emaj13, Fmaj13, Gmaj13, Amaj13, Bmaj13
            'minor13': 'm13',      # Cm13, Dm13, Em13, Fm13, Gm13, Am13, Bm13
            
            # Altered chords
            '7#5': '7#5',          # C7#5, D7#5, E7#5, F7#5, G7#5, A7#5, B7#5
            '7b5': '7b5',          # C7b5, D7b5, E7b5, F7b5, G7b5, A7b5, B7b5
            '7#9': '7#9',          # C7#9, D7#9, E7#9, F7#9, G7#9, A7#9, B7#9
            '7b9': '7b9',          # C7b9, D7b9, E7b9, F7b9, G7b9, A7b9, B7b9
            '7#11': '7#11',        # C7#11, D7#11, E7#11, F7#11, G7#11, A7#11, B7#11
            '7b13': '7b13',        # C7b13, D7b13, E7b13, F7b13, G7b13, A7b13, B7b13
        }
        
        # Validate that we have required fields
        if not self.root or not self.quality:
            return ''
        
        # Start with root note
        chord_parts = [self.root]
        
        # Add quality suffix
        quality_suffix = quality_map.get(self.quality, '')
        if quality_suffix:
            chord_parts.append(quality_suffix)
        
        # Add extensions if present
        if self.extensions and self.extensions.strip():
            chord_parts.append(self.extensions.strip())
        
        return ''.join(chord_parts)
    
    def __str__(self):
        return f"{self.song.title} - {self.chord_name} (M{self.measure}, B{self.beat})"
    
    def transpose(self, semitones: int) -> str:
        """Transpose chord by given number of semitones."""
        chromatic_scale = [
            'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'
        ]
        
        # Create a map for all note names (sharps and flats) to index
        note_to_index = {
            'C': 0, 'B#': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
            'E': 4, 'Fb': 4, 'F': 5, 'E#': 5, 'F#': 6, 'Gb': 6, 'G': 7,
            'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11, 'Cb': 11
        }
        
        current_index = note_to_index.get(self.root)
        if current_index is None:
            return self.root # Return original if not found
        
        new_index = (current_index + semitones) % 12
        return chromatic_scale[new_index] # Always prefer sharp notation for consistency

class ChordDiagram(models.Model):
    """Guitar chord diagram model"""
    chord_name = models.CharField(max_length=20)
    tuning = models.CharField(max_length=50, default='EADGBE')  # Guitar tuning
    frets = models.JSONField()  # Fret positions for each string
    fingers = models.JSONField()  # Finger positions
    difficulty = models.CharField(max_length=20, choices=Song.DIFFICULTY_CHOICES, default='intermediate')
    capo_friendly = models.BooleanField(default=False)  # Works well with capo
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['chord_name', 'tuning']
    
    def __str__(self):
        return f"{self.chord_name} ({self.tuning})"

class SongRequest(models.Model):
    """User requests for new songs"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    genre_name = models.CharField(max_length=100, blank=True)
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100, blank=True)
    additional_notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"{self.title} - {self.artist_name} (Requested by {self.user_email})"

class SearchQuery(models.Model):
    """Search query tracking for analytics"""
    query = models.CharField(max_length=200)
    results_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.query} ({self.timestamp})"

