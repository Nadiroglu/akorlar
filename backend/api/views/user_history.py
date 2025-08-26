from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from ..models import UserHistory, Song
from ..serializers.user_history import UserHistorySerializer

class UserHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user history"""
    serializer_class = UserHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['action']

    def get_queryset(self):
        return UserHistory.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def record(self, request):
        """Record a user action"""
        song_id = request.data.get('song_id')
        action = request.data.get('action', 'view')
        
        if not song_id:
            return Response({'error': 'song_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        song = get_object_or_404(Song, id=song_id)
        UserHistory.objects.create(
            user=request.user,
            song=song,
            action=action
        )
        
        # Update song play count if action is 'play'
        if action == 'play':
            song.play_count += 1
            song.save()
        
        return Response({'status': 'recorded'})
