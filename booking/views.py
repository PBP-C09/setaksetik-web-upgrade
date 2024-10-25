from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from booking.forms import BookingForm, FilterForm
from booking.models import Booking
from explore.models import Menu
from django.contrib.auth.models import User

# Create your views here.
def main_booking_page(request):
    return render(request, 'booking/main_booking_page.html')

def create_booking(request):
    form_filter = FilterForm(request.GET or None)
    menus = Menu.objects.all()

    if form_filter.is_valid():
        if form_filter.cleaned_data['takeaway']:
            menus = menus.filter(takeaway=True)
        if form_filter.cleaned_data['delivery']:
            menus = menus.filter(delivery=True)
        if form_filter.cleaned_data['outdoor']:
            menus = menus.filter(outdoor=True)
        if form_filter.cleaned_data['wifi']:
            menus = menus.filter(wifi=True)

    context = {
    'form_filter': form_filter,
    'menus': menus,
    }
    return render (request, 'booking/create_booking.html', context)

def lihat_booking(request):
    bookings = Booking.objects.filter(user=request.user)
    print(bookings)
    context = {
        'bookings': bookings
    }
    return render(request, 'booking/lihat_booking.html', context)

@login_required
def booking_form(request, menu_id):
    menu = Menu.objects.get(id=menu_id)

    if not menu:
        return HttpResponseNotFound("Menu not found")
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.menu_items = menu
            booking.user = request.user
            booking.save()
            return redirect('booking:main_booking_page')
    else:
        form = BookingForm()

    context = {
        'menu': menu,
        'form': form,
    }

    return render(request, 'booking/booking_form.html', context)

@login_required
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponseNotFound("Booking tidak ditemukan.")

    booking.delete()

    return redirect('booking:lihat_booking')

@login_required
def edit_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return HttpResponseNotFound("Booking tidak ditemukan.")
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking:lihat_booking')
    else:
        form = BookingForm(instance=booking)

    context = {
        'form': form,
        'booking': booking,
    }

    return render(request, 'booking/edit_booking.html', context)