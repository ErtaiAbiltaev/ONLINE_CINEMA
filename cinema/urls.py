from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('search/', views.search_films, name='search'),
    path('film/<int:tmdb_id>/', views.film_detail, name='film_detail'),
    path('favorites/', views.favorites, name='favorites'),
    path('history/', views.watch_history, name='watch_history'),
    path('toggle-favorite/<int:film_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('review/<int:film_id>/', views.add_review, name='add_review'),
    path('category/<str:category>/', views.category_view, name='category'),
    path('novelties/', views.novelties, name='novelties'),
]
