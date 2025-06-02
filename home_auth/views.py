from django.shortcuts import render, redirect
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            return redirect('home')  
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})