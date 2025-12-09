from django.contrib import admin
from .models import Film, Favorite, WatchHistory, Review

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'rating', 'views')
    list_filter = ('release_date',)
    search_fields = ('title',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'added_at')

@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'watched_at', 'progress')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'rating', 'created_at')
