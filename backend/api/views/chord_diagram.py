from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import ChordDiagram
from ..serializers.chord_diagram import ChordDiagramSerializer

class ChordDiagramViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public-facing ViewSet for browsing chord diagrams.
    Provides list and retrieve actions with search and filtering.
    """
    queryset = ChordDiagram.objects.all()
    serializer_class = ChordDiagramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['chord_name'] # Search by the chord name
    
    def get_queryset(self):
        """Custom filtering for chord diagrams via query parameters."""
        queryset = super().get_queryset()
        
        # Filter by tuning
        tuning = self.request.query_params.get('tuning', None)
        if tuning:
            queryset = queryset.filter(tuning__iexact=tuning)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Filter by capo friendly
        capo_friendly = self.request.query_params.get('capo_friendly', None)
        if capo_friendly:
            queryset = queryset.filter(capo_friendly=capo_friendly.lower() == 'true')
        
        return queryset
