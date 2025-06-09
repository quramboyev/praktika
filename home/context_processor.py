from .models import TicketModel


def payments(request):
    if request.user.is_authenticated:
        return {"payments": request.user.tickets.select_related("session", "session__movie", "session__cinema").all()}
    return {"payments": []}
