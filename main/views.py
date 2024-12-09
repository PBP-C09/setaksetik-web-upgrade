import datetime
import json

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from main.models import UserProfile
from main.forms import UserProfileForm

@csrf_exempt
def show_main(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {
            'role': user_profile.role,
            'last_login': request.COOKIES['last_login'],
        }
    else:
        context = None

    return render(request, "main.html", context)

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
def forbidden(request):
    return render(request, 'forbidden.html')

@csrf_exempt
def login_mobile(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            user_profile = UserProfile.objects.get(user=user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "full_name": user_profile.full_name, # gada
                "role": user_profile.role, # gada
                "status": True,
                "message": "Logged in!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Failed to log in."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Failed to log in!\nRecheck your username and password."
        }, status=401)
    
@csrf_exempt
def register_mobile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        role = data['role']
        full_name = data['full_name']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user and user profile
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        UserProfile.objects.create(user=user, full_name=full_name, role=role)

        print(user.username)
        print(lmao)
        
        return JsonResponse({
            "username": user.username,
            "full_name": full_name,
            "role": role,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

@csrf_exempt
def logout_mobile(request):
    username = request.user.username

    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)