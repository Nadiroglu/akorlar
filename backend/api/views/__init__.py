# Import all views for easy access
from .genre import GenreViewSet
from .artist import ArtistViewSet
from .song import SongViewSet
from .chord import ChordViewSet
from .chord_diagram import ChordDiagramViewSet
from .admin import AdminSongViewSet, AdminArtistViewSet, AdminGenreViewSet, AdminChordDiagramViewSet
from .song_request import SongRequestViewSet, AdminSongRequestViewSet

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
