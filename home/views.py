from django.shortcuts import render, redirect
from home.models import MovieModel, SessionModel


def home(request):
    movies = MovieModel.objects.all().translated()
    return render(request, 'home.html', context={'movies': movies})

def movie_about(request, pk: int):
    movie = MovieModel.objects.get(pk=pk).translated()
    return render(request, 'movie_about.html', context={'movie': movie})

def movie_sessions(request, pk: int):
    try:
        movie = MovieModel.objects.get(pk=pk).translated()
    except MovieModel.DoesNotExist:
        return redirect('home')
    sessions = movie.sessions.all()
    return render(request, 'movie_sessions.html', context={'sessions': sessions, 'movie': movie})

def cinema_seats(request, pk: int):
    try:
        session = SessionModel.objects.prefetch_related('tickets').select_related('cinema', 'movie').get(pk=pk).translated()
    except MovieModel.DoesNotExist:
        return redirect('home')
    cinema = session.cinema
    rows = cinema.seats_row_count
    cols = cinema.seats_column_count
    occupied = session.tickets.values_list('seat_row', 'seat_column').order_by('seat_row', 'seat_column')
    return render(request, 'seats.html', context={'cinema': cinema, 'rows': rows, 'cols': cols, 'occupied': occupied})
