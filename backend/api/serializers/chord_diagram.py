from rest_framework import serializers
from ..models import ChordDiagram

class ChordDiagramSerializer(serializers.ModelSerializer):
    """Serializer for ChordDiagram model"""
    class Meta:
        model = ChordDiagram
        fields = '__all__'
