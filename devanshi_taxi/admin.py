from django.contrib import admin
from .models import Car, Booking

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_type', 'rate', 'capacity')
    list_filter = ('car_type',)
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('username', 'pickup', 'drop', 'pickup_date', 'pickup_time', 'return_date')
    list_filter = ('pickup_date', 'return_date')
    search_fields = ('username', 'pickup', 'drop')
