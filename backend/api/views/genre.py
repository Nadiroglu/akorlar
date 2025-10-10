from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Genre
from ..serializers.genre import GenreSerializer, GenreDetailSerializer
# Import the lightweight SongListSerializer for better performance
from ..serializers.song import SongListSerializer

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public-facing ViewSet for browsing genres.
    Provides list and retrieve actions with search and ordering.
    """
    queryset = Genre.objects.prefetch_related('songs').all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']

    def get_serializer_class(self):
        """Use a more detailed serializer for the retrieve action."""
        if self.action == 'retrieve':
            return GenreDetailSerializer
        return GenreSerializer

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        """Get all songs for a specific genre."""
        genre = self.get_object()
        songs = genre.songs.all()
        
        # OPTIMIZATION: Use the lightweight SongListSerializer.
        # This avoids sending all the chord data for every song in the list,
        # making the API response much smaller and faster.
        serializer = SongListSerializer(songs, many=True)
        return Response(serializer.data)
