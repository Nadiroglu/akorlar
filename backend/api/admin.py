from django.contrib import admin
from .models import Genre, Artist, Song, Chord, ChordDiagram, SongRequest, SearchQuery

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    ordering = ['name']

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'birth_date', 'created_at', 'updated_at']
    list_filter = ['country', 'birth_date', 'created_at', 'updated_at']
    search_fields = ['name', 'bio', 'country']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'difficulty', 'key', 'is_popular', 'chords_available', 'tabs_available', 'created_at']
    list_filter = ['genre', 'difficulty', 'key', 'is_popular', 'chords_available', 'tabs_available', 'year', 'created_at']
    search_fields = ['title', 'artist__name', 'lyrics']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'play_count']
    list_editable = ['is_popular', 'chords_available', 'tabs_available']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'artist', 'genre', 'lyrics')
        }),
        ('Musical Details', {
            'fields': ('difficulty', 'key', 'tempo', 'year', 'duration')
        }),
        ('Features', {
            'fields': ('chords_available', 'tabs_available', 'is_popular')
        }),
        ('Statistics', {
            'fields': ('play_count', 'rating'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Chord)
class ChordAdmin(admin.ModelAdmin):
    list_display = ['song', 'chord_name', 'position', 'bar', 'beat', 'duration', 'created_at']
    list_filter = ['chord_name', 'bar', 'created_at']
    search_fields = ['song__title', 'chord_name']
    ordering = ['song', 'position', 'bar', 'beat']
    readonly_fields = ['created_at']

@admin.register(ChordDiagram)
class ChordDiagramAdmin(admin.ModelAdmin):
    list_display = ['chord_name', 'tuning', 'difficulty', 'created_at']
    list_filter = ['difficulty', 'tuning', 'created_at']
    search_fields = ['chord_name']
    ordering = ['chord_name', 'tuning']
    readonly_fields = ['created_at']

@admin.register(SongRequest)
class SongRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist_name', 'genre_name', 'user_email', 'status', 'requested_at', 'days_since_request']
    list_filter = ['status', 'genre_name', 'requested_at']
    search_fields = ['title', 'artist_name', 'user_email', 'user_name']
    ordering = ['-requested_at']
    readonly_fields = ['requested_at', 'updated_at', 'days_since_request']
    list_editable = ['status']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('title', 'artist_name', 'genre_name', 'additional_notes')
        }),
        ('User Information', {
            'fields': ('user_email', 'user_name')
        }),
        ('Status Management', {
            'fields': ('status', 'admin_notes', 'completed_song')
        }),
        ('Timestamps', {
            'fields': ('requested_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def days_since_request(self, obj):
        from datetime import datetime
        delta = datetime.now().replace(tzinfo=None) - obj.requested_at.replace(tzinfo=None)
        return f"{delta.days} days"
    days_since_request.short_description = 'Days Since Request'
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='approved')
        self.message_user(request, f'{updated} song requests have been approved.')
    approve_requests.short_description = "Approve selected requests"
    
    def reject_requests(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f'{updated} song requests have been rejected.')
    reject_requests.short_description = "Reject selected requests"

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'results_count', 'timestamp', 'ip_address']
    list_filter = ['timestamp', 'results_count']
    search_fields = ['query', 'ip_address']
    ordering = ['-timestamp']
    readonly_fields = ['timestamp']
    list_per_page = 100
