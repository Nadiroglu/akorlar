from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from ..models import SongRequest, Song, Artist, Genre
from ..serializers.song_request import (
    SongRequestSerializer, 
    SongRequestCreateSerializer, 
    SongRequestAdminSerializer
)
from ..serializers.song import SongSerializer

class SongRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for song requests - public creation, admin management"""
    queryset = SongRequest.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'genre_name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SongRequestCreateSerializer
        elif self.action in ['update', 'partial_update'] and self.request.user.is_staff:
            return SongRequestAdminSerializer
        return SongRequestSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Create a new song request (public access)"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            song_request = serializer.save()
            
            # Send confirmation email to user
            try:
                self.send_confirmation_email(song_request)
            except Exception as e:
                # Log error but don't fail the request
                print(f"Failed to send confirmation email: {e}")
            
            # Send notification to admin
            try:
                self.send_admin_notification(song_request)
            except Exception as e:
                print(f"Failed to send admin notification: {e}")
            
            return Response({
                'message': 'Song request submitted successfully! We will review it and get back to you.',
                'request_id': song_request.id,
                'status': song_request.status
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_confirmation_email(self, song_request):
        """Send confirmation email to user"""
        subject = f"Song Request Confirmation: {song_request.title}"
        message = f"""
        Thank you for your song request!
        
        Song: {song_request.title}
        Artist: {song_request.artist_name}
        Genre: {song_request.genre_name or 'Not specified'}
        
        We have received your request and will review it. You will be notified once we have an update.
        
        Request ID: {song_request.id}
        Submitted: {song_request.requested_at.strftime('%B %d, %Y')}
        
        Best regards,
        Turkish Music Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[song_request.user_email],
            fail_silently=True
        )
    
    def send_admin_notification(self, song_request):
        """Send notification to admin about new request"""
        subject = f"New Song Request: {song_request.title}"
        message = f"""
        New song request received:
        
        Song: {song_request.title}
        Artist: {song_request.artist_name}
        Genre: {song_request.genre_name or 'Not specified'}
        User: {song_request.user_name or 'Anonymous'} ({song_request.user_email})
        Notes: {song_request.additional_notes or 'None'}
        
        Request ID: {song_request.id}
        Submitted: {song_request.requested_at.strftime('%B %d, %Y at %H:%M')}
        
        Review at: {settings.SITE_URL}/admin/api/songrequest/{song_request.id}/
        """
        
        # Send to admin email (configure in settings)
        admin_email = getattr(settings, 'ADMIN_EMAIL', settings.DEFAULT_FROM_EMAIL)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=True
        )

class AdminSongRequestViewSet(viewsets.ModelViewSet):
    """Admin ViewSet for managing song requests"""
    queryset = SongRequest.objects.all()
    serializer_class = SongRequestAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'genre_name', 'user_email']
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a song request"""
        song_request = self.get_object()
        
        if song_request.status != 'pending':
            return Response(
                {'error': 'Only pending requests can be approved'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        song_request.status = 'approved'
        song_request.admin_notes = request.data.get('admin_notes', '')
        song_request.save()
        
        # Send approval email to user
        self.send_status_update_email(song_request, 'approved')
        
        return Response({
            'message': f'Song request "{song_request.title}" has been approved',
            'status': song_request.status
        })
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a song request"""
        song_request = self.get_object()
        
        if song_request.status != 'pending':
            return Response(
                {'error': 'Only pending requests can be rejected'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        song_request.status = 'rejected'
        song_request.admin_notes = request.data.get('admin_notes', '')
        song_request.save()
        
        # Send rejection email to user
        self.send_status_update_email(song_request, 'rejected')
        
        return Response({
            'message': f'Song request "{song_request.title}" has been rejected',
            'status': song_request.status
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a song request as completed by linking it to a created song"""
        song_request = self.get_object()
        song_id = request.data.get('song_id')
        
        if not song_id:
            return Response(
                {'error': 'song_id is required to mark request as completed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {'error': 'Song not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        song_request.status = 'completed'
        song_request.completed_song = song
        song_request.admin_notes = request.data.get('admin_notes', '')
        song_request.save()
        
        # Send completion email to user
        self.send_status_update_email(song_request, 'completed')
        
        return Response({
            'message': f'Song request "{song_request.title}" has been marked as completed',
            'status': song_request.status,
            'completed_song': SongSerializer(song).data
        })
    
    def send_status_update_email(self, song_request, status):
        """Send status update email to user"""
        status_messages = {
            'approved': 'Your song request has been approved and is now in our queue for processing.',
            'rejected': 'Your song request has been reviewed but cannot be fulfilled at this time.',
            'completed': 'Great news! Your requested song has been added to our database.'
        }
        
        subject = f"Song Request Update: {song_request.title}"
        message = f"""
        Your song request has been updated:
        
        Song: {song_request.title}
        Artist: {song_request.artist_name}
        Status: {song_request.get_status_display()}
        
        {status_messages.get(status, 'Your request status has been updated.')}
        
        {f'Admin Notes: {song_request.admin_notes}' if song_request.admin_notes else ''}
        
        Request ID: {song_request.id}
        
        Best regards,
        Turkish Music Team
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[song_request.user_email],
            fail_silently=True
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get song request statistics for admin dashboard"""
        total_requests = SongRequest.objects.count()
        pending_requests = SongRequest.objects.filter(status='pending').count()
        approved_requests = SongRequest.objects.filter(status='approved').count()
        completed_requests = SongRequest.objects.filter(status='completed').count()
        rejected_requests = SongRequest.objects.filter(status='rejected').count()
        
        # Recent requests (last 30 days)
        from datetime import datetime, timedelta
        recent_requests = SongRequest.objects.filter(
            requested_at__gte=datetime.now() - timedelta(days=30)
        ).count()
        
        # Genre distribution
        genre_stats = {}
        for request in SongRequest.objects.filter(genre_name__isnull=False):
            genre = request.genre_name
            genre_stats[genre] = genre_stats.get(genre, 0) + 1
        
        return Response({
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'approved_requests': approved_requests,
            'completed_requests': completed_requests,
            'rejected_requests': rejected_requests,
            'recent_requests_30_days': recent_requests,
            'genre_distribution': genre_stats
        })
