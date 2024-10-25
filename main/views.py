import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render, redirect
from main.forms import MenuItemForm  
from main.models import MenuItem
from .models import MeatupRequest, Wishlist

@login_required(login_url='/login')
def show_main(request):
    menu_items = MenuItem.objects.all()

    context = {
        'name': 'SetakSetik',
        'class': 'PBP C',
        'menu_items': menu_items,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def create_menu_item(request):
    form = MenuItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_menu_item.html", context)

@login_required(login_url='/login')
def wishlist_list(request):
    wishlist_items = Wishlist.objects.all()  # Fetch all wishlist items
    
    context = {
        'wishlist_items': wishlist_items,
        'last_login': request.COOKIES.get('last_login', 'Unknown'),  # Ensure 'last_login' cookie is handled
    }

    return render(request, 'wishlist_list.html', context)

from django.shortcuts import get_object_or_404, redirect
from .models import MeatupRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def agree_request(request, request_id):
    meatup_request = get_object_or_404(MeatupRequest, id=request_id, receiver=request.user)
    
    if meatup_request.status == 'pending':  # Only allow if the request is still pending
        meatup_request.status = 'accepted'
        meatup_request.save()
        messages.success(request, 'You have accepted the meetup request.')
    else:
        messages.error(request, 'This request has already been processed.')
    
    return redirect('main:request_list')  # Redirect to the request list after action

@login_required
def decline_request(request, request_id):
    meatup_request = get_object_or_404(MeatupRequest, id=request_id, receiver=request.user)
    
    if meatup_request.status == 'pending':  # Only allow if the request is still pending
        meatup_request.status = 'declined'
        meatup_request.save()
        messages.success(request, 'You have declined the meetup request.')
    else:
        messages.error(request, 'This request has already been processed.')
    
    return redirect('main:request_list')  # Redirect to the request list after action

@login_required
def request_list(request):
    requests = MeatupRequest.objects.filter(receiver=request.user)

    context = {
        'requests': requests,
    }

    return render(request, 'request_list.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
      
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def show_xml(request):
    data = MenuItem.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = MenuItem.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = MenuItem.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = MenuItem.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
