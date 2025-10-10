# api/views/song.py

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
# Authentication has been removed for now
# from rest_framework.permissions import IsAuthenticated

from ..models import Song, SearchQuery
# Import the SongListSerializer to use it in the ViewSet
from ..serializers.song import SongSerializer, SongListSerializer, SongDetailSerializer

class SongViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A single, authoritative ViewSet for Songs.

    Provides a comprehensive list/retrieve endpoint with powerful filtering,
    search, and ordering capabilities. Also includes a public action for
    permanently transposing a song.
    """
    queryset = Song.objects.select_related('artist', 'genre').prefetch_related('chords')
    # permission_classes have been removed to allow public access.
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'artist__name', 'lyrics']
    ordering_fields = ['title', 'created_at', 'play_count', 'rating', 'year']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Use a simplified serializer for the list action and a detailed
        serializer for the retrieve action to optimize performance.
        """
        if self.action == 'list':
            return SongListSerializer
        if self.action == 'retrieve':
            return SongDetailSerializer
        # Use the base SongSerializer as a fallback for other actions (e.g., transpose)
        return SongSerializer

    def get_queryset(self):
        """Custom filtering via query parameters using if-statements."""
        queryset = super().get_queryset()
        
        # Filter by genre
        genre = self.request.query_params.get('genre', None)
        if genre:
            queryset = queryset.filter(genre__name__iexact=genre)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by key
        key = self.request.query_params.get('key', None)
        if key:
            queryset = queryset.filter(key__iexact=key)
        
        # Filter by chords available
        chords_available = self.request.query_params.get('chords_available', None)
        if chords_available:
            queryset = queryset.filter(chords_available=chords_available.lower() == 'true')
        
        # Filter by tabs available
        tabs_available = self.request.query_params.get('tabs_available', None)
        if tabs_available:
            queryset = queryset.filter(tabs_available=tabs_available.lower() == 'true')
        
        # Filter by popular
        is_popular = self.request.query_params.get('is_popular', None)
        if is_popular:
            queryset = queryset.filter(is_popular=is_popular.lower() == 'true')
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Overrides the default list action to track search queries.
        """
        queryset = self.filter_queryset(self.get_queryset())
        
        # Track search query if a search term is present
        search_term = request.query_params.get('search', None)
        if search_term:
            # Authentication check removed for search query tracking
            SearchQuery.objects.create(
                query=search_term,
                results_count=queryset.count(),
                ip_address=request.META.get('REMOTE_ADDR') # Example of getting IP
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post']) # permission_classes removed
    def transpose(self, request, pk=None):
        """
        Permanently transposes a song to the target key.
        This is a destructive action and is currently public.
        """
        song = self.get_object()
        target_key = request.data.get('key')

        if not target_key:
            return Response(
                {'error': 'Target key ("key") is required in the request body.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Correctly capture both return values from the model method
        success, message = song.transpose_to_key(target_key)

        if success:
            serializer = self.get_serializer(song)
            return Response({
                'message': message, # Use the detailed message from the model
                'song': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            # Return a detailed error message from the model
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )