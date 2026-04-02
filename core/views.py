from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db.models import Avg
from django.contrib import messages
from .forms import RegisterForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Hotel, City

def index(request):
    hotels = Hotel.objects.select_related('city').all()
    cities = City.objects.all()
    hotel_count = hotels.count()
    country_count = City.objects.values('country').distinct().count()
    avg_rating = round(hotels.aggregate(avg=Avg('rating'))['avg'] or 0, 1)

    for hotel in hotels:
        hotel.amenities_list = [a.strip() for a in hotel.amenities.split(',') if a.strip()]

    context = {
        'hotels': hotels,
        'cities': cities,
        'hotel_count': hotel_count,
        'country_count': country_count,
        'avg_rating': avg_rating,
    }

    return render(request, "index.html", context)

def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна!")
            return redirect("index")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Неверный логин или пароль.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def city_hotels(request, city_id):
    city = get_object_or_404(City, id=city_id)
    hotels = Hotel.objects.filter(city=city)
    for hotel in hotels:
        hotel.amenities_list = [a.strip() for a in hotel.amenities.split(',') if a.strip()]
    return render(request, 'hotel_list.html', {'city': city, 'hotels': hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    hotel.amenities_list = [a.strip() for a in hotel.amenities.split(',') if a.strip()]
    images = hotel.images.all()
    return render(request, 'hotel_detail.html', {'hotel': hotel, 'images': images})

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

def terms(request):
    return render(request, 'terms.html')

def privacy(request):
    return render(request, 'privacy.html')

def faq(request):
    return render(request, 'faq.html')

def report_bug(request):
    return render(request, 'report_bug.html')

def search(request):
    query = request.GET.get('q', '').strip()
    guests = int(request.GET.get('guests', 1))
    hotels = Hotel.objects.select_related('city').all()

    if query:
        for word in query.split():
            hotels = hotels.filter(
                Q(name__icontains=word) |
                Q(city__name__icontains=word)
            )

    if guests > 1:
        hotels = hotels.filter(max_guests__gte=guests)

    return render(request, 'search.html', {
        'hotels': hotels,
        'query': query,
        'guests': guests,
    })

def all_hotels(request):
    cities = City.objects.all()
    hotels = Hotel.objects.select_related('city').all()
    for hotel in hotels:
        hotel.amenities_list = [a.strip() for a in hotel.amenities.split(',') if a.strip()]
    return render(request, 'all_hotels.html', {'hotels': hotels, 'cities': cities})


from datetime import timedelta
from django.utils import timezone
from .models import Flight


def flight_search(request):
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    date = request.GET.get('date_there')

    baggage = request.GET.get('baggage')
    transfers = request.GET.get('transfers')
    time_filter = request.GET.get('time')

    flights = Flight.objects.all()

    # 🔍 Фильтр по маршруту и дате
    if origin and destination and date:
        flights = flights.filter(
            origin__name=origin,
            destination__name=destination,
            departure_date=date
        )

    # 🎯 Фильтры
    if baggage:
        flights = flights.exclude(baggage__isnull=True)

    if transfers != "" and transfers is not None:
        flights = flights.filter(transfers=transfers)

    if time_filter:
        if time_filter == 'morning':
            flights = flights.filter(departure_time__lt="12:00")
        elif time_filter == 'day':
            flights = flights.filter(departure_time__gte="12:00", departure_time__lt="18:00")
        elif time_filter == 'evening':
            flights = flights.filter(departure_time__gte="18:00")

    # 📅 nearby dates
    nearby_dates = []

    if date and origin and destination:
        base_date = timezone.datetime.strptime(date, "%Y-%m-%d").date()

        for i in range(-7, 8):
            d = base_date + timedelta(days=i)

            flight = Flight.objects.filter(
                origin__name=origin,
                destination__name=destination,
                departure_date=d
            ).first()

            nearby_dates.append({
                "date": d,
                "price": flight.price if flight else None
            })

    return render(request, "flights.html", {
        "flights": flights,
        "nearby_dates": nearby_dates,
        "origin": origin,
        "destination": destination,
        "selected_date": date,
        'hide_footer_newsletter': True
    })

import uuid
from django.contrib.auth.decorators import login_required
from .models import Hotel, Booking

@login_required(login_url='login')  # редирект если не вошёл
def booking(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == 'POST':
        check_in    = request.POST.get('check_in')
        check_out   = request.POST.get('check_out')
        room_type   = request.POST.get('room_type', 'Стандарт')
        adults      = int(request.POST.get('adults', 2))
        children    = int(request.POST.get('children', 0))
        total_price = request.POST.get('total_price', 0)
        booking_num = 'LUX-' + uuid.uuid4().hex[:6].upper()

        Booking.objects.create(
            user=request.user,
            hotel=hotel,
            room_type=room_type,
            check_in=check_in,
            check_out=check_out,
            adults=adults,
            children=children,
            total_price=total_price,
            booking_num=booking_num,
        )
        return redirect('booking_success', booking_num=booking_num)

    return render(request, 'booking.html', {'hotel': hotel})


def booking_success(request, booking_num):
    booking = get_object_or_404(Booking, booking_num=booking_num)
    return render(request, 'booking_success.html', {'booking': booking})

from django.contrib.auth.decorators import login_required
from django.db.models import Sum

@login_required(login_url='login')
def my_bookings(request):
    from django.utils import timezone
    bookings = Booking.objects.filter(user=request.user).select_related('hotel','hotel__city').order_by('-created_at')
    today = timezone.now().date()
    active_count = bookings.filter(check_out__gte=today).count()
    total_spent = bookings.aggregate(s=Sum('total_price'))['s'] or 0
    return render(request, 'my_bookings.html', {
        'bookings': bookings,
        'active_count': active_count,
        'total_spent': round(total_spent, 2),
    })

@login_required(login_url='login')
def cancel_booking(request, booking_num):
    booking = get_object_or_404(Booking, booking_num=booking_num, user=request.user)
    if request.method == 'POST':
        booking.delete()
    return redirect('my_bookings')