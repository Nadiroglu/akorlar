from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

# Import the models
from ..models import (
    Genre, Artist, Song, Chord, ChordDiagram, SongRequest, SearchQuery
)

# Import serializers
from ..serializers import (
    SongSerializer, ArtistSerializer, GenreSerializer, ChordDiagramSerializer
)

# Import the custom view (moved to avoid circular import)
# from ..views.admin_views import SongManagementView

# Django Admin Classes
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'birth_date']
    list_filter = ['country']
    search_fields = ['name', 'bio']
    ordering = ['name']

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """
    The main admin interface for the Song list view.
    """
    list_display = ['title', 'artist', 'genre', 'key', 'difficulty', 'manage_song_link']
    list_filter = ['genre', 'difficulty', 'key', 'chords_available', 'is_popular']
    search_fields = ['title', 'artist__name']
    ordering = ['-created_at']
    
    def manage_song_link(self, obj):
        """Generate a link to our custom management view for an existing song."""
        # TODO: Implement custom song management
        return format_html('<span class="button">Manage Chords (Coming Soon)</span>')
    manage_song_link.short_description = 'Actions'

@admin.register(Chord)
class ChordAdmin(admin.ModelAdmin):
    list_display = ['chord_name', 'song', 'root', 'quality', 'measure', 'beat']
    list_filter = ['root', 'quality', 'song__genre']
    search_fields = ['chord_name', 'song__title']
    ordering = ['song', 'measure', 'beat']

@admin.register(ChordDiagram)
class ChordDiagramAdmin(admin.ModelAdmin):
    list_display = ['chord_name', 'tuning', 'capo_friendly']
    list_filter = ['capo_friendly', 'difficulty']
    search_fields = ['chord_name']
    ordering = ['chord_name']

@admin.register(SongRequest)
class SongRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist_name', 'status', 'requested_at']
    list_filter = ['status', 'requested_at']
    search_fields = ['title', 'artist_name', 'user_email']
    ordering = ['-requested_at']

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'results_count', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['query']
    ordering = ['-timestamp']

# API ViewSets for admin endpoints
class AdminSongViewSet(viewsets.ModelViewSet):
    """
    Admin-only ViewSet for managing songs with full CRUD operations.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['genre', 'difficulty', 'key', 'is_popular']
    search_fields = ['title', 'artist__name']

class AdminArtistViewSet(viewsets.ModelViewSet):
    """
    Admin-only ViewSet for managing artists with full CRUD operations.
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['name', 'bio']

class AdminGenreViewSet(viewsets.ModelViewSet):
    """
    Admin-only ViewSet for managing genres with full CRUD operations.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['name']

class AdminChordDiagramViewSet(viewsets.ModelViewSet):
    """
    Admin-only ViewSet for managing chord diagrams with full CRUD operations.
    """
    queryset = ChordDiagram.objects.all()
    serializer_class = ChordDiagramSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['chord__root', 'chord__quality']