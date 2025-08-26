from rest_framework import serializers
from ..models import Genre

class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model"""
    class Meta:
        model = Genre
        fields = '__all__'

class GenreDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Genre with related songs"""
    from .song import SongListSerializer
    songs = SongListSerializer(many=True, read_only=True)
    
    class Meta:
        model = Genre
        fields = '__all__'
