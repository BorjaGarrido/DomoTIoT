from django.contrib import admin

# Register your models here.

from .models import Modulo, UserProfile

admin.site.register(Modulo)
admin.site.register(UserProfile)
