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

# Create your views here.
# Steak Lover (Customer)
@login_required
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

@login_required
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


@login_required
def delete_booking(request, booking_id):
    if request.method == 'DELETE':  # Hanya bisa method DELETE
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            booking.delete()
            return JsonResponse({'message': 'Booking deleted successfully'}, status=200)
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
@login_required
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
@login_required
def pantau_booking_owner(request):
    # Cek apakah user memiliki restoran yang sudah di-claim
    user = request.user
    claimed_restaurant = Menu.objects.filter(claimed_by=user).first()

    context = {
        'restaurant': claimed_restaurant
    }

    # Jika user memiliki restoran yang sudah di-claim, ambil daftar booking
    if claimed_restaurant:
        bookings = Booking.objects.filter(menu_items=claimed_restaurant)
        context['bookings'] = bookings

    return render(request, 'booking/pantau_booking_owner.html', context)

@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.user == booking.menu_items.claimed_by:  # Memastikan hanya owner yang bisa approve
        booking.status = 'approved'
        booking.save()

    return redirect('booking:pantau_booking_owner')  # Redirect kembali ke pantau booking owner


@login_required
def show_booking_xml(request):
    data = Booking.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


@login_required
def show_booking_json(request):
    data = Booking.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required
def show_booking_xml_by_id(request, booking_id):
    data = Booking.objects.filter(pk=booking_id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required
def show_booking_json_by_id(request, booking_id):
    data = Booking.objects.filter(pk=booking_id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")