from django.urls import path
from .views import login_view, clear_modal_flag, profile_view, delete_card

urlpatterns = [
    path('login/', login_view, name='login'),
    path('clear-modal-flag/', clear_modal_flag, name='clear-modal-flag'),
    path('profile/', profile_view, name='profile'),
    path('delete-card/<int:card_id>/', delete_card, name='delete_card'),
]