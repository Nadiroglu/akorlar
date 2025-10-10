#admin_views.py
from django.views import View
from django.shortcuts import render, get_object_or_404
from ..admin.forms import SongForm, ChordForm
from django.http import JsonResponse
from api.models import Song, Chord, Genre, Artist
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages


class SongManagementView(View):

    template_name = 'admin/song_management.html'


    def get(self, request,song_id=None):

        if song_id:
            song = get_object_or_404(Song, id=song_id)
            form = SongForm(instance=song)
            chords = song.chords.all()
            mode = 'edit'
        else:
            song = None
            form = SongForm()
            chords = []
            mode = 'create'
        
        context = {
            'song': song,
            'form': form,
            'chords': chords,
            'mode': mode,
            'artists': Artist.objects.all(),
            'genres': Genre.objects.all(),
            'available_keys': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m', 'Gm', 'G#m', 'Am', 'A#m', 'Bm'],
            'chord_qualities': [q[0] for q in Chord.QUALITY_CHOICES],
        }
        return render(request, self.template_name, context)
    

    def post(self, request, song_id=None):

        action_map = {
            'save_song': self.save_song,
            'add_chord': self.add_or_update_chord,
            'update_chord': self.add_or_update_chord,
            'delete_chord': self.delete_chord,
            'transpose_chords': self.transpose_chords,
            'add_artist': self.add_artist,
            'add_genre': self.add_genre,
        }

        action_func = action_map.get(request.POST.get('action'))

        if action_func:
            return action_func(request, song_id)
        
        return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)

    
    def save_song(self, request, song_id=None):
        song_instance = get_object_or_404(Song, id=song_id) if song_id else None
        form = SongForm(request.POST, instance=song_instance)


        # eger form validdirse o zaman song_instance save edilir

        if form.is_valid():
            song = form.save()
            song.chords_available = song.chords.exists()
            song.save(update_fields=['chords_available'])

            messages.success(request, f'Song "{song.title}" saved successfully!')
            return JsonResponse({'success': True, 'song_id': song.id})
        
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    
    def add_or_update_chord(self, request, song_id=None):
        song = get_object_or_404(Song, id=song_id)
        chord_id = request.POST.get('chord_id')
        chord_instance = get_object_or_404(Chord, id=chord_id) if chord_id else None

        form = ChordForm(request.POST, instance=chord_instance, initial={'song_key': song.key})

        if form.is_valid():
            chord = form.save(commit=False)
            chord.song = song # Explicitly set the song relationship
            chord.save()
            return JsonResponse({'success': True, 'chord_id': chord.id, 'chord_name': chord.chord_name})
            
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        
    def delete_chord(self, request, song_id):
        """Delete a chord."""
        try:
            chord_id = request.POST.get('chord_id')
            chord = get_object_or_404(Chord, id=chord_id, song_id=song_id)
            chord.delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    def transpose_chords(self, request, song_id):
        """Transpose all chords for the song."""
        song = get_object_or_404(Song, id=song_id)
        new_key = request.POST.get('new_key')
        
        if not new_key:
            return JsonResponse({'success': False, 'error': 'New key is required.'}, status=400)

        success, message = song.transpose_to_key(new_key)
        
        if success:
            return JsonResponse({'success': True, 'message': message})
        return JsonResponse({'success': False, 'error': message}, status=400)
    
    def add_artist(self, request):
        """Quick-add a new artist."""
        name = request.POST.get('name', '').strip()
        if not name:
            return JsonResponse({'success': False, 'error': 'Name is required'}, status=400)
        
        artist, created = Artist.objects.get_or_create(name__iexact=name, defaults={'name': name})
        return JsonResponse({'success': True, 'artist_id': artist.id, 'artist_name': artist.name})
        
    def add_genre(self, request):
        """Quick-add a new genre."""
        name = request.POST.get('name', '').strip()
        if not name:
            return JsonResponse({'success': False, 'error': 'Name is required'}, status=400)
            
        genre, created = Genre.objects.get_or_create(name__iexact=name, defaults={'name': name})
        return JsonResponse({'success': True, 'genre_id': genre.id, 'genre_name': genre.name})
