from django.urls import path
from .views import *
urlpatterns = [
    path("", index, name="index"),
    path("register/", register, name="register"),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('city/<int:city_id>/', city_hotels, name='city_hotels'),
    path('hotel/<int:hotel_id>/', hotel_detail, name='hotel_detail'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    path('search/', search, name='search'),
    path('hotels/', all_hotels, name='all_hotels'),
    path('faq/', faq, name='faq'),
    path('report/', report_bug, name='report_bug'),
    path('flights/', flight_search, name='flight_search'),
    path('hotel/<int:hotel_id>/booking/', booking, name='booking'),
    path('booking/<str:booking_num>/success/', booking_success, name='booking_success'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('booking/<str:booking_num>/cancel/', cancel_booking, name='cancel_booking'),
]

