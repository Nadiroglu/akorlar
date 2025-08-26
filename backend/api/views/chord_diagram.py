from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ChordDiagram
from ..serializers.chord_diagram import ChordDiagramSerializer

class ChordDiagramViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for chord diagrams"""
    queryset = ChordDiagram.objects.all()
    serializer_class = ChordDiagramSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['chord_name']
    filterset_fields = ['tuning', 'difficulty']
