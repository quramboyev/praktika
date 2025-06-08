from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import *


admin.site.register(GenreModel, TranslatableAdmin)
admin.site.register(DirectorModel, TranslatableAdmin)
admin.site.register(ActorModel, TranslatableAdmin)
admin.site.register(MovieModel, TranslatableAdmin)
admin.site.register(RatingModel, admin.ModelAdmin)
admin.site.register(CinemaModel, TranslatableAdmin)
admin.site.register(SessionModel, admin.ModelAdmin)
admin.site.register(TicketModel, admin.ModelAdmin)
