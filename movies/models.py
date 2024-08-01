# movies/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Movie(models.Model):
    movie_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    poster_url = models.URLField(max_length=200)
    cast = models.TextField()
    plot = models.TextField()
    release_date = models.DateField()
    revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    rating_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()
    def __str__(self):
        return f'{self.movie.title} - {self.rating} by {self.user.username}'


class Watchlist(models.Model):
    watchlist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tmdb_movie_id = models.CharField(max_length=20, null=True, blank=True)  # Rename to tmdb_movie_id
    title = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.movie.title} - {self.user.username}'
