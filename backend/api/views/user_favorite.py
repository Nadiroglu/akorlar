from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from ..models import UserFavorite, Song
from ..serializers.user_favorite import UserFavoriteSerializer

class UserFavoriteViewSet(viewsets.ModelViewSet):
    """ViewSet for user favorites"""
    serializer_class = UserFavoriteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['song']

    def get_queryset(self):
        return UserFavorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle favorite status for a song"""
        song_id = request.data.get('song_id')
        if not song_id:
            return Response({'error': 'song_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        song = get_object_or_404(Song, id=song_id)
        favorite, created = UserFavorite.objects.get_or_create(
            user=request.user,
            song=song
        )
        
        if not created:
            favorite.delete()
            return Response({'status': 'removed'})
        
        return Response({'status': 'added'})
