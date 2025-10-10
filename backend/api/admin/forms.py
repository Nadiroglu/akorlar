from django import forms
from api.models import Song, Chord


class SongForm(forms.ModelForm):

    is_popular = forms.BooleanField(required=False)
    play_count = forms.IntegerField(initial=0)
    rating = forms.FloatField(initial=0.0)


    class Meta:

        model = Song

        fields = [
            'title', 'artist', 'genre', 'key', 'difficulty', 'year', 'tempo', 
            'duration', 'lyrics', 'is_popular', 'play_count', 'rating',
            'tabs_available' # Assuming you want to edit this too
        ]

        widgets = {
            'lyrics': forms.Textarea(attrs={'rows': 10}),
        }

class ChordForm(forms.ModelForm):

    class Meta:

        model = Chord

        fields = [
            'song', 'root', 'quality', 'inversion', 'measure', 'beat', 'sub_beat', 'duration_in_beats', 'key_context', 'roman_numeral'
        ]

    def save(self, commit=True):
        """
        Override save to let the model's own logic handle chord_name
        and roman_numeral generation.
        """
        # We don't call super().save() immediately.
        # We prepare the instance first.
        instance = super().save(commit=False)
        
        # Set the context from the parent song
        instance.key_context = self.initial['song'].key
        
        # The model's own .save() method will automatically generate the chord_name
        # and run full_clean(). We don't need to do it here.
        
        if commit:
            instance.save()
        return instance