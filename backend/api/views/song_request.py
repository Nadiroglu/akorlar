from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Q
from datetime import datetime, timedelta

from ..models import SongRequest, Song
from ..serializers.song_request import (
    SongRequestSerializer, 
    SongRequestCreateSerializer, 
    SongRequestAdminSerializer
)
from ..serializers.song import SongSerializer

class SongRequestViewSet(viewsets.ModelViewSet):
    """
    A single, authoritative ViewSet for managing Song Requests.
    - Public users can create and view individual requests.
    - Admin users can list, manage, and perform actions on all requests.
    """
    queryset = SongRequest.objects.select_related('completed_song').all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'genre_name', 'user_email']
    ordering = ['-requested_at']

    def get_serializer_class(self):
        """Return the appropriate serializer based on the action and user role."""
        if self.action == 'create':
            return SongRequestCreateSerializer
        # For admins, use the detailed admin serializer for updates
        if self.action in ['update', 'partial_update'] and self.request.user.is_staff:
            return SongRequestAdminSerializer
        return SongRequestSerializer
    
    def get_permissions(self):
        """
        Set permissions dynamically based on the action.
        - 'create' and 'retrieve' are open to anyone.
        - All other actions require admin (staff) permissions.
        """
        if self.action in ['create', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        """Create a new song request (public access)."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        song_request = serializer.save()
        
        # Send confirmation and notification emails
        self._send_confirmation_email(song_request)
        self._send_admin_notification(song_request)
        
        return Response({
            'message': 'Song request submitted successfully! We will review it shortly.',
            'request_id': song_request.id,
        }, status=status.HTTP_21_CREATED)
    
    # --- Admin Actions ---

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Admin: Approve a song request."""
        song_request = self.get_object()
        if song_request.status != 'pending':
            return Response({'error': 'Only pending requests can be approved.'}, status=status.HTTP_400_BAD_REQUEST)
        
        song_request.status = 'approved'
        song_request.admin_notes = request.data.get('admin_notes', song_request.admin_notes)
        song_request.save()
        
        self._send_status_update_email(song_request, 'approved')
        
        return Response({
            'message': f'Song request "{song_request.title}" has been approved.',
            'status': song_request.status
        })
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Admin: Reject a song request."""
        song_request = self.get_object()
        if song_request.status != 'pending':
            return Response({'error': 'Only pending requests can be rejected.'}, status=status.HTTP_400_BAD_REQUEST)
            
        song_request.status = 'rejected'
        song_request.admin_notes = request.data.get('admin_notes', 'No reason provided.')
        song_request.save()
        
        self._send_status_update_email(song_request, 'rejected')
        
        return Response({
            'message': f'Song request "{song_request.title}" has been rejected.',
            'status': song_request.status
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Admin: Mark a request as completed by linking it to a new song."""
        song_request = self.get_object()
        song_id = request.data.get('song_id')
        
        if not song_id:
            return Response({'error': 'A "song_id" is required to complete the request.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({'error': f'Song with id {song_id} not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        song_request.status = 'completed'
        song_request.completed_song = song
        song_request.admin_notes = request.data.get('admin_notes', song_request.admin_notes)
        song_request.save()
        
        self._send_status_update_email(song_request, 'completed')
        
        return Response({
            'message': f'Song request "{song_request.title}" marked as completed.',
            'completed_song': SongSerializer(song).data
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Admin: Get aggregated statistics for song requests."""
        
        # Use aggregation for efficient counting
        stats_data = SongRequest.objects.aggregate(
            total_requests=Count('id'),
            pending_requests=Count('id', filter=Q(status='pending')),
            approved_requests=Count('id', filter=Q(status='approved')),
            completed_requests=Count('id', filter=Q(status='completed')),
            rejected_requests=Count('id', filter=Q(status='rejected')),
            recent_requests_30_days=Count('id', filter=Q(requested_at__gte=datetime.now() - timedelta(days=30)))
        )
        
        # Use annotation for genre distribution
        genre_distribution = {
            item['genre_name']: item['count']
            for item in SongRequest.objects.filter(genre_name__isnull=False).values('genre_name').annotate(count=Count('id')).order_by()
        }
        
        stats_data['genre_distribution'] = genre_distribution
        
        return Response(stats_data)

    # --- Helper Methods for Email ---
    
    def _send_confirmation_email(self, song_request):
        """Send a confirmation email to the user after submission."""
        try:
            subject = f"Song Request Confirmation: {song_request.title}"
            message = f"Thank you for your song request for '{song_request.title}' by {song_request.artist_name}. We have received it and will review it shortly. Your request ID is {song_request.id}."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [song_request.user_email], fail_silently=False)
        except Exception as e:
            # In a real app, log this error to a monitoring service
            print(f"ERROR: Failed to send confirmation email for request {song_request.id}: {e}")

    def _send_admin_notification(self, song_request):
        """Notify an admin of a new song request."""
        try:
            admin_email = getattr(settings, 'ADMIN_EMAIL', None)
            if not admin_email: return

            subject = f"[New Song Request] {song_request.title} by {song_request.artist_name}"
            message = f"A new song request has been submitted by {song_request.user_email}.\n\nTitle: {song_request.title}\nArtist: {song_request.artist_name}\n\nReview it in the admin panel."
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email], fail_silently=False)
        except Exception as e:
            print(f"ERROR: Failed to send admin notification for request {song_request.id}: {e}")
            
    def _send_status_update_email(self, song_request, new_status):
        """Send an email to the user when their request status changes."""
        try:
            subject = f"Update on your song request for '{song_request.title}'"
            status_messages = {
                'approved': 'Your request has been approved and is now in our queue to be added.',
                'rejected': 'Unfortunately, we are unable to fulfill your request at this time.',
                'completed': f"Great news! Your requested song, '{song_request.title}', has been added to our library."
            }
            message = f"Hi {song_request.user_name or 'there'},\n\n{status_messages.get(new_status, '')}\n\nThank you for your contribution!"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [song_request.user_email], fail_silently=False)
        except Exception as e:
            print(f"ERROR: Failed to send status update email for request {song_request.id}: {e}")
