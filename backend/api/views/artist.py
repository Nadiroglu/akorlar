from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Artist
from ..serializers.artist import ArtistSerializer, ArtistDetailSerializer

class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for artists"""
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'bio', 'country']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    filterset_fields = ['country']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArtistDetailSerializer
        return ArtistSerializer

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        """Get all songs for a specific artist"""
        artist = self.get_object()
        songs = artist.songs.all()
        from ..serializers.song import SongSerializer
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
