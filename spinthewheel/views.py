from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

from explore.models import Menu
from main.models import UserProfile
from spinthewheel.models import SpinHistory, SecretHistory
from spinthewheel.forms import SpinHistoryForm

@login_required(login_url='/login')
def spin_view(request):
    categories = ['All Categories', 'Beef', 'Chicken', 'Fish', 'Lamb', 'Pork', 'Rib Eye', 'Sirloin', 'Tenderloin', 'T-Bone', 'Wagyu', 'Other']

    options = Menu.objects.all()
    context = {
        'user': request.user,
        'categories': categories,
        'options': options, 
    }

    if request.user.userprofile.role == "admin":
        return render(request, 'spin-secret.html', context)

    return render(request, 'spin.html', context)

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
    form = SpinHistoryForm(request.POST or None)

    # Create new SpinHistory entry
    if form.is_valid() and request.method == "POST":
        spin_history = form.save(commit=False)
        spin_history.user = request.user
        spin_history.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponse(b"BAD REQUEST", status=400)

def delete_spin_history(request, id):
    spin_history = SpinHistory.objects.get(pk = id)
    spin_history.delete()
    return HttpResponseRedirect(reverse('spinthewheel:spin_view'))

def secret_view(request):
    context = {
        'user': request.user,
    }
    
    return render(request, 'spin-secret.html', context)

def secret_json(request):
    data = SecretHistory.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def add_secret_history(request):
    user = request.user
    winner = request.POST.get("winner")

    if winner:
        secret_history = SecretHistory(
            user=user,
            winner=winner,
        )
        secret_history.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponse(b"BAD REQUEST", status=400)

def delete_secret_history(request, id):
    secret_history = SecretHistory.objects.get(pk = id)
    secret_history.delete()
    return HttpResponseRedirect(reverse('spinthewheel:secret_view'))

