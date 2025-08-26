from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..models import Genre
from ..serializers.genre import GenreSerializer, GenreDetailSerializer

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for genres"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GenreDetailSerializer
        return GenreSerializer

    @action(detail=True, methods=['get'])
    def songs(self, request, pk=None):
        """Get all songs for a specific genre"""
        genre = self.get_object()
        songs = genre.songs.all()
        from ..serializers.song import SongSerializer
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)
