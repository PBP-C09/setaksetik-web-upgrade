from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from booking.forms import BookingForm, FilterForm
from booking.models import Booking
from explore.models import Menu
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.models import User

# Create your views here.
def main_booking_page(request):
    return render(request, 'booking/main_booking_page.html')

def create_booking(request):
    form_filter = FilterForm(request.GET or None)
    menus = Menu.objects.all()

    # Filter berdasarkan checkbox
    if form_filter.is_valid():
        if form_filter.cleaned_data['takeaway']:
            menus = menus.filter(takeaway=True)
        if form_filter.cleaned_data['delivery']:
            menus = menus.filter(delivery=True)
        if form_filter.cleaned_data['outdoor']:
            menus = menus.filter(outdoor=True)
        if form_filter.cleaned_data['wifi']:
            menus = menus.filter(wifi=True)
        
        # Filter berdasarkan kota
        city = form_filter.cleaned_data.get('city')
        if city:
            menus = menus.filter(city__iexact=city)

    context = {
        'form_filter': form_filter,
        'menus': menus,
    }
    return render(request, 'booking/create_booking.html', context)

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

@csrf_exempt
@require_POST
def add_booking_ajax(request):
    menu_id = request.POST.get("menu_id")
    booking_date = strip_tags(request.POST.get("booking_date"))
    number_of_people = request.POST.get("number_of_people")

    if not menu_id or not booking_date or not number_of_people:
        return JsonResponse({"error": "Incomplete data"}, status=400)

    try:
        menu = Menu.objects.get(id=menu_id)
    except Menu.DoesNotExist:
        return JsonResponse({"error": "Menu not found"}, status=404)

    # Create booking instance
    booking = Booking(
        user=request.user,
        menu_items=menu,
        booking_date=booking_date,
        number_of_people=number_of_people,
    )
    booking.save()

    # Return success response
    return JsonResponse({
        "message": "Booking created successfully",
        "menu_name": menu.menu,
        "restaurant_name": menu.restaurant_name,
    }, status=201)

def show_booking_xml(request):
    data = Booking.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_booking_json(request):
    data = Booking.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_booking_xml_by_id(request, booking_id):
    data = Booking.objects.filter(pk=booking_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_booking_json_by_id(request, booking_id):
    data = Booking.objects.filter(pk=booking_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")