from rest_framework import serializers
from ..models import Song

class SongSerializer(serializers.ModelSerializer):
    """Basic serializer for Song model"""
    artist = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    chords = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = '__all__'
    
    def get_artist(self, obj):
        """Get artist data without circular import"""
        from .artist import ArtistSerializer
        return ArtistSerializer(obj.artist, read_only=True).data if obj.artist else None
    
    def get_genre(self, obj):
        """Get genre data without circular import"""
        from .genre import GenreSerializer
        return GenreSerializer(obj.genre, read_only=True).data if obj.genre else None
    
    def get_chords(self, obj):
        """Get chords data without circular import"""
        from .chord import ChordSerializer
        return ChordSerializer(obj.chords.all(), many=True, read_only=True).data

class SongListSerializer(serializers.ModelSerializer):
    """Simplified serializer for song lists"""
    artist = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = [
            'id', 'title', 'artist', 'genre', 'difficulty',
            'year', 'duration', 'key', 'tempo', 'chords_available',
            'tabs_available', 'is_popular', 'play_count', 'rating',
            'created_at'
        ]
    
    def get_artist(self, obj):
        """Get artist data without circular import"""
        from .artist import ArtistSerializer
        return ArtistSerializer(obj.artist, read_only=True).data if obj.artist else None
    
    def get_genre(self, obj):
        """Get genre data without circular import"""
        from .genre import GenreSerializer
        return GenreSerializer(obj.genre, read_only=True).data if obj.genre else None

class SongDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Song with full relationships"""
    artist = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    chords = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = '__all__'
    
    def get_artist(self, obj):
        """Get artist data without circular import"""
        from .artist import ArtistSerializer
        return ArtistSerializer(obj.artist, read_only=True).data if obj.artist else None
    
    def get_genre(self, obj):
        """Get genre data without circular import"""
        from .genre import GenreSerializer
        return GenreSerializer(obj.genre, read_only=True).data if obj.genre else None
    
    def get_chords(self, obj):
        """Get chords data without circular import"""
        from .chord import ChordSerializer
        return ChordSerializer(obj.chords.all(), many=True, read_only=True).data
