from django.db import models
from django.contrib.auth.models import User

class Film(models.Model):
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField(null=True, blank=True)
    rating = models.FloatField(default=0)
    poster_url = models.URLField()
    backdrop_url = models.URLField(blank=True)
    duration = models.IntegerField(null=True, blank=True)
    genres = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    user_rating = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(default='https://via.placeholder.com/150')
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now=True)
    progress = models.IntegerField(default=0, help_text="Прогресс в секундах")

    class Meta:
        ordering = ['-watched_at']

    def __str__(self):
        return f"{self.user} -> {self.film}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user} -> {self.film}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.film} ({self.rating}/10)"

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='recommended_by')
    title = models.CharField(max_length=255, default="Советую посмотреть!")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} рекомендует {self.film}"
