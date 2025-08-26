# Import all serializers from separate files
from .serializers.genre import GenreSerializer, GenreDetailSerializer
from .serializers.artist import ArtistSerializer, ArtistDetailSerializer
from .serializers.song import SongSerializer, SongListSerializer, SongDetailSerializer
from .serializers.chord import ChordSerializer
from .serializers.chord_diagram import ChordDiagramSerializer
from .serializers.song_request import SongRequestSerializer, SongRequestCreateSerializer, SongRequestAdminSerializer
from .serializers.search_query import SearchQuerySerializer

# Re-export all serializers for backward compatibility
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
