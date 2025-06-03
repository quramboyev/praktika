from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def movie_about(request):
    return render(request, 'movie_about.html')

def movie_sessions(request):
    return render(request, 'movie_sessions.html')

def cinema_seets(request):
    return render(request, 'seets.html')
