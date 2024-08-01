# movies/views.py
from django.shortcuts import render, get_object_or_404, redirect
import requests
from config import IMDB_API_KEY, TMDB_API_KEY
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Movie, Rating, Watchlist
from django.http import HttpResponse
from django.contrib import messages

TMDB_API_KEY = "8ecba0ec3008a6842619a91099e9627f"


def search(request):
    # Get the query from the search box
    query = request.GET.get('q')
    print(query)

    # If the query is not empty
    if query:
        # Get the results from the API
        data = requests.get(
            f"https://api.themoviedb.org/3/search/{request.GET.get('type')}?api_key={TMDB_API_KEY}&language=en-US&page=1&include_adult=false&query={query}")
        print(data.json())
    else:
        return HttpResponse("Please enter a search query")

    # Render the template
    return render(request, 'movies/results.html', {
        "data": data.json(),
        "type": request.GET.get("type")
    })


def index(request):
    return render(request, 'movies/home.html')


def view_movie_detail(request, movie_id):
    data = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    recommendations = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US")
    cast = fetch_cast_details(movie_id)

    return render(request, "movies/movie_detail.html", {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "movie",
        "cast": cast,
    })


def view_tv_detail(request, tv_id):
    data = requests.get(
        f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US")
    recommendations = requests.get(
        f"https://api.themoviedb.org/3/tv/{tv_id}/recommendations?api_key={TMDB_API_KEY}&language=en-US")
    cast = fetch_cast_details(tv_id)

    return render(request, "movies/tv_detail.html", {
        "data": data.json(),
        "recommendations": recommendations.json(),
        "type": "tv",
        "cast": cast,
    })


def view_trendings_results(request):
    type = request.GET.get("media_type")
    time_window = request.GET.get("time_window")

    try:
        trendings = requests.get(
            f"https://api.themoviedb.org/3/trending/{type}/{time_window}?api_key={TMDB_API_KEY}&language=en-US")
        trendings.raise_for_status()  # Raise HTTPError for bad responses
        return JsonResponse(trendings.json())
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection errors, timeouts)
        print(f"Request error: {e}")
        return HttpResponse("Error fetching trending data", status=500)
    except Exception as e:
        # Handle other exceptions
        print(f"Unexpected error: {e}")
        return HttpResponse("Unexpected error", status=500)


@login_required
def add_to_watchlist(request, movie_id):
    tmdb_movie_details = fetch_tmdb_movie_details(movie_id)

    if tmdb_movie_details:
        user = request.user
        movie, created = Movie.objects.get_or_create(
            movie_id=movie_id,
            defaults={
                'title': tmdb_movie_details.get('title', ''),
                # Use get to provide a default value
                'poster_url': tmdb_movie_details.get('poster_path', ''),
                'release_date': tmdb_movie_details.get('release_date', ''),
                # Add other fields as needed
            }
        )

        if not Watchlist.objects.filter(user=user, movie=movie).exists():
            # Add movie to watchlist
            Watchlist.objects.create(user=user, movie=movie)
            return JsonResponse({'message': 'Movie added to watchlist successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Movie already in watchlist'}, status=200)
    else:
        return JsonResponse({'error': 'Failed to fetch movie details from TMDb'}, status=500)


@login_required
def rate_movie(request, movie_id):
    tmdb_movie_details = fetch_tmdb_movie_details(movie_id)

    if tmdb_movie_details:
        user = request.user
        movie, created = Movie.objects.get_or_create(
            movie_id=movie_id,
            defaults={
                'title': tmdb_movie_details.get('title', ''),
                # Use get to provide a default value
                'poster_url': tmdb_movie_details.get('poster_path', ''),
                'release_date': tmdb_movie_details.get('release_date', ''),
                # Add other fields as needed
            }
        )

        rating_value = int(request.POST.get('rating', 0))

        if 1 <= rating_value <= 10:
            # Add or update rating
            Rating.objects.update_or_create(
                user=user, movie=movie, defaults={'rating': rating_value})
            return JsonResponse({'message': 'Movie rated successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid rating value. Rating must be between 1 and 10.'}, status=400)
    else:
        return JsonResponse({'error': 'Failed to fetch movie details from TMDb'}, status=500)


def fetch_cast_details(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=en-US")

    if response.status_code == 200:
        return response.json().get('cast', [])
    else:
        return []


def fetch_tmdb_movie_details(movie_id):
    tmdb_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US'
    response = requests.get(tmdb_url)

    if response.status_code == 200:
        movie_details = response.json()

        # Extract relevant details
        title = movie_details.get('title', '')
        poster_url = movie_details.get('poster_path', '')
        release_date = movie_details.get('release_date', '')

        return {
            'title': title,
            'poster_url': poster_url,
            'release_date': release_date,
            'movie_id': movie_id,
        }
    else:
        return None


@login_required
def add_tv_to_watchlist(request, tv_id):
    tmdb_tv_details = fetch_tmdb_tv_details(tv_id)

    if tmdb_tv_details:
        user = request.user
        movie, created = Movie.objects.get_or_create(
            movie_id=tv_id,
            defaults={
                'title': tmdb_tv_details['name'],
                'poster_url': tmdb_tv_details['poster_path'],
                'release_date': tmdb_tv_details['first_air_date'],
                # Add other fields as needed
            }
        )

        if not Watchlist.objects.filter(user=user, movie=movie).exists():
            # Add TV show (considered as a movie in this context) to watchlist
            Watchlist.objects.create(user=user, movie=movie)
            return JsonResponse({'message': 'TV show added to watchlist successfully'}, status=200)
        else:
            return JsonResponse({'message': 'TV show already in watchlist'}, status=200)
    else:
        return JsonResponse({'error': 'Failed to fetch TV show details from TMDb'}, status=500)


@login_required
def rate_tv_show(request, tv_id):
    tmdb_tv_details = fetch_tmdb_tv_details(tv_id)

    if tmdb_tv_details:
        user = request.user
        tv, created = Movie.objects.get_or_create(
            movie_id=tv_id,
            defaults={
                'title': tmdb_tv_details['name'],
                'poster_url': tmdb_tv_details['poster_path'],
                'release_date': tmdb_tv_details.get('first_air_date', ''),
                # Add other fields as needed
            }
        )

        rating_value = int(request.POST.get('rating', 0))

        if 1 <= rating_value <= 10:
            # Add or update rating
            Rating.objects.update_or_create(
                user=user, movie=tv, defaults={'rating': rating_value})
            return JsonResponse({'message': 'TV show rated successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid rating value. Rating must be between 1 and 10.'}, status=400)
    else:
        return JsonResponse({'error': 'Failed to fetch TV show details from TMDb'}, status=500)


def fetch_tmdb_tv_details(tv_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/tv/{tv_id}?api_key={TMDB_API_KEY}&language=en-US")
    if response.status_code == 200:
        return response.json()
    else:
        return None
