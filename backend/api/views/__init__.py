# Import all views for easy access
from .genre import GenreViewSet
from .artist import ArtistViewSet
from .song import SongViewSet
from .chord import ChordViewSet
from .chord_diagram import ChordDiagramViewSet
from .song_request import SongRequestViewSet

__all__ = [
    'GenreViewSet',
    'ArtistViewSet',
    'SongViewSet',
    'ChordViewSet',
    'ChordDiagramViewSet',
    'SongRequestViewSet',
]

