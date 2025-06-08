from django.urls import path
from .views import home, movie_about, movie_sessions, cinema_seats

urlpatterns = [
    path('', home, name='home'),
    path('movie_about/<int:pk>/', movie_about, name='movie_about'),
    path('movie_sessions/<int:pk>/', movie_sessions, name='movie_sessions'),
    path('seets/<int:pk>/', cinema_seats, name='seats'),
]