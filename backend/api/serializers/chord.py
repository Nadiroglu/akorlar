from rest_framework import serializers
from ..models import Chord

class ChordSerializer(serializers.ModelSerializer):
    """Serializer for Chord model"""
    class Meta:
        model = Chord
        fields = '__all__'
