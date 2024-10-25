from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
import json

from explore.models import Menu
from .models import Option, SpinHistory

@login_required(login_url='/login')
def menu_view(request):
    categories = ['All Categories', 'Beef', 'Chicken', 'Fish', 'Lamb', 'Pork', 'Rib Eye', 'Sirloin', 'Tenderloin', 'T-Bone', 'Wagyu', 'Other']

    options = Menu.objects.all()

    context = {
        'user': request.user,
        'categories': categories,
        'options': options, 
    }
    
    return render(request, 'lmao.html', context)

def history_json(request):
    data = SpinHistory.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def option_json(request, selected_category="All Categories"):
    if selected_category == "All Categories":
        data = Menu.objects.all()
    else:
        data = Menu.objects.filter(category=selected_category)

    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def add_spin_history(request):
    winner = request.POST.get("winner")
    user = request.user

    # Create new SpinHistory entry
    if winner:
        spin_history = SpinHistory(
            user=user,
            winner=winner,
        )
        spin_history.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponse(b"BAD REQUEST", status=400)

def delete_spin_history(request, id):
    spin_history = SpinHistory.objects.get(pk = id)
    spin_history.delete()
    return HttpResponseRedirect(reverse('spinthewheel:menu_view'))

from django.http import JsonResponse