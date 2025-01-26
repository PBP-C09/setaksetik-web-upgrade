from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from booking.forms import BookingForm, FilterForm
from booking.models import Booking
from explore.models import Menu
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db.models import Q
import json

# Steak Lover (Customer)
@csrf_exempt
@login_required(login_url='/login')
def create_booking(request):
    form_filter = FilterForm(request.GET or None)
    menus = Menu.objects.all()

    restaurant_search = request.GET.get('restaurant', '')
    if restaurant_search:
        menus = menus.filter(restaurant_name__icontains=restaurant_search)

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

    unique_restaurants = [] # Filter berdasarkan resto
    for restaurant in menus.values('restaurant_name').distinct():
        first_menu = menus.filter(restaurant_name=restaurant['restaurant_name']).first()
        if first_menu:
            unique_restaurants.append(first_menu)

    context = {
        'form_filter': form_filter,
        'menus_unique': unique_restaurants,
    }
    return render(request, 'booking/create_booking.html', context)

@login_required(login_url='/login')
def lihat_booking(request):
    bookings = Booking.objects.filter(user=request.user)
    context = {
        'bookings': bookings
    }
    return render(request, 'booking/lihat_booking.html', context)

@csrf_exempt
@login_required(login_url='/login')
def booking_form(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    bookings = Booking.objects.filter(user=request.user)

    if not menu:
        return HttpResponseNotFound("Menu not found")
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.menu_items = menu
            booking.user = request.user
            booking.save()
            
            # Kembalikan data JSON untuk digunakan di AJAX
            booking_data = {
                'id': booking.id,
                'menu': booking.menu_items.menu,
                'booking_date': booking.booking_date.strftime("%B %d, %Y"),
                'number_of_people': booking.number_of_people,
                'restaurant_name': booking.menu_items.restaurant_name,
                'city': booking.menu_items.city,
                'rating': booking.menu_items.rating,
                'status': booking.get_status_display(),
                'image': booking.menu_items.image,
            }
            return JsonResponse({'message': 'Booking berhasil', 'booking': booking_data})
        else:
            return JsonResponse({'error': 'Form tidak valid'}, status=400)
    else:
        form = BookingForm()

    context = {
        'menu': menu,
        'form': form,
        'bookings': bookings
    }

    return render(request, 'booking/booking_form.html', context)

@csrf_exempt
@login_required(login_url='/login')
def delete_booking(request, booking_id):
    if request.method == 'DELETE':  # Hanya bisa method DELETE
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            booking.delete()
            return JsonResponse({'message': 'Booking deleted successfully'}, status=200)
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt    
@login_required(login_url='/login')
def edit_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return HttpResponseNotFound("Booking tidak ditemukan.")
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()  # Simpan perubahan ke database
            # Setelah berhasil menyimpan, form masih akan ditampilkan
            context = {
                'form': form,
                'booking': booking,
                'success': True,  # Tanda bahwa update berhasil
            }
            return render(request, 'booking/edit_booking.html', context)
        else:
            context = {
                'form': form,
                'booking': booking,
                'error': True  # Tanda bahwa ada kesalahan
            }
            return render(request, 'booking/edit_booking.html', context)
    else:
        form = BookingForm(instance=booking)
        context = {
            'form': form,
            'booking': booking,
        }
        return render(request, 'booking/edit_booking.html', context)


# Steak House Owner (Resto Owner)
@login_required(login_url='/login')
def pantau_booking_owner(request):
    user = request.user
    claimed_restaurant = Menu.objects.filter(claimed_by=user)
    
    if claimed_restaurant:
        bookings = []
        for menu in claimed_restaurant:
            bookings.extend(Booking.objects.filter(menu_items=menu))

        context = {
            'restaurant': claimed_restaurant[0], 
            'bookings': bookings,
            'resto_image': claimed_restaurant[0].image if claimed_restaurant else None
        }
    else:
        context = {
            'restaurant': None,
            'bookings': None
        }

    return render(request, 'booking/pantau_booking_owner.html', context)


@csrf_exempt
@login_required(login_url='/login')
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.user == booking.menu_items.claimed_by:  # Memastikan hanya owner yang bisa approve
        booking.status = 'approved'
        booking.save()

    return redirect('booking:pantau_booking_owner')  # Redirect kembali ke pantau booking owner


@login_required(login_url='/login')
def show_booking_xml(request):
    data = Booking.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


@login_required(login_url='/login')
def show_booking_json(request):
    data = Booking.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
def show_booking_xml_by_id(request, booking_id):
    data = Booking.objects.filter(pk=booking_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url='/login')
def show_booking_json_by_id(request, booking_id):
    data = Booking.objects.filter(pk=booking_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
def get_bookings_json(request):
    bookings = Booking.objects.all().filter(user=request.user)
    
    # Format data ke dalam struktur yang sesuai dengan model BookingEntry di Flutter
    booking_list = []
    for booking in bookings:
        booking_entry = {
            "model": "booking",  # Nama model Booking dalam format sederhana
            "pk": booking.id,  # Primary key dari Booking (berbasis integer)
            "fields": {
                "user": booking.user.id,
                "menu_items": booking.menu_items.id,
                "booking_date": booking.booking_date.strftime("%Y-%m-%dT%H:%M:%S"),  # Format ISO 8601
                "number_of_people": booking.number_of_people,
                "status": booking.status,
            }
        }
        booking_list.append(booking_entry)
    
    return JsonResponse(booking_list, safe=False)

@csrf_exempt
def delete_booking_flutter(request, booking_id):
    if request.method == 'POST':  # Hanya izinkan metode DELETE
        try:
            booking = get_object_or_404(Booking, id=booking_id)
            booking.delete()
            return JsonResponse({'message': 'Booking deleted successfully'}, status=200)
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def add_booking_flutter(request, menu_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parsing JSON dari request body
            booking_date = data.get('booking_date')
            number_of_people = data.get('number_of_people')

            if not all([booking_date, number_of_people]):
                return JsonResponse({'error': 'Missing required fields (booking_date or number_of_people)'}, status=400)
            
            user = request.user  # Menggunakan user dari request
            menu = get_object_or_404(Menu, id=menu_id)
            
            form = BookingForm({
                'booking_date': booking_date,
                'number_of_people': number_of_people
            })

            if form.is_valid():
                booking = form.save(commit=False)
                booking.user = user
                booking.menu_items = menu
                booking.status = 'waiting'  # Status default saat membuat booking
                booking.save()
                
                booking_data = {
                    'id': booking.id,
                    'menu': booking.menu_items.menu,
                    'booking_date': booking.booking_date.strftime("%B %d, %Y"),
                    'number_of_people': booking.number_of_people,
                    'restaurant_name': booking.menu_items.restaurant_name,
                    'city': booking.menu_items.city,
                    'rating': booking.menu_items.rating,
                    'status': booking.get_status_display(),
                    'image': booking.menu_items.image,
                }
                
                return JsonResponse({
                    'message': 'Booking added successfully', 
                    'booking': booking_data
                }, status=201)
            else:
                return JsonResponse({'error': 'Invalid form data', 'form_errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def edit_booking_flutter(request, booking_id):
    if request.method == 'POST':
        try:
            booking = get_object_or_404(Booking, id=booking_id)
            data = json.loads(request.body)  # Parsing JSON dari request body
            booking_date = data.get('booking_date')
            number_of_people = data.get('number_of_people')

            if not all([booking_date, number_of_people]):
                return JsonResponse({'error': 'Missing required fields (booking_date or number_of_people)'}, status=400)
            
            form = BookingForm({
                'booking_date': booking_date,
                'number_of_people': number_of_people
            }, instance=booking)
            
            if form.is_valid():
                booking = form.save(commit=False)
                booking.status = 'waiting'  # Status default saat mengedit booking
                booking.save()
                
                booking_data = {
                    'id': booking.id,
                    'menu': booking.menu_items.menu,
                    'booking_date': booking.booking_date.strftime("%B %d, %Y"),
                    'number_of_people': booking.number_of_people,
                    'restaurant_name': booking.menu_items.restaurant_name,
                    'city': booking.menu_items.city,
                    'rating': booking.menu_items.rating,
                    'status': booking.get_status_display(),
                    'image': booking.menu_items.image,
                }
                
                return JsonResponse({
                    'message': 'Booking edited successfully', 
                    'booking': booking_data
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid form data', 'form_errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def pantau_booking_owner_flutter(request):
    user = request.user
    claimed_restaurant = Menu.objects.filter(claimed_by=user)

    if not claimed_restaurant:
        return JsonResponse({
            'status': 'failed',
            'message': 'You do not own any restaurant.'
        })

    booking_list = []
    for menu in claimed_restaurant:
        bookings = Booking.objects.filter(menu_items=menu)

        for booking in bookings:
            booking_data = {
                "id": booking.id,
                "user": booking.user.username,
                "menu": booking.menu_items.restaurant_name,
                "booking_date": booking.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
                "number_of_people": booking.number_of_people,
                "status": booking.status,
            }
            booking_list.append(booking_data)

    return JsonResponse({
        'status': 'success',
        'restaurant': {
            "id": claimed_restaurant[0].id,
            "restaurant_name": claimed_restaurant[0].restaurant_name,
            "city": claimed_restaurant[0].city
        },
        'bookings': booking_list
    })

@login_required(login_url='/login')
@csrf_exempt
def approve_booking_flutter(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.user == booking.menu_items.claimed_by:
        booking.status = 'approved'
        booking.save()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'failed', 'message': 'You do not have permission to approve this booking.'})

@login_required(login_url='/login')
def booking_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    context = {'menu': menu}
    return render(request, 'booking/booking_detail.html', context)

@login_required(login_url='/login')
def resto_menu(request, menu_id):
    current_menu = get_object_or_404(Menu, id=menu_id)
    
    all_menus = Menu.objects.filter(restaurant_name=current_menu.restaurant_name)
    context = {
        'restaurant_name': current_menu.restaurant_name,
        'menus': all_menus,
        'menu_id': menu_id
    }
    return render(request, 'booking/resto_menu.html', context)

from django.http import JsonResponse

@login_required(login_url='/login')
def booking_detail_flutter(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    data = {
        'id': menu.id,
        'restaurant_name': menu.restaurant_name,
        'menu': menu.menu,
        'category': menu.category,
        'price': menu.price,
        'city': menu.city,
        'specialized': menu.specialized,
        'rating': menu.rating,
        'takeaway': menu.takeaway,
        'delivery': menu.delivery,
        'outdoor': menu.outdoor,
        'smoking_area': menu.smoking_area,
        'wifi': menu.wifi,
        'image': menu.image.url if menu.image else None,
    }
    return JsonResponse(data)

def resto_menu_flutter(request, menu_id):
    current_menu = get_object_or_404(Menu, id=menu_id)
    
    all_menus = Menu.objects.filter(restaurant_name=current_menu.restaurant_name)
    
    menu_list = []
    for menu in all_menus:
        menu_data = {
            'pk': menu.id, 
            'model': 'explore.menu',
            'fields': {
                'menu': menu.menu,
                'category': menu.category,
                'restaurant_name': menu.restaurant_name,
                'price': menu.price,
                'city': menu.city,
                'specialized': menu.specialized,
                'rating': menu.rating,
                'takeaway': menu.takeaway,
                'delivery': menu.delivery,
                'outdoor': menu.outdoor,
                'smoking_area': menu.smoking_area,
                'wifi': menu.wifi,
                'image': menu.image,
                'claimed_by': menu.claimed_by.username if menu.claimed_by else None,
            },
        }
        menu_list.append(menu_data)
    
    return JsonResponse({
        'status': 'success',
        'restaurant': {
            'restaurant_name': current_menu.restaurant_name,
            'city': current_menu.city,
        },
        'menus': menu_list
    }, status=200)
