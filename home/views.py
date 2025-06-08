from django.shortcuts import render, redirect
from home.models import MovieModel, SessionModel, CinemaModel


def home(request):
    movies = MovieModel.objects.all().translated()
    return render(request, 'home.html', context={'movies': movies})

def movie_about(request, pk: int):
    movie = MovieModel.objects.translated().get(pk=pk)
    return render(request, 'movie_about.html', context={'movie': movie})

def movie_sessions(request, pk: int):
    try:
        movie = MovieModel.objects.translated().get(pk=pk)
    except MovieModel.DoesNotExist:
        return redirect('home')
    cinemas = CinemaModel.objects.prefetch_related('sessions').filter(sessions__movie_id=pk).distinct()
    return render(request, 'movie_sessions.html', context={'cinemas': cinemas, 'movie': movie})

def cinema_seats(request, pk: int):
    try:
        session = SessionModel.objects.prefetch_related('tickets').select_related('cinema', 'movie').get(pk=pk)
    except MovieModel.DoesNotExist:
        return redirect('home')
    price_type = request.GET.get('type')
    match price_type:
        case "child":
            price = session.child
        case "student":
            price = session.student
        case _:
            price = session.adult
    cinema = session.cinema
    rows = cinema.seats_row_count
    cols = cinema.seats_column_count
    occupied = session.tickets.values_list('seat_row', 'seat_column').order_by('seat_row', 'seat_column')
    print(occupied)
    return render(request, 'seats.html', context={'cinema': cinema, 'rows': rows, 'cols': cols, 'occupied': [list(i) for i in occupied], "session": session, "price": price})
