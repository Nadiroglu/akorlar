from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from ..models import Song, SearchQuery
from ..serializers.song import SongSerializer, SongListSerializer, SongDetailSerializer

class SongViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for songs"""
    queryset = Song.objects.select_related('artist', 'genre').prefetch_related('chords')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'artist__name', 'lyrics']
    ordering_fields = ['title', 'created_at', 'play_count', 'rating', 'year']
    ordering = ['-created_at']
    filterset_fields = ['genre', 'difficulty', 'key', 'chords_available', 'tabs_available', 'is_popular']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SongDetailSerializer
        return SongSerializer

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular songs"""
        popular_songs = self.queryset.filter(is_popular=True).order_by('-play_count')[:20]
        serializer = self.get_serializer(popular_songs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search for songs"""
        query = request.query_params.get('q', '')
        genre = request.query_params.get('genre', '')
        difficulty = request.query_params.get('difficulty', '')
        key = request.query_params.get('key', '')
        
        queryset = self.queryset
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(artist__name__icontains=query) |
                Q(lyrics__icontains=query)
            )
        
        if genre:
            queryset = queryset.filter(genre__name__iexact=genre)
        
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        if key:
            queryset = queryset.filter(key__iexact=key)
        
        # Track search query
        if query and request.user.is_authenticated:
            SearchQuery.objects.create(
                query=query,
                user=request.user,
                results_count=queryset.count()
            )
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def chords(self, request, pk=None):
        """Get chords for a specific song"""
        song = self.get_object()
        chords = song.chords.all()
        from ..serializers.chord import ChordSerializer
        serializer = ChordSerializer(chords, many=True)
        return Response(serializer.data)
