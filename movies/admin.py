# movies/admin.py
from django.contrib import admin
from .models import Movie, Rating, Watchlist

admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Watchlist)
