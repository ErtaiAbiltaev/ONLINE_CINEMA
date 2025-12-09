from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
import requests
from django.conf import settings
from .models import Film, WatchHistory, Favorite, Review, UserProfile
import json

TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_BASE_URL = settings.TMDB_BASE_URL

def get_tmdb_data(endpoint, params=None):
    """Получить данные из TheMovieDB API"""
    if params is None:
        params = {}
    params['api_key'] = TMDB_API_KEY
    params['language'] = 'ru-RU'
    response = requests.get(f"{TMDB_BASE_URL}{endpoint}", params=params)
    return response.json() if response.status_code == 200 else {}

def home(request):
    """Главная страница"""
    trending = get_tmdb_data('/trending/movie/week')
    popular = get_tmdb_data('/movie/popular')
    top_rated = get_tmdb_data('/movie/top_rated')
    
    context = {
        'trending': trending.get('results', [])[:10],
        'popular': popular.get('results', [])[:8],
        'top_rated': top_rated.get('results', [])[:8],
    }
    return render(request, 'cinema/home.html', context)

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            return render(request, 'cinema/register.html', {'error': 'Пароли не совпадают'})

        if User.objects.filter(username=username).exists():
            return render(request, 'cinema/register.html', {'error': 'Пользователь уже существует'})

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        login(request, user)
        return redirect('home')

    return render(request, 'cinema/register.html')

def login_view(request):
    """Вход пользователя"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'cinema/login.html', {'error': 'Неверные учетные данные'})

    return render(request, 'cinema/login.html')

def logout_view(request):
    """Выход пользователя"""
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    """Профиль пользователя"""
    user_profile = request.user.profile
    favorites = Favorite.objects.filter(user=request.user).select_related('film')
    watch_history = WatchHistory.objects.filter(user=request.user).select_related('film')[:10]
    
    context = {
        'user_profile': user_profile,
        'favorites_count': favorites.count(),
        'history_count': watch_history.count(),
        'favorites': favorites[:6],
        'watch_history': watch_history,
    }
    return render(request, 'cinema/profile.html', context)

def search_films(request):
    """Поиск фильмов"""
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    
    if query:
        results = get_tmdb_data('/search/movie', {'query': query, 'page': page})
        films = results.get('results', [])
    else:
        films = []
    
    return render(request, 'cinema/search.html', {
        'films': films,
        'query': query,
        'total_pages': results.get('total_pages', 0) if query else 0
    })

def film_detail(request, tmdb_id):
    """Детальная страница фильма"""
    film_data = get_tmdb_data(f'/movie/{tmdb_id}')
    
    if not film_data.get('id'):
        return render(request, 'cinema/404.html', status=404)
    
    credits = get_tmdb_data(f'/movie/{tmdb_id}/credits')
    recommendations = get_tmdb_data(f'/movie/{tmdb_id}/recommendations')
    videos = get_tmdb_data(f'/movie/{tmdb_id}/videos')
    
    trailer_url = None
    for video in videos.get('results', []):
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            trailer_url = f"https://www.youtube.com/embed/{video['key']}"
            break
    
    film, created = Film.objects.get_or_create(
        tmdb_id=int(tmdb_id),
        defaults={
            'title': film_data.get('title', 'Неизвестно'),
            'description': film_data.get('overview', ''),
            'release_date': film_data.get('release_date'),
            'rating': float(film_data.get('vote_average', 0)),
            'poster_url': f"https://image.tmdb.org/t/p/w500{film_data.get('poster_path', '')}" if film_data.get('poster_path') else '',
            'backdrop_url': f"https://image.tmdb.org/t/p/w1280{film_data.get('backdrop_path', '')}" if film_data.get('backdrop_path') else '',
            'duration': film_data.get('runtime'),
            'genres': ', '.join([g['name'] for g in film_data.get('genres', [])]),
        }
    )
    
    film.views += 1
    film.save()
    
    is_favorite = False
    user_review = None
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, film=film).exists()
        user_review = Review.objects.filter(user=request.user, film=film).first()
        WatchHistory.objects.update_or_create(user=request.user, film=film)
    
    reviews = Review.objects.filter(film=film).select_related('user')[:5]
    
    context = {
        'film': film,
        'film_data': film_data,
        'credits': credits.get('cast', [])[:5],
        'recommendations': recommendations.get('results', [])[:6],
        'is_favorite': is_favorite,
        'user_review': user_review,
        'reviews': reviews,
        'trailer_url': trailer_url,
        'avg_rating': sum(r.rating for r in reviews) / len(reviews) if reviews else 0,
    }
    return render(request, 'cinema/film_detail.html', context)

@login_required
@require_POST
def toggle_favorite(request, film_id):
    """Добавить/удалить из избранного"""
    film = get_object_or_404(Film, id=film_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, film=film)
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})

@login_required
def favorites(request):
    """Избранные фильмы"""
    favorites = Favorite.objects.filter(user=request.user).select_related('film')
    return render(request, 'cinema/favorites.html', {'favorites': favorites})

@login_required
def watch_history(request):
    """История просмотров"""
    history = WatchHistory.objects.filter(user=request.user).select_related('film')
    return render(request, 'cinema/watch_history.html', {'history': history})

@login_required
@require_POST
def add_review(request, film_id):
    """Добавить рецензию"""
    film = get_object_or_404(Film, id=film_id)
    rating = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '')
    
    review, created = Review.objects.update_or_create(
        user=request.user,
        film=film,
        defaults={'rating': rating, 'comment': comment}
    )
    
    return redirect('film_detail', tmdb_id=film.tmdb_id)

def genre_films(request, genre_id):
    """Фильмы по жанру"""
    page = request.GET.get('page', 1)
    results = get_tmdb_data('/discover/movie', {'with_genres': genre_id, 'page': page})
    films = results.get('results', [])
    
    return render(request, 'cinema/genre_films.html', {
        'films': films,
        'genre_id': genre_id,
        'total_pages': results.get('total_pages', 0)
    })
