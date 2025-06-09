from django.contrib import admin
from .models import *

admin.site.register(User, admin.ModelAdmin)
admin.site.register(Card, admin.ModelAdmin)
