from django.contrib import admin
from .models import *

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "image"]

class HotelImageInline(admin.TabularInline):
    model   = HotelImage
    extra   = 4       
    max_num = 4
    fields  = ('image',)
    verbose_name        = 'Доп. фото'
    verbose_name_plural = 'Доп. фотографии (макс. 4)'

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display  = ('name', 'city', 'stars', 'price', 'rating')
    list_filter   = ('stars', 'city')
    search_fields = ('name',)
    inlines       = [HotelImageInline]





@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'departure_date', 'price', 'airline', 'transfers')
    list_filter = ('origin', 'destination', 'transfers', 'departure_date')
    search_fields = ('airline',)

