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
from main.models import UserProfile
from main.forms import UserProfileForm

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
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response

def forbidden(request):
    return render(request, 'forbidden.html')