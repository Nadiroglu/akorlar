#!/usr/bin/env python
"""
Advanced Chord API Views for Akorlar
Supports transposition, capo, and dynamic chord operations
"""

from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.db.models import Q

from api.models import Song, Chord, ChordDiagram
from api.serializers import ChordSerializer, SongSerializer
from api.utils.music_theory import music_engine


class ChordViewSet(ModelViewSet):
    """Advanced Chord ViewSet with transposition and capo support"""
    queryset = Chord.objects.all()
    serializer_class = ChordSerializer
    
    @action(detail=False, methods=['get'])
    def by_song(self, request):
        """Get chords for a specific song with optional transposition"""
        song_id = request.query_params.get('song_id')
        transpose = int(request.query_params.get('transpose', 0))
        capo = int(request.query_params.get('capo', 0))
        
        if not song_id:
            return Response(
                {"error": "song_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            song = Song.objects.get(id=song_id)
            chords = Chord.objects.filter(song=song).order_by('position')
            
            if transpose != 0 or capo != 0:
                # Apply transposition and capo
                chord_data = ChordSerializer(chords, many=True).data
                modified_chords = self._apply_transposition_and_capo(chord_data, transpose, capo)
                return Response({
                    "song": SongSerializer(song).data,
                    "chords": modified_chords,
                    "transpose": transpose,
                    "capo": capo
                })
            
            return Response({
                "song": SongSerializer(song).data,
                "chords": ChordSerializer(chords, many=True).data
            })
            
        except Song.DoesNotExist:
            return Response(
                {"error": "Song not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def transpose_song(self, request):
        """Transpose all chords in a song"""
        song_id = request.data.get('song_id')
        semitones = int(request.data.get('semitones', 0))
        
        if not song_id:
            return Response(
                {"error": "song_id and semitones are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            song = Song.objects.get(id=song_id)
            chords = Chord.objects.filter(song=song).order_by('position')
            
            # Get original chord data
            chord_data = ChordSerializer(chords, many=True).data
            
            # Apply transposition
            transposed_chords = music_engine.transpose_progression(chord_data, semitones)
            
            return Response({
                "song": SongSerializer(song).data,
                "original_chords": chord_data,
                "transposed_chords": transposed_chords,
                "semitones": semitones
            })
            
        except Song.DoesNotExist:
            return Response(
                {"error": "Song not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def progression_types(self, request):
        """Get available chord progression types"""
        return Response({
            "progression_types": list(music_engine.COMMON_PROGRESSIONS.keys()),
            "descriptions": {
                "pop": "Standard pop progression (I-vi-IV-V)",
                "folk": "Folk music progression (I-V-vi-IV)",
                "jazz": "Jazz progression (ii-V-I-vi)",
                "blues": "Blues progression (I-IV-I-V-IV-I)",
                "turkish_pop": "Turkish pop style (i-VII-VI-V)",
                "turkish_folk": "Turkish folk style (i-v-VI-III)",
                "arabesk": "Arabesk style (i-VII-VI-V-i)"
            }
        })
    
    @action(detail=False, methods=['post'])
    def generate_progression(self, request):
        """Generate a new chord progression"""
        key = request.data.get('key', 'C')
        progression_type = request.data.get('progression_type', 'pop')
        bars = int(request.data.get('bars', 4))
        beats_per_bar = int(request.data.get('beats_per_bar', 4))
        
        try:
            progression = music_engine.generate_progression(
                key=key,
                progression_type=progression_type,
                bars=bars,
                beats_per_bar=beats_per_bar
            )
            
            return Response({
                "key": key,
                "progression_type": progression_type,
                "bars": bars,
                "beats_per_bar": beats_per_bar,
                "progression": progression
            })
            
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _apply_transposition_and_capo(self, chord_data, transpose, capo):
        """Apply transposition and capo to chord data"""
        modified_chords = []
        
        for chord in chord_data:
            chord_name = chord['chord_name']
            
            # Extract root note
            root_note = chord_name[0]
            if len(chord_name) > 1 and chord_name[1] in ['#', 'b']:
                root_note = chord_name[:2]
            
            # Apply transposition and capo
            total_semitones = transpose + capo
            new_root = music_engine.transpose_note(root_note, total_semitones)
            
            # Reconstruct chord name
            if chord_name.startswith(root_note):
                new_chord_name = chord_name.replace(root_note, new_root, 1)
            else:
                new_chord_name = new_root + chord_name[1:]
            
            modified_chord = chord.copy()
            modified_chord['chord_name'] = new_chord_name
            modified_chord['transposed'] = True
            modified_chord['transpose_semitones'] = transpose
            modified_chord['capo_fret'] = capo
            
            modified_chords.append(modified_chord)
        
        return modified_chords


@api_view(['GET'])
def song_chords(request, song_id):
    """Get chords for a specific song with advanced options"""
    transpose = int(request.query_params.get('transpose', 0))
    capo = int(request.query_params.get('capo', 0))
    include_diagrams = request.query_params.get('include_diagrams', 'false').lower() == 'true'
    
    try:
        song = get_object_or_404(Song, id=song_id)
        chords = Chord.objects.filter(song=song).order_by('position')
        
        # Get chord diagrams if requested
        diagrams = {}
        if include_diagrams:
            chord_names = [chord.chord_name for chord in chords]
            chord_diagrams = ChordDiagram.objects.filter(chord_name__in=chord_names)
            for diagram in chord_diagrams:
                diagrams[diagram.chord_name] = {
                    'fret_positions': diagram.fret_positions,
                    'fingers': diagram.fingers,
                    'difficulty': diagram.difficulty,
                    'capo_friendly': diagram.capo_friendly
                }
        
        # Apply transposition and capo if specified
        if transpose != 0 or capo != 0:
            chord_data = ChordSerializer(chords, many=True).data
            modified_chords = []
            
            for chord in chord_data:
                chord_name = chord['chord_name']
                root_note = chord_name[0]
                if len(chord_name) > 1 and chord_name[1] in ['#', 'b']:
                    root_note = chord_name[:2]
                
                total_semitones = transpose + capo
                new_root = music_engine.transpose_note(root_note, total_semitones)
                
                if chord_name.startswith(root_note):
                    new_chord_name = chord_name.replace(root_note, new_root, 1)
                else:
                    new_chord_name = new_root + chord_name[1:]
                
                modified_chord = chord.copy()
                modified_chord['chord_name'] = new_chord_name
                modified_chord['transposed'] = True
                modified_chord['transpose_semitones'] = transpose
                modified_chord['capo_fret'] = capo
                
                modified_chords.append(modified_chord)
            
            chords_data = modified_chords
        else:
            chords_data = ChordSerializer(chords, many=True).data
        
        return Response({
            "song": SongSerializer(song).data,
            "chords": chords_data,
            "chord_diagrams": diagrams if include_diagrams else None,
            "transpose": transpose,
            "capo": capo,
            "total_chords": len(chords_data)
        })
        
    except Exception as e:
        return Response(
            {"error": str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
