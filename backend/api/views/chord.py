from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Chord
from ..serializers.chord import (
    ChordSerializer,
    ChordProgressionSerializer,
    ChordTranspositionSerializer, # Assuming this is for the preview
)
# This was missing from your provided file
from ..utils.music_theory import music_engine


class ChordViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A single, authoritative ViewSet for Chords.

    Provides a comprehensive list/retrieve endpoint with powerful filtering,
    search, and transposition previews. Also includes utility actions for
    generating progressions.
    """
    queryset = Chord.objects.select_related('song')
    serializer_class = ChordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['chord_name', 'root', 'quality', 'roman_numeral']
    
    def get_queryset(self):
        """Enhanced filtering via query parameters."""
        queryset = super().get_queryset()
        
        # Filter by song ID
        song_id = self.request.query_params.get('song', None)
        if song_id:
            queryset = queryset.filter(song_id=song_id)
        
        # Filter by root note
        root = self.request.query_params.get('root', None)
        if root:
            queryset = queryset.filter(root=root)
        
        # Filter by chord quality
        quality = self.request.query_params.get('quality', None)
        if quality:
            queryset = queryset.filter(quality=quality)
        
        return queryset

    def list(self, request, *args, **kwargs):
        """
        Overrides the default list action to support transposition previews
        via query parameters. This replaces the need for a custom 'by_song' action.
        """
        # 1. Get transposition parameters from the URL query
        transpose = int(request.query_params.get('transpose', 0))
        capo = int(request.query_params.get('capo', 0))
        
        # 2. Get the filtered queryset (this calls get_queryset automatically)
        queryset = self.filter_queryset(self.get_queryset())
        
        # 3. Prepare context to pass to the serializer
        context = self.get_serializer_context()
        context['semitones'] = transpose + capo
        
        # 4. Serialize the data with the context
        serializer = self.get_serializer(queryset, many=True, context=context)
        
        # 5. Construct the final response
        return Response({
            'count': queryset.count(),
            'transpose': transpose,
            'capo': capo,
            'chords': serializer.data,
        })

    @action(detail=False, methods=['post'], url_path='preview-transposition')
    def preview_transposition(self, request):
        """
        Provides a non-destructive preview of a transposed song.
        Note: The main `list` action can also do this with GET parameters.
        """
        # Use raise_exception=True for cleaner validation
        serializer = ChordTranspositionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.get_transposed_song()
        return Response(result)
    
    @action(detail=False, methods=['get'], url_path='progression-types')
    def progression_types(self, request):
        """Get available chord progression types."""
        # This data can be static if it doesn't change often
        return Response({
            "progression_types": list(music_engine.COMMON_PROGRESSIONS.keys()),
            "descriptions": {
                "pop": "Standard pop progression (I-V-vi-IV)",
                "jazz": "Jazz progression (ii-V-I-vi)",
                "blues": "Blues progression (I-IV-V-I)",
                "turkish_pop": "Turkish pop style (i-VII-VI-V)",
            }
        })
    
    @action(detail=False, methods=['post'], url_path='generate-progression')
    def generate_progression(self, request):
        """Generate a new chord progression using the music engine."""
        serializer = ChordProgressionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.generate_progression()
        return Response(result)

