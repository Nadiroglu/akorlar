from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router and register viewsets
router = DefaultRouter()

# Public API endpoints
router.register(r'api/genres', views.GenreViewSet)
router.register(r'api/artists', views.ArtistViewSet)
router.register(r'api/songs', views.SongViewSet)
router.register(r'api/chords', views.ChordViewSet)
router.register(r'api/chord-diagrams', views.ChordDiagramViewSet)
router.register(r'api/song-requests', views.SongRequestViewSet)

# Admin API endpoints
router.register(r'api/admin/songs', views.AdminSongViewSet, basename='admin-songs')
router.register(r'api/admin/artists', views.AdminArtistViewSet, basename='admin-artists')
router.register(r'api/admin/genres', views.AdminGenreViewSet, basename='admin-genres')
router.register(r'api/admin/chord-diagrams', views.AdminChordDiagramViewSet, basename='admin-chord-diagrams')
router.register(r'api/admin/song-requests', views.AdminSongRequestViewSet, basename='admin-song-requests')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
