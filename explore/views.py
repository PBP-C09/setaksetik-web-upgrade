# Create your views here
from django.shortcuts import render, redirect, get_object_or_404
from .models import Menu
from main.models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import MenuFilterForm, AddMenuForm
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import strip_tags

@login_required(login_url='/login')
def show_menu(request):
    user_profile = UserProfile.objects.get(user=request.user)
    menus = Menu.objects.filter(claimed_by=None)
    form = MenuFilterForm(request.GET)
   
    context = {
        'form': form,
        'explore': menus,  
    }

    if form.is_valid():
        menu_name = form.cleaned_data.get("menu")
        kategori = form.cleaned_data.get("category")
        min_harga = form.cleaned_data.get("min_price")
        max_harga = form.cleaned_data.get("max_price")
        restaurant = form.cleaned_data.get("restaurant")
        kota = form.cleaned_data.get("city")
        specialization = form.cleaned_data.get("specialize")
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
    
    if (user_profile.role.casefold() == "steakhouse owner"):
        if (Menu.objects.filter(claimed_by=request.user).count() == 0):
            return render(request, 'menu_owner.html', context)
        else:
            return redirect('claim:owned_restaurant')
    
    return render(request, 'menu.html', context)

@login_required(login_url='/login')
def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    context = {'menu': menu}
    return render(request, 'menu_detail.html', context)

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

@login_required(login_url='/login')
def get_menu(request):
    data = Menu.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
def get_menu_by_id(request, id):
    data = Menu.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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

@login_required(login_url='/login')
def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    menu.delete()
    return redirect('explore:show_menu')

@csrf_exempt
@login_required(login_url='/login')
def filter_menu(request):
    menu_name = request.GET.get('menu', '')
    kategori = request.GET.get('category', '')
    min_harga = request.GET.get('min_price', None)
    max_harga = request.GET.get('max_price', None)
    restaurant = request.GET.get('restaurant', '')
    kota = request.GET.get('city', '')
    specialization = request.GET.get('specialize', '')
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
        menus = menus.filter(specialized__icontains=specialization)

    if min_rate is not None and max_rate is not None:
            menus = menus.filter(rating__gte=min_rate, rating__lte=max_rate)
    menu_json = serializers.serialize('json', menus)
    return JsonResponse(menu_json, safe=False)

@login_required(login_url='/login')
def show_xml(request):
    data = Menu.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url='/login')
def show_json(request):
    data = Menu.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
def show_xml_by_id(request, id):
    data = Menu.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@login_required(login_url='/login')
def show_json_by_id(request, id):
    data = Menu.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")