from rest_framework import serializers
from ..models import Chord, Song, ChordDiagram
from api.utils.music_theory import music_engine


class ChordSerializer(serializers.ModelSerializer):
    """
    Serializer for the Chord model.

    This serializer has a special capability: when a 'semitones' integer is
    passed into its context, it will dynamically add transposed information
    to the representation without altering the original model instance.
    """
    class Meta:
        model = Chord
        # Using '__all__' is convenient, but for production it's often better to
        # explicitly list the fields you want to expose.
        fields = '__all__'

    def to_representation(self, instance):
        """
        Override the default representation to dynamically add transposed data.
        This method uses the model's own robust methods for transposition,
        avoiding fragile string parsing.
        """
        # Start with the default serialized data (a dictionary)
        data = super().to_representation(instance)

        # Check if transposition is requested in the serializer's context
        if 'semitones' in self.context:
            semitones = self.context.get('semitones', 0)

            if semitones != 0:
                # 1. Use the robust model INSTANCE method to get the new root.
                new_root = instance.transpose(semitones)

                # 2. Use the model INSTANCE to generate the new chord name.
                # This requires temporarily changing the root on the instance.
                original_root = instance.root
                instance.root = new_root
                new_chord_name = instance.generate_chord_name()
                instance.root = original_root  # IMPORTANT: Reset the instance state!

                # 3. Add the new, dynamic data to the output dictionary.
                data['transposed_root'] = new_root
                data['transposed_chord_name'] = new_chord_name
                data['is_transposed'] = True
                data['semitones_applied'] = semitones

        return data


class ChordTranspositionSerializer(serializers.Serializer):
    """
    A non-model "service" serializer to handle the complex logic for the
    'by_song' action. It validates input and orchestrates data fetching
    and serialization.
    """
    song_id = serializers.IntegerField(required=True)
    transpose = serializers.IntegerField(default=0, min_value=-12, max_value=12)
    capo = serializers.IntegerField(default=0, min_value=0, max_value=12)
    include_diagrams = serializers.BooleanField(default=False)

    def validate_song_id(self, value):
        """Validate that the song exists in the database."""
        if not Song.objects.filter(id=value).exists():
            raise serializers.ValidationError("Song with the provided ID not found.")
        return value

    def get_response_data(self):
        """
        Fetches all necessary data and returns a structured dictionary
        ready to be sent as an API response.
        """
        validated_data = self.validated_data
        song_id = validated_data['song_id']
        transpose = validated_data['transpose']
        capo = validated_data['capo']
        include_diagrams = validated_data['include_diagrams']
        total_semitones = transpose + capo

        # Get the song and its chords
        song = Song.objects.get(id=song_id)
        chords_queryset = Chord.objects.filter(song=song).order_by('measure', 'beat', 'sub_beat')

        # Prepare context for our main ChordSerializer
        context = {'semitones': total_semitones}
        
        # Serialize chords, passing the context to trigger transposition
        chords_data = ChordSerializer(chords_queryset, many=True, context=context).data

        # Get chord diagrams if requested
        diagrams = {}
        if include_diagrams:
            # Fetch diagrams based on the *original* chord names for efficiency
            original_chord_names = chords_queryset.values_list('chord_name', flat=True).distinct()
            chord_diagrams = ChordDiagram.objects.filter(chord_name__in=original_chord_names)
            for diagram in chord_diagrams:
                diagrams[diagram.chord_name] = {
                    'frets': diagram.frets,
                    'fingers': diagram.fingers,
                    'difficulty': diagram.difficulty,
                }

        # Assemble the final response payload
        return {
            'song': SongSerializer(song).data,
            'chords': chords_data,
            'chord_diagrams': diagrams if include_diagrams else None,
            'transpose_value': transpose,
            'capo_fret': capo,
            'total_chords': len(chords_data)
        }


class ChordProgressionSerializer(serializers.Serializer):
    """Serializer for validating and generating chord progressions."""
    key = serializers.CharField(max_length=10, default='C')
    progression_type = serializers.CharField(max_length=20, default='pop')
    bars = serializers.IntegerField(default=4, min_value=1, max_value=16)
    beats_per_bar = serializers.IntegerField(default=4, min_value=1, max_value=8)

    def validate_progression_type(self, value):
        """Validate that the progression type is supported by the music engine."""
        if value not in music_engine.COMMON_PROGRESSIONS:
            raise serializers.ValidationError(f"Invalid progression type.")
        return value

    def generate(self):
        """Generate the chord progression using the music engine."""
        data = self.validated_data
        try:
            progression = music_engine.generate_progression(
                key=data['key'],
                progression_type=data['progression_type'],
                bars=data['bars'],
                beats_per_bar=data['beats_per_bar']
            )
            data['progression'] = progression
            return data
        except ValueError as e:
            raise serializers.ValidationError(str(e))