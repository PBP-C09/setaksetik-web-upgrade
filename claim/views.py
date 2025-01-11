from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from explore.models import Menu
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

@login_required
def available_restaurants(request):
    # Jika resto owner sudah meng-claim restoran, langsung ke halaman restoran yang dimiliki
    user = request.user
    if user.userprofile.role == 'steakhouse owner':
        claimed_restaurant = Menu.objects.filter(claimed_by=user).first()
        if claimed_restaurant:
            return redirect('claim:owned_restaurant')
    
    # Jika belum claim restoran, tampilkan daftar restoran yang tersedia
    available_menus = Menu.objects.filter(claimed_by__isnull=True)
    context = {'available_menus': available_menus}
    return render(request, 'available_restaurants.html', context)

@login_required
def owned_restaurant(request):
    user = request.user
    claimed_restaurant = Menu.objects.filter(claimed_by=user).first()
    restaurant_menus = Menu.objects.filter(claimed_by=user)

    if not restaurant_menus:
        return redirect('claim:available_restaurants')
    
    context = {
        'restaurant': claimed_restaurant,
        'restaurant_menus': restaurant_menus,
    }
    return render(request, 'owned_restaurant.html', context)

@csrf_exempt
@login_required
def delete_ownership(request, restaurant_id):
    menu = Menu.objects.get(id=restaurant_id)

    if menu.claimed_by == request.user:
        Menu.objects.filter(restaurant_name=menu.restaurant_name).update(claimed_by=None)
    
    return redirect('/explore')

@login_required
def claim_restaurant(request, restaurant_id):
    user = request.user
    menu = Menu.objects.get(id=restaurant_id)
    menus_in_restaurant = Menu.objects.filter(restaurant_name=menu.restaurant_name)
    
    # Cek apakah user adalah 'steakhouse owner' dan belum claim restoran lain
    if user.userprofile.role == "steakhouse owner" and Menu.objects.filter(claimed_by=user).count() == 0:
        menus_in_restaurant.update(claimed_by=user)
        return redirect('claim:owned_restaurant')  # Redirect ke halaman restoran yang dimiliki
    else:
        return render(request, 'claim/error.html', {'message': 'You cannot claim more than one restaurant or you are not a steakhouse owner.'})

def is_admin(user):
    return user.is_staff  # Mengecek apakah user memiliki role admin

@csrf_exempt
@login_required
def manage_ownership(request):
    claimed_restaurants = Menu.objects.filter(claimed_by__isnull=False)  # Menampilkan semua restoran yang sudah di-claim

    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        menu = get_object_or_404(Menu, id=menu_id)
        menu.claimed_by = None  # Menghapus ownership
        menu.save()
        return redirect('claim:manage_ownership')

    context = {
        'claimed_restaurants': claimed_restaurants,
    }
    return render(request, 'manage_ownership.html', context)

@login_required(login_url='/login')
@csrf_exempt
def get_claimable_json(request):
    # Ambil restoran yang belum di-claim
    available_menus = Menu.objects.filter(claimed_by__isnull=True)
    
    # Format data untuk di-return sebagai JSON
    menu_list = []
    for menu in available_menus:
        menu_entry = {
            "model": "explore.menu",  # Nama model sesuai dengan Flutter
            "pk": menu.id,  # Primary key dari Menu
            "fields": {
                "menu": menu.menu,
                "category": menu.category,
                "restaurant_name": menu.restaurant_name,
                "image": menu.image,
                "city": menu.city,
                "price": menu.price,
                "rating": menu.rating,
                "specialized": menu.specialized,
                "takeaway": menu.takeaway,
                "delivery": menu.delivery,
                "outdoor": menu.outdoor,
                "smoking_area": menu.smoking_area,
                "wifi": menu.wifi,
                "claimed_by": None,  # Karena hanya restoran yang belum di-claim
                "review_count" : menu.review_count,
                "total_rating" : menu.total_rating
            }
        }
        menu_list.append(menu_entry)
    
    # Return data dalam format JSON
    return JsonResponse(menu_list, safe=False)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_menu(request):
    user = request.user
    claimed_restaurant = Menu.objects.filter(claimed_by=user).first()
    if request.method == "POST":
        menu = strip_tags(request.POST.get('menu_name'))
        category = request.POST.get('category').title()
        restaurant_name = claimed_restaurant.restaurant_name 
        city = claimed_restaurant.city
        price = request.POST.get('price')
        rating = request.POST.get('rating')
        specialized = claimed_restaurant.specialized
        takeaway = request.POST.get('takeaway') == 'on'
        delivery = request.POST.get('delivery') == 'on'
        outdoor = request.POST.get('outdoor') == 'on'
        smoking_area = request.POST.get('smoking_area') == 'on'
        wifi = request.POST.get('wifi') == 'on'
        image = request.POST.get('image_url')

        new_menu = Menu(menu=menu, category=category, restaurant_name=restaurant_name, city=city, 
                        price=price, rating=rating, specialized=specialized, takeaway=takeaway, delivery=delivery, 
                        outdoor=outdoor, smoking_area=smoking_area, wifi=wifi, image=image, claimed_by=user)
        new_menu.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

@login_required(login_url='/login')
@csrf_exempt
def claim_resto_flutter(request, restaurant_id):
    user = request.user
    menu = Menu.objects.get(id=restaurant_id)
    
    # Cek apakah user adalah 'steakhouse owner' dan belum claim restoran lain
    if user.userprofile.role == "steakhouse owner" and Menu.objects.filter(claimed_by=user).count() == 0:
        if menu.claimed_by is None:  # Pastikan restoran belum di-claim
            menu.claimed_by = user
            menu.save()
            return JsonResponse({'status': 'success', 'message': f'You have successfully claimed {menu.restaurant_name}.'})
        else:
            return JsonResponse({'status': 'failed', 'message': f'{menu.restaurant_name} has already been claimed.'})
    else:
        return JsonResponse({'status': 'failed', 'message': 'You cannot claim more than one restaurant or you are not a steakhouse owner.'})

@login_required(login_url='/login')
@csrf_exempt
def get_owned_restaurant_flutter(request):
    """Mengambil restoran yang dimiliki oleh steakhouse owner"""
    user = request.user
    claimed_restaurant = Menu.objects.filter(claimed_by=user).first()

    if not claimed_restaurant:
        return JsonResponse({'status': 'failed', 'message': 'You do not own any restaurant.'}, status=404)

    owned_restaurant = {
        "model": "explore.menu",
        "pk": claimed_restaurant.id,
        "fields": {
            "menu": claimed_restaurant.menu,
            "category": claimed_restaurant.category,
            "restaurant_name": claimed_restaurant.restaurant_name,
            "image": claimed_restaurant.image,
            "city": claimed_restaurant.city,
            "price": claimed_restaurant.price,
            "rating": claimed_restaurant.rating,
            "specialized": claimed_restaurant.specialized,
            "takeaway": claimed_restaurant.takeaway,
            "delivery": claimed_restaurant.delivery,
            "outdoor": claimed_restaurant.outdoor,
            "smoking_area": claimed_restaurant.smoking_area,
            "wifi": claimed_restaurant.wifi,
            "claimed_by": claimed_restaurant.claimed_by.id if claimed_restaurant.claimed_by else None,
            "review_count" : claimed_restaurant.review_count,
            "total_rating" : claimed_restaurant.total_rating
        }
    }

    return JsonResponse(owned_restaurant, safe=False)

@login_required(login_url='/login')
@csrf_exempt
def delete_ownership_flutter(request, restaurant_id):
    """
    Menghapus ownership restoran untuk user steakhouse owner.
    """
    try:
        menu = Menu.objects.get(id=restaurant_id)

        # Pastikan user memiliki restoran tersebut
        if menu.claimed_by == request.user:
            menu.claimed_by = None  # Set claimed_by menjadi null
            menu.save()
            return JsonResponse({'status': 'success', 'message': 'Ownership deleted successfully.'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'You do not own this restaurant.'}, status=403)
    except Menu.DoesNotExist:
        return JsonResponse({'status': 'failed', 'message': 'Restaurant not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
@csrf_exempt
@login_required
def manage_ownership_flutter(request):
    """API untuk mendapatkan semua restoran yang telah di-claim."""
    claimed_restaurants = Menu.objects.filter(claimed_by__isnull=False)
    claimed_list = [
        {
            "id": menu.id,
            "restaurant_name": menu.restaurant_name,
            "claimed_by": menu.claimed_by.username,
        }
        for menu in claimed_restaurants
    ]
    return JsonResponse({"status": "success", "claimed_restaurants": claimed_list})

@csrf_exempt
@login_required
def revoke_ownership_flutter(request):
    """API untuk menghapus ownership restoran."""
    if request.method == 'POST':
        menu_id = request.POST.get('menu_id')
        menu = get_object_or_404(Menu, id=menu_id)
        menu.claimed_by = None  # Menghapus ownership
        menu.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})

