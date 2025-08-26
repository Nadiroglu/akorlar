from rest_framework import serializers
from ..models import Artist

class ArtistSerializer(serializers.ModelSerializer):
    """Serializer for Artist model"""
    class Meta:
        model = Artist
        fields = '__all__'

class ArtistDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Artist with related songs"""
    songs = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = '__all__'
    
    def get_songs(self, obj):
        """Get songs for this artist without circular import"""
        from .song import SongListSerializer
        return SongListSerializer(obj.songs.all(), many=True, read_only=True).data
