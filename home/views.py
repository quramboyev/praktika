from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from home.models import MovieModel, SessionModel, CinemaModel
from django.utils.translation import gettext_lazy as _


@login_required(login_url="login")
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
            type_name = _("Child")
            price = str(session.child).replace(',', '.')
        case "student":
            type_name = _("Student")
            price = str(session.student).replace(',', '.')
        case _:
            type_name = _("Adult")
            price = str(session.adult).replace(',', '.')
    cinema = session.cinema
    rows = cinema.seats_row_count
    cols = cinema.seats_column_count
    occupied = session.tickets.values_list('seat_row', 'seat_column').order_by('seat_row', 'seat_column')
    return render(request, 'seats.html', context={'cinema': cinema, 'rows': rows, 'cols': cols, 'occupied': [list(i) for i in occupied], "session": session, "price": price, "type_name": type_name })
