from django.shortcuts import render, redirect
from .forms import LoginForm, CardForm
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Card
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

User = get_user_model()

@login_required
def profile_view(request):
    cards = request.user.cards.all()

    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect('profile')  
    else:
        form = CardForm()

    return render(request, 'login.html', {
        'cards': cards,
        'form': form,
    })

@require_POST
@login_required
def delete_card(request, card_id):
    card = get_object_or_404(Card, id=card_id, user=request.user)
    card.delete()
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            if number == '907377720':
                user, created = User.objects.get_or_create(username=number)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth_login(request, user)

                request.session['show_modal'] = True
                return redirect('profile')  # ✅ было 'login', стало 'profile'
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def clear_modal_flag(request):
    request.session.pop('show_modal', None)
    return HttpResponse("OK")