from django.db import models
from django.conf import settings

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Город")
    country = models.CharField(max_length=100, verbose_name="Страна")
    image = models.ImageField(upload_to='cities/', blank=True, null=True, verbose_name="Фото города")

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return f"{self.name}, {self.country}"


class Hotel(models.Model):
    name        = models.CharField(max_length=200, verbose_name="Название")
    city        = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name="Город")
    description = models.TextField(verbose_name="Описание")
    price       = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за ночь")
    stars       = models.IntegerField(default=5, verbose_name="Звёзды")
    rating      = models.DecimalField(max_digits=3, decimal_places=1, default=0, verbose_name="Рейтинг")
    image       = models.ImageField(upload_to='hotels/', blank=True, null=True, verbose_name="Фото")
    amenities   = models.CharField(max_length=500, blank=True, verbose_name="Удобства (через запятую)")
    max_guests  = models.IntegerField(default=2, verbose_name="Макс. гостей")
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "Отель"
        verbose_name_plural = "Отели"
        ordering            = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.city}"

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='hotels/gallery/', verbose_name="Фото")

    class Meta:
        verbose_name = "Фото отеля"
        verbose_name_plural = "Фото отелей"


class Flight(models.Model):
    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='arrivals')

    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    departure_time = models.TimeField(null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    airline = models.CharField(max_length=100)

    baggage = models.CharField(max_length=100, default="Багаж 23 кг — 1 шт")
    hand_luggage = models.CharField(max_length=100, default="Ручная кладь 10 кг — 1 шт")

    transfers = models.IntegerField(default=0)  # 0 = прямой
    duration = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.origin} → {self.destination}"

class Booking(models.Model):
    user    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    hotel   = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    room_type    = models.CharField(max_length=50, default='Стандарт')
    check_in     = models.DateField()
    check_out    = models.DateField()
    adults       = models.IntegerField(default=2)
    children     = models.IntegerField(default=0)
    total_price  = models.DecimalField(max_digits=10, decimal_places=2)
    booking_num  = models.CharField(max_length=20, unique=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return f"{self.booking_num} — {self.hotel.name}"
    
