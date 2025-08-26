# Import all serializers for easy access
from .genre import GenreSerializer, GenreDetailSerializer
from .artist import ArtistSerializer, ArtistDetailSerializer
from .song import SongSerializer, SongListSerializer, SongDetailSerializer
from .chord import ChordSerializer
from .chord_diagram import ChordDiagramSerializer
from .song_request import SongRequestSerializer, SongRequestCreateSerializer, SongRequestAdminSerializer
from .search_query import SearchQuerySerializer

__all__ = [
    'GenreSerializer',
    'GenreDetailSerializer',
    'ArtistSerializer',
    'ArtistDetailSerializer',
    'SongSerializer',
    'SongListSerializer',
    'SongDetailSerializer',
    'ChordSerializer',
    'ChordDiagramSerializer',
    'SongRequestSerializer',
    'SongRequestCreateSerializer',
    'SongRequestAdminSerializer',
    'SearchQuerySerializer',
]
