from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Artist
from ..serializers.artist import ArtistSerializer, ArtistDetailSerializer
# Reverting to the standard SongSerializer as requested.
# Note: For better performance, a lightweight serializer (like SongListSerializer)
# that omits the 'chords' field is recommended for this list view.
from ..serializers.song import SongSerializer 

class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public-facing ViewSet for browsing artists.
    Provides list and retrieve actions with search, ordering, and filtering.
    """
    queryset = Artist.objects.prefetch_related('songs').all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Reverting filter_backends to remove DjangoFilterBackend
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    search_fields = ['name', 'bio', 'country']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        """Custom filtering via query parameters using if-statements."""
        queryset = super().get_queryset()
        
        # Filter by country (case-insensitive)
        country = self.request.query_params.get('country', None)
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        return queryset

    def get_serializer_class(self):
        """Use a more detailed serializer for the retrieve action."""
        if self.action == 'retrieve':
            return ArtistDetailSerializer
        return ArtistSerializer

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        """Get all songs for a specific artist."""
        artist = self.get_object()
        songs = artist.songs.all()
        
        # Using the standard SongSerializer as requested.
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

