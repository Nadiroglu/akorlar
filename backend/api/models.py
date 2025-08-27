from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    key = models.CharField(max_length=10, blank=True)  # C, D, E, etc.
    tempo = models.IntegerField(null=True, blank=True)  # BPM
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

class Chord(models.Model):
    """Chord model for songs"""
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='chords')
    chord_name = models.CharField(max_length=20)  # C, Dm, G7, etc.
    position = models.IntegerField()  # Position in the song
    bar = models.IntegerField()  # Bar number
    beat = models.IntegerField()  # Beat within the bar
    duration = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)  # Duration in beats
    roman_numeral = models.CharField(max_length=10, blank=True)  # I, ii, V, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['position', 'bar', 'beat']
        unique_together = ['song', 'position', 'bar', 'beat']
    
    def __str__(self):
        return f"{self.song.title} - {self.chord_name} (Bar {self.bar}, Beat {self.beat})"

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
