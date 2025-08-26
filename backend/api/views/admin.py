from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.contrib.auth.models import User
from ..models import Song, Artist, Genre, Chord, ChordDiagram
from ..serializers.song import SongSerializer, SongDetailSerializer
from ..serializers.artist import ArtistSerializer
from ..serializers.genre import GenreSerializer
from ..serializers.chord import ChordSerializer
from ..serializers.chord_diagram import ChordDiagramSerializer

class IsAdminUser(permissions.BasePermission):
    """Custom permission to only allow admin users."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class AdminSongViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for managing songs with full CRUD operations"""
    queryset = Song.objects.select_related('artist', 'genre').prefetch_related('chords')
    serializer_class = SongSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre', 'difficulty', 'key', 'chords_available', 'tabs_available', 'is_popular']
    
    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return SongDetailSerializer
        return SongSerializer

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create multiple songs"""
        songs_data = request.data.get('songs', [])
        if not songs_data:
            return Response(
                {'error': 'No songs data provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_songs = []
        errors = []
        
        with transaction.atomic():
            for song_data in songs_data:
                try:
                    # Handle artist creation if needed
                    artist_name = song_data.get('artist_name')
                    if artist_name:
                        artist, created = Artist.objects.get_or_create(
                            name=artist_name,
                            defaults={
                                'bio': song_data.get('artist_bio', ''),
                                'country': song_data.get('artist_country', 'Turkey')
                            }
                        )
                        song_data['artist'] = artist.id
                    
                    # Handle genre creation if needed
                    genre_name = song_data.get('genre_name')
                    if genre_name:
                        genre, created = Genre.objects.get_or_create(
                            name=genre_name,
                            defaults={'description': f'Music genre: {genre_name}'}
                        )
                        song_data['genre'] = genre.id
                    
                    serializer = self.get_serializer(data=song_data)
                    if serializer.is_valid():
                        song = serializer.save()
                        created_songs.append(song)
                    else:
                        errors.append({
                            'data': song_data,
                            'errors': serializer.errors
                        })
                except Exception as e:
                    errors.append({
                        'data': song_data,
                        'errors': str(e)
                    })
        
        return Response({
            'created_count': len(created_songs),
            'errors': errors,
            'created_songs': SongSerializer(created_songs, many=True).data
        })

    @action(detail=True, methods=['post'])
    def add_chords(self, request, pk=None):
        """Add chord progression to a song"""
        song = self.get_object()
        chords_data = request.data.get('chords', [])
        
        if not chords_data:
            return Response(
                {'error': 'No chords data provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_chords = []
        with transaction.atomic():
            for chord_data in chords_data:
                chord_data['song'] = song.id
                serializer = ChordSerializer(data=chord_data)
                if serializer.is_valid():
                    chord = serializer.save()
                    created_chords.append(chord)
                else:
                    return Response(
                        {'error': f'Invalid chord data: {serializer.errors}'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        # Update song to indicate chords are available
        song.chords_available = True
        song.save()
        
        return Response({
            'message': f'Added {len(created_chords)} chords to {song.title}',
            'chords': ChordSerializer(created_chords, many=True).data
        })

    @action(detail=True, methods=['post'])
    def toggle_popular(self, request, pk=None):
        """Toggle popular status of a song"""
        song = self.get_object()
        song.is_popular = not song.is_popular
        song.save()
        
        return Response({
            'message': f'{song.title} is now {"popular" if song.is_popular else "not popular"}',
            'is_popular': song.is_popular
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get song statistics for admin dashboard"""
        total_songs = Song.objects.count()
        popular_songs = Song.objects.filter(is_popular=True).count()
        songs_with_chords = Song.objects.filter(chords_available=True).count()
        songs_with_tabs = Song.objects.filter(tabs_available=True).count()
        
        # Genre distribution
        genre_stats = {}
        for genre in Genre.objects.all():
            genre_stats[genre.name] = genre.songs.count()
        
        # Difficulty distribution
        difficulty_stats = {}
        for difficulty in ['beginner', 'intermediate', 'advanced']:
            difficulty_stats[difficulty] = Song.objects.filter(difficulty=difficulty).count()
        
        return Response({
            'total_songs': total_songs,
            'popular_songs': popular_songs,
            'songs_with_chords': songs_with_chords,
            'songs_with_tabs': songs_with_tabs,
            'genre_distribution': genre_stats,
            'difficulty_distribution': difficulty_stats
        })

class AdminArtistViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for managing artists"""
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        """Get all songs by an artist"""
        artist = self.get_object()
        songs = artist.songs.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

class AdminGenreViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for managing genres"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        """Get all songs in a genre"""
        genre = self.get_object()
        songs = genre.songs.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

class AdminChordDiagramViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for managing chord diagrams"""
    queryset = ChordDiagram.objects.all()
    serializer_class = ChordDiagramSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['difficulty', 'tuning']
