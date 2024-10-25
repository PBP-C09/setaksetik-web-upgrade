# Create your views here
from django.shortcuts import render, redirect, get_object_or_404
from .models import Menu
from main.models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import MenuFilterForm
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required(login_url='/login')
def show_menu(request):
    user_profile = UserProfile.objects.get(user=request.user)
    menus = Menu.objects.all()
    form = MenuFilterForm(request.GET)
   
    context = {
        'form': form,
        'explore': menus,  
    }

    if form.is_valid():
        menu_name = form.cleaned_data.get("menu")
        kategori = form.cleaned_data.get("category")
        harga = form.cleaned_data.get("price")
        restaurant = form.cleaned_data.get("restaurant")
        kota = form.cleaned_data.get("city")
        specialization = form.cleaned_data.get("specialize")
        rate = form.cleaned_data.get("rating")

        if menu_name:
            menus = menus.filter(menu__icontains=menu_name)
        if kategori:
            menus = menus.filter(category__icontains=kategori)
        if harga:
            menus = menus.filter(price=harga)
        if restaurant:
            menus = menus.filter(restaurant_name__icontains=restaurant)
        if kota:
            menus = menus.filter(city__icontains=kota)
        if specialization:
            menus = menus.filter(specialized__icontains=specialization)
        if rate:
            menus = menus.filter(rating=rate)

        context['explore'] = menus  

    # Jika pengguna adalah admin
    if user_profile.role.casefold() == "admin":
        return render(request, 'menu_admin.html', context)
    
    if user_profile.role.casefold() == "steakhouse owner":
        return render(request, 'menu_owner.html', context)
    
    return render(request, 'menu.html', context)


def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    context = {'menu': menu}
    return render(request, 'menu_detail.html', context)

def admin_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    context = {'menu': menu}
    return render(request, 'admin_detail.html', context)

def owner_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    context = {'menu': menu}
    return render(request, 'owner_detail.html', context)

@csrf_exempt
@require_POST
def add_menu(request):
    if request.method == "POST":
        menu = request.POST.get('menu_name')
        category = request.POST.get('category')
        restaurant_name = request.POST.get('restaurant_name')
        city = request.POST.get('city')
        price = request.POST.get('price')
        rating = request.POST.get('rating')
        specialized = request.POST.get('specialized')
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

def get_menu(request):
    data = Menu.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_menu_by_id(request, id):
    data = Menu.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def edit_menu(request, id):
    data = Menu.objects.filter(pk=id)
    form = MenuFilterForm(request.POST or None, instance=data)
    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('explore:show_menu'))

    context = {'form': form}
    return render(request, "edit_menu.html", context)

def delete_menu(request, id):
    data = Menu.objects.filter(pk=id)
    data.delete()
    return HttpResponseRedirect(reverse('explore:show_menu'))

@csrf_exempt
def filter_menu(request):
    menu_name = request.GET.get('menu', '')
    kategori = request.GET.get('category', '')
    harga = request.GET.get('price', None)
    restaurant = request.GET.get('restaurant', '')
    kota = request.GET.get('city', '')
    specialization = request.GET.get('specialize', '')
    rate = request.GET.get('rating', None)

    menus = Menu.objects.all()
    if menu_name:
         menus = menus.filter(menu__icontains=menu_name)

    if kategori:
        menus = menus.filter(category__icontains=kategori)

    if harga:
        menus = menus.filter(price=harga)

    if restaurant:
        menus = menus.filter(restaurant_name__icontains=restaurant)

    if kota:
        menus = menus.filter(city__icontains=kota)

    if specialization:
        menus = menus.filter(specialized__icontains=specialization)

    if rate:
        menus = menus.filter(rating=rate)
    menu_json = serializers.serialize('json', menus)
    return JsonResponse(menu_json, safe=False)