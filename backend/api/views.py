# Import all views from separate files
from .views.genre import GenreViewSet
from .views.artist import ArtistViewSet
from .views.song import SongViewSet
from .views.chord import ChordViewSet
from .views.chord_diagram import ChordDiagramViewSet
from .views.admin import AdminSongViewSet, AdminArtistViewSet, AdminGenreViewSet, AdminChordDiagramViewSet
from .views.song_request import SongRequestViewSet, AdminSongRequestViewSet

# Re-export all views for backward compatibility
__all__ = [
    'GenreViewSet',
    'ArtistViewSet',
    'SongViewSet',
    'ChordViewSet',
    'ChordDiagramViewSet',
    'AdminSongViewSet',
    'AdminArtistViewSet',
    'AdminGenreViewSet',
    'AdminChordDiagramViewSet',
    'SongRequestViewSet',
    'AdminSongRequestViewSet',
]
