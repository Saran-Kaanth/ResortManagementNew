from django.contrib import admin
from .models import *
# admin.site.register(Rooms)

@admin.register(Rooms)
class RoomAdmin(admin.ModelAdmin):
    list_display=Rooms.DisplayFields

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display=Reservation.DisplayFields

# Register your models here.
