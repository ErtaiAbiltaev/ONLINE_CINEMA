from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.cache import cache
import requests
from django.conf import settings
from .models import Film, WatchHistory, Favorite, Review, UserProfile

TMDB_API_KEY = settings.TMDB_API_KEY
TMDB_BASE_URL = settings.TMDB_BASE_URL

def get_tmdb_data(endpoint, params=None, cache_time=3600):
    """Получить данные из TheMovieDB API с кешированием"""
    if params is None:
        params = {}
    
    cache_key = f"tmdb_{endpoint}_{str(params)}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data
    
    try:
        params['api_key'] = TMDB_API_KEY
        params['language'] = 'ru-RU'
        response = requests.get(f"{TMDB_BASE_URL}{endpoint}", params=params, timeout=10)
        data = response.json() if response.status_code == 200 else {'results': []}
        cache.set(cache_key, data, cache_time)
        return data
    except Exception as e:
        print(f"⚠️ Ошибка API: {e}")
        return {'results': []}

def home(request):
    trending = get_tmdb_data('/trending/movie/week', cache_time=7200)
    popular = get_tmdb_data('/movie/popular', cache_time=7200)
    top_rated = get_tmdb_data('/movie/top_rated', cache_time=7200)
    upcoming = get_tmdb_data('/movie/upcoming', cache_time=7200)
    
    context = {
        'trending': trending.get('results', [])[:12],
        'popular': popular.get('results', [])[:12],
        'top_rated': top_rated.get('results', [])[:12],
        'upcoming': upcoming.get('results', [])[:12],
    }
    return render(request, 'cinema/home.html', context)

def category_view(request, category):
    genre_ids = {
        'horror': 27,
        'action': 28,
        'adventure': 12,
        'comedy': 35,
        'crime': 80,
        'documentary': 99,
        'drama': 18,
        'family': 10751,
        'fantasy': 14,
        'history': 36,
        'mystery': 9648,
        'romance': 10749,
        'scifi': 878,
        'thriller': 53,
        'war': 10752,
        'western': 37,
    }
    
    genre_names = {
        'horror': '🎭 Ужасы',
        'action': '🔥 Боевики',
        'adventure': '🗺️ Приключения',
        'comedy': '😂 Комедии',
        'crime': '🔪 Криминал',
        'documentary': '📽️ Документалистика',
        'drama': '💔 Драма',
        'family': '👨‍👩‍👧‍👦 Семейные',
        'fantasy': '✨ Фэнтези',
        'history': '⏰ Исторические',
        'mystery': '🔍 Мистика',
        'romance': '💕 Романтика',
        'scifi': '🚀 Научная фантастика',
        'thriller': '😨 Триллеры',
        'war': '⚔️ Военные',
        'western': '🤠 Вестерны',
    }
    
    page = request.GET.get('page', 1)
    sort = request.GET.get('sort', 'rating')  # По умолчанию сортируем по рейтингу
    results = {}
    films = []
    genre_name = category
    
    if category in genre_ids:
        results = get_tmdb_data('/discover/movie', {
            'with_genres': genre_ids[category],
            'page': page,
            'sort_by': 'vote_average.desc' if sort == 'rating' else 'popularity.desc'
        })
        films = results.get('results', [])
        # Фильтруем только фильмы с рейтингом выше 6.0
        films = [f for f in films if f.get('vote_average', 0) >= 6.0]
        genre_name = genre_names.get(category, category)
    
    return render(request, 'cinema/category.html', {
        'films': films,
        'category': category,
        'genre_name': genre_name,
        'total_pages': results.get('total_pages', 0),
        'sort': sort
    })

def novelties(request):
    page = request.GET.get('page', 1)
    results = get_tmdb_data('/movie/upcoming', {'page': page})
    films = results.get('results', [])
    return render(request, 'cinema/category.html', {
        'films': films,
        'category': 'novelties',
        'genre_name': '🎬 Новинки',
        'total_pages': results.get('total_pages', 0)
    })

def register(request):
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
    logout(request)
    return redirect('home')

@login_required
def profile(request):
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
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)
    results = {}
    films = []
    
    if query:
        results = get_tmdb_data('/search/movie', {'query': query, 'page': page})
        films = results.get('results', [])
    
    return render(request, 'cinema/search.html', {
        'films': films,
        'query': query,
        'total_pages': results.get('total_pages', 0) if query else 0
    })

def film_detail(request, tmdb_id):
    film_data = get_tmdb_data(f'/movie/{tmdb_id}')
    
    if not film_data.get('id'):
        return render(request, 'cinema/404.html', status=404)
    
    credits = get_tmdb_data(f'/movie/{tmdb_id}/credits')
    recommendations = get_tmdb_data(f'/movie/{tmdb_id}/recommendations')
    videos = get_tmdb_data(f'/movie/{tmdb_id}/videos')
    
    trailer_url = None
    for video in videos.get('results', []):
        if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
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
    film = get_object_or_404(Film, id=film_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, film=film)
    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})

@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('film')
    return render(request, 'cinema/favorites.html', {'favorites': favorites})

@login_required
def watch_history(request):
    history = WatchHistory.objects.filter(user=request.user).select_related('film')
    return render(request, 'cinema/watch_history.html', {'history': history})

@login_required
@require_POST
def add_review(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    rating = int(request.POST.get('rating', 5))
    comment = request.POST.get('comment', '')
    
    review, created = Review.objects.update_or_create(
        user=request.user,
        film=film,
        defaults={'rating': rating, 'comment': comment}
    )
    
    return redirect('film_detail', tmdb_id=film.tmdb_id)

@login_required
def clear_history(request):
    """Очистить историю просмотров"""
    WatchHistory.objects.filter(user=request.user).delete()
    return redirect('watch_history')

def about(request):
    """Страница о сервисе"""
    context = {
        'title': 'О WESTLINE',
        'description': 'Платформа для потокового просмотра фильмов',
        'features': [
            'Потоковый просмотр фильмов',
            'Расширенный каталог фильмов',
            'История просмотров',
            'Система рецензий',
            'Избранные фильмы',
            'Рекомендации на основе рейтинга',
        ]
    }
    return render(request, 'cinema/about.html', context)

@login_required
def add_recommendation(request, film_id):
    """Добавить рекомендацию фильма"""
    film = get_object_or_404(Film, id=film_id)
    
    if request.method == 'POST':
        title = request.POST.get('title', 'Советую посмотреть!')
        message = request.POST.get('message', '')
        
        if message.strip():
            from .models import Recommendation
            Recommendation.objects.create(
                user=request.user,
                film=film,
                title=title,
                message=message
            )
        
        return redirect('film_detail', tmdb_id=film.tmdb_id)
    
    return redirect('film_detail', tmdb_id=film.tmdb_id)

@login_required
def like_recommendation(request, recommendation_id):
    """Лайк рекомендации"""
    from .models import Recommendation
    recommendation = get_object_or_404(Recommendation, id=recommendation_id)
    recommendation.likes += 1
    recommendation.save()
    return redirect('film_detail', tmdb_id=recommendation.film.tmdb_id)
