from django.contrib import admin

from .models import *

# admin.site.register(CustomUser)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display=CustomUser.DisplayFields
