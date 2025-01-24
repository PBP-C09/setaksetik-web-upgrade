from django.shortcuts import render, redirect, get_object_or_404
from .models import Menu
from main.models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import MenuFilterForm, AddMenuForm
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

# Fungsi untuk menampilkan semua menu
@login_required(login_url='/login')
def show_menu(request):
     # Filter menu berdasarkan role user
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.role.casefold() == "admin" :
        menus = Menu.objects.all()
    elif user_profile.role.casefold() == "steakhouse owner":
        menus = Menu.objects.filter(claimed_by=None)
    else:
        menus = Menu.objects.all()
    form = MenuFilterForm(request.GET)
   
    context = {
        'form': form,
        'explore': menus,  
    }

    # Proses filter berdasarkan input user
    if form.is_valid():
        menu_name = form.cleaned_data.get("menu")
        kategori = form.cleaned_data.get("category")
        min_harga = form.cleaned_data.get("min_price")
        max_harga = form.cleaned_data.get("max_price")
        restaurant = form.cleaned_data.get("restaurant")
        kota = form.cleaned_data.get("city")
        specialization = form.cleaned_data.get("specialized")
        min_rate = form.cleaned_data.get("min_rating")
        max_rate = form.cleaned_data.get("max_rating")

        if menu_name:
            menus = menus.filter(menu__icontains=menu_name)
        if kategori:
            menus = menus.filter(category__icontains=kategori)
        if min_harga is not None and max_harga is not None:
            menus = menus.filter(price__gte=min_harga, price__lte=max_harga)
        if restaurant:
            menus = menus.filter(restaurant_name__icontains=restaurant)
        if kota:
            menus = menus.filter(city__icontains=kota)
        if specialization:
            menus = menus.filter(specialized__icontains=specialization)
        if min_rate is not None and max_rate is not None:
            menus = menus.filter(rating__gte=min_rate, rating__lte=max_rate)

        context['explore'] = menus  

    # Jika pengguna adalah admin
    if user_profile.role.casefold() == "admin":
        return render(request, 'menu_admin.html', context)
    
    # Jika pengguna adalah owner
    if (user_profile.role.casefold() == "steakhouse owner"):
        if (Menu.objects.filter(claimed_by=request.user).count() == 0):
            return render(request, 'menu_owner.html', context)
        else:
            return redirect('claim:owned_restaurant')
        
    # Jika pengguna adalah steaklover
    return render(request, 'menu.html', context)

# Fungsi untuk menampilkan menu detail
@login_required(login_url='/login')
def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    context = {'menu': menu}
    return render(request, 'menu_detail.html', context)

# Fungsi untuk menampilkan menu detail
@login_required(login_url='/login')
def admin_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    context = {'menu': menu}
    return render(request, 'admin_detail.html', context)

@login_required(login_url='/login')
def owner_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    context = {'menu': menu}
    return render(request, 'owner_detail.html', context)

# Fungsi untuk menambah menu 
@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_menu(request):
    if request.method == "POST":
        menu = strip_tags(request.POST.get('menu_name'))
        category = request.POST.get('category').title()
        restaurant_name = strip_tags(request.POST.get('restaurant_name'))
        city = request.POST.get('city').title()
        price = request.POST.get('price')
        rating = request.POST.get('rating')
        specialized = request.POST.get('specialized').title()
        takeaway = request.POST.get('takeaway') == 'on'
        delivery = request.POST.get('delivery') == 'on'
        outdoor = request.POST.get('outdoor') == 'on'
        smoking_area = request.POST.get('smoking_area') == 'on'
        wifi = request.POST.get('wifi') == 'on'
        image = request.POST.get('image_url')

        new_menu = Menu(menu=menu, category=category, restaurant_name=restaurant_name, city=city, 
                        price=price, rating=rating, specialized=specialized, takeaway=takeaway, delivery=delivery, 
                        outdoor=outdoor, smoking_area=smoking_area, wifi=wifi, image=image)
        new_menu.save()
        return HttpResponse(b"CREATED", status=201)
    return HttpResponseNotFound()

# Fungsi untuk mendapatkan semua menu dalam format JSON
@login_required(login_url='/login')
def get_menu(request):
    data = Menu.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Fungsi untuk mendapatkan menu berdasarkan ID dalam format JSON
@login_required(login_url='/login')
def get_menu_by_id(request, id):
    data = Menu.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Fungsi untuk edit menu 
@csrf_exempt
@login_required(login_url='/login')
def edit_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    
    if request.method == 'POST':
        form = AddMenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('explore:show_menu') 
    else:
        form = AddMenuForm(instance=menu)

    return render(request, 'edit_menu.html', {'form': form, 'menu': menu})

# Fungsi untuk hapus menu 
@login_required(login_url='/login')
def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    menu.delete()
    return redirect('explore:show_menu')

# Fungsi untuk filter menu 
@csrf_exempt
@login_required(login_url='/login')
def filter_menu(request):
    menu_name = request.GET.get('menu', '')
    kategori = request.GET.get('category', '')
    min_harga = request.GET.get('min_price', None)
    max_harga = request.GET.get('max_price', None)
    restaurant = request.GET.get('restaurant', '')
    kota = request.GET.get('city', '')
    specialization = request.GET.get('specialized', '')
    min_rate = request.GET.get('min_rating', None)
    max_rate = request.GET.get('max_rating', None)

    menus = Menu.objects.all()
    if menu_name:
         menus = menus.filter(menu__icontains=menu_name)

    if kategori:
        menus = menus.filter(category__icontains=kategori)

    if min_harga is not None and max_harga is not None:
        menus = menus.filter(price__gte=min_harga, price__lte=max_harga)

    if restaurant:
        menus = menus.filter(restaurant_name__icontains=restaurant)

    if kota:
        menus = menus.filter(city__icontains=kota)

    if specialization:
        menus = menus.filter(specialized__=specialization)

    if min_rate is not None and max_rate is not None:
            menus = menus.filter(rating__gte=min_rate, rating__lte=max_rate)
    menu_json = serializers.serialize('json', menus)
    return JsonResponse(menu_json, safe=False)

# Fungsi untuk Menampilkan data dalam format XML
@login_required(login_url='/login')
def show_xml(request):
    data = Menu.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Fungsi untuk Menampilkan data dalam format JSON
@login_required(login_url='/login')
def show_json(request):
    data = Menu.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Fungsi untuk Menampilkan data berdasarkan ID dalam format XML
@login_required(login_url='/login')
def show_xml_by_id(request, id):
    data = Menu.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# Fungsi untuk Menampilkan data berdasarkan ID dalam format JSON
@login_required(login_url='/login')
def show_json_by_id(request, id):
    data = Menu.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# Fungsi untuk menambah menu di flutter
@csrf_exempt
def create_flutter(request):    
    if request.method == 'POST':
        try:         
            data = json.loads(request.body)
            # Create new menu
            new_menu = Menu.objects.create(
                menu=data["menu"],
                category=data["category"].title(),
                restaurant_name=data["restaurant_name"],
                city=data["city"].title(),
                price=int(data["price"]),  
                rating=float(data["rating"]),
                specialized=data["specialized"].title(),
                image=data.get("image", "default_image_url"),
                takeaway=string_to_bool(data["takeaway"]),
                delivery=string_to_bool(data["delivery"]),
                outdoor=string_to_bool(data["outdoor"]),
                smoking_area=string_to_bool(data["smoking_area"]),
                wifi=string_to_bool(data["wifi"]),
            )
            new_menu.save()
            
            return JsonResponse({"status": "success", "message": "Menu added successfully"}, status=200)
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

# Fungsi untuk edit menu di flutter
@csrf_exempt
def edit_flutter(request, menu_id):
    if request.method == 'POST':
        try:
            menu = Menu.objects.get(pk=menu_id) 
            data = json.loads(request.body)
           
            # Update fields
            menu.menu = data.get('menu', menu.menu)
            menu.category = data.get('category', menu.category)
            menu.restaurant_name = data.get('restaurant_name', menu.restaurant_name)
            menu.city = data.get('city', menu.city)
            menu.price = int(data.get('price', menu.price))
            menu.rating = float(data.get('rating', menu.rating))
            menu.specialized = data.get('specialized', menu.specialized)
            menu.image = data.get('image', menu.image)
            menu.takeaway = string_to_bool(data.get('takeaway', menu.takeaway))
            menu.delivery = string_to_bool(data.get('delivery', menu.delivery))
            menu.outdoor = string_to_bool(data.get('outdoor', menu.outdoor))
            menu.smoking_area = string_to_bool(data.get('smoking_area', menu.smoking_area))
            menu.wifi = string_to_bool(data.get('wifi', menu.wifi))
            
            menu.save()
            return JsonResponse({
                "status": "success",
                "message": "Menu updated successfully!"
            }, status=200)
        except Menu.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Menu not found!"
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)
    return JsonResponse({
        "status": "error",
        "message": "Invalid method"
    }, status=405)

# Fungsi untuk mengubah string jadi boolean
def string_to_bool(value): 
    if isinstance(value, bool):  
        return value

    if isinstance(value, str): 
        value = value.strip().lower()  
        
        if value in ('true'):
            return True
        elif value in ('false'):
            return False