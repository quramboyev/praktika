from .models import Card


def cards(request):
    if request.user.is_authenticated:
        return {"cards": request.user.cards.all()}
    return {"cards": []}