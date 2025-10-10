from django.urls import path, include
from rest_framework.routers import DefaultRouter

# CORRECTED IMPORTS: Import only the ViewSets that actually exist
from .views import (
    GenreViewSet,
    ArtistViewSet,
    SongViewSet,
    ChordViewSet,
    ChordDiagramViewSet,
    SongRequestViewSet,
)

# Create a single router for the entire API
router = DefaultRouter()

# --- Register Public-Facing ViewSets ---
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'songs', SongViewSet, basename='song')
router.register(r'chords', ChordViewSet, basename='chord')
router.register(r'chord-diagrams', ChordDiagramViewSet, basename='chorddiagram')
router.register(r'song-requests', SongRequestViewSet, basename='songrequest')
x
urlpatterns = [
    # All generated API URLs are now included under the main router
    path('', include(router.urls)),
    
    # This provides the browsable API's login/logout views
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]