from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from explore.models import Menu
from django.contrib.auth.models import User

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

    if not claimed_restaurant:
        return redirect('claim:available_restaurants')
    
    context = {'restaurant': claimed_restaurant}
    return render(request, 'owned_restaurant.html', context)

@login_required
def delete_ownership(request, restaurant_id):
    menu = Menu.objects.get(id=restaurant_id)

    if menu.claimed_by == request.user:
        menu.claimed_by = None  # Menghapus kepemilikan
        menu.save()
    
    return redirect('/explore')

@login_required
def claim_restaurant(request, restaurant_id):
    user = request.user
    menu = Menu.objects.get(id=restaurant_id)
    
    # Cek apakah user adalah 'steakhouse owner' dan belum claim restoran lain
    if user.userprofile.role == "steakhouse owner" and Menu.objects.filter(claimed_by=user).count() == 0:
        menu.claimed_by = user
        menu.save()
        return redirect('claim:owned_restaurant')  # Redirect ke halaman restoran yang dimiliki
    else:
        return render(request, 'claim/error.html', {'message': 'You cannot claim more than one restaurant or you are not a steakhouse owner.'})

def is_admin(user):
    return user.is_staff  # Mengecek apakah user memiliki role admin

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