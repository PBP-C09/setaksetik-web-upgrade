from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from explore.models import Menu

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
    
    return redirect('claim:available_restaurants')

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
