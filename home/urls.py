from django.urls import path
from .views import home, movie_about, movie_sessions, cinema_seats

urlpatterns = [
    path('', home, name='home'),
    path('movie_about/', movie_about, name='movie_about'),
    path('movie_sessions', movie_sessions, name='movie_sessions'),
    path('seets/', cinema_seats, name='seets'),
]