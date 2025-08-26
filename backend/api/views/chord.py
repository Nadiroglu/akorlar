from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Chord
from ..serializers.chord import ChordSerializer

class ChordViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for chords"""
    queryset = Chord.objects.select_related('song')
    serializer_class = ChordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['song', 'chord_name', 'bar']
