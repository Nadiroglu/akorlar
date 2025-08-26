from rest_framework import serializers
from ..models import SongRequest, Song
from .song import SongListSerializer

class SongRequestSerializer(serializers.ModelSerializer):
    """Serializer for SongRequest model"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    days_since_request = serializers.SerializerMethodField()
    
    class Meta:
        model = SongRequest
        fields = [
            'id', 'title', 'artist_name', 'genre_name', 'user_email', 
            'user_name', 'additional_notes', 'status', 'status_display',
            'admin_notes', 'requested_at', 'updated_at', 'completed_song',
            'days_since_request'
        ]
        read_only_fields = ['id', 'status', 'admin_notes', 'requested_at', 'updated_at', 'completed_song', 'days_since_request']

    def get_days_since_request(self, obj):
        """Calculate days since request was made"""
        from datetime import datetime
        delta = datetime.now().replace(tzinfo=None) - obj.requested_at.replace(tzinfo=None)
        return delta.days

class SongRequestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating song requests (public access)"""
    
    class Meta:
        model = SongRequest
        fields = [
            'title', 'artist_name', 'genre_name', 'user_email', 
            'user_name', 'additional_notes'
        ]
    
    def validate_title(self, value):
        """Validate song title"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Song title must be at least 2 characters long.")
        return value.strip()
    
    def validate_artist_name(self, value):
        """Validate artist name"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Artist name must be at least 2 characters long.")
        return value.strip()
    
    def validate_user_email(self, value):
        """Validate user email"""
        # Check if user has made too many recent requests
        from datetime import datetime, timedelta
        recent_requests = SongRequest.objects.filter(
            user_email=value,
            requested_at__gte=datetime.now() - timedelta(days=7)
        ).count()
        
        if recent_requests >= 5:
            raise serializers.ValidationError("You have made too many requests recently. Please wait before making another request.")
        
        return value.lower()

class SongRequestAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin management of song requests"""
    completed_song_details = SongListSerializer(source='completed_song', read_only=True)
    
    class Meta:
        model = SongRequest
        fields = '__all__'
    
    def update(self, instance, validated_data):
        """Handle status updates and admin notes"""
        # If status is being updated to 'completed', ensure completed_song is set
        if 'status' in validated_data and validated_data['status'] == 'completed':
            if not validated_data.get('completed_song') and not instance.completed_song:
                raise serializers.ValidationError(
                    "A completed song must be linked when marking request as completed."
                )
        
        return super().update(instance, validated_data)
