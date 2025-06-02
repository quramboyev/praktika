from django.urls import path
from .views import home, movie_about, movie_sessions

urlpatterns = [
    path('home/', home, name='home'),
    path('movie_about/', movie_about, name='movie_about'),
    path('movie_sessions', movie_sessions, name='movie_sessions')
]