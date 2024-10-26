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
from main.models import MenuItem
from .models import MeatupRequest, Wishlist
from main.models import UserProfile
from main.forms import UserProfileForm

@login_required(login_url='/login')
def show_main(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'role': user_profile.role,
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

# @login_required(login_url='/login')
# def wishlist_list(request):
#     wishlist_items = Wishlist.objects.all()  # Fetch all wishlist items
    
#     context = {
#         'wishlist_items': wishlist_items,
#         'last_login': request.COOKIES.get('last_login', 'Unknown'),  # Ensure 'last_login' cookie is handled
#     }

#     return render(request, 'wishlist_list.html', context)

# from django.shortcuts import get_object_or_404, redirect
# from .models import MeatupRequest
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# @login_required
# def agree_request(request, request_id):
#     meatup_request = get_object_or_404(MeatupRequest, id=request_id, receiver=request.user)
    
#     if meatup_request.status == 'pending':  # Only allow if the request is still pending
#         meatup_request.status = 'accepted'
#         meatup_request.save()
#         messages.success(request, 'You have accepted the meetup request.')
#     else:
#         messages.error(request, 'This request has already been processed.')
    
#     return redirect('main:request_list')  # Redirect to the request list after action

# @login_required
# def decline_request(request, request_id):
#     meatup_request = get_object_or_404(MeatupRequest, id=request_id, receiver=request.user)
    
#     if meatup_request.status == 'pending':  # Only allow if the request is still pending
#         meatup_request.status = 'declined'
#         meatup_request.save()
#         messages.success(request, 'You have declined the meetup request.')
#     else:
#         messages.error(request, 'This request has already been processed.')
    
#     return redirect('main:request_list')  # Redirect to the request list after action

# @login_required
# def request_list(request):
#     requests = MeatupRequest.objects.filter(receiver=request.user)

#     context = {
#         'requests': requests,
#     }

#     return render(request, 'request_list.html', context)

def register(request):
    form = UserProfileForm()

    if request.method == "POST":
        form = UserProfileForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)

            if request.POST.get('is_admin'):
                role = 'admin'
            else:
                role = form.cleaned_data["role"]

            user.save()
            UserProfile.objects.create(user=user, full_name=form.cleaned_data["full_name"], role=role)
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
            for error in form.non_field_errors():
                messages.error(request, error)
      
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response