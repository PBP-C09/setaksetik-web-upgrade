import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import MeatupRequest, Wishlist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_requests(request):

    requests = MeatupRequest.objects.filter(receiver=request.user)

    context = {
        'nama' : 'steak',
        'lokasi' : 'jaksel',
        'rating' : '5',
    }
    return render(request, 'meatup.html', context)

@login_required
def request_list(request):
    requests = MeatupRequest.objects.filter(receiver=request.user)
    return render(request, 'meatup/request_list.html', {'requests': requests})

@login_required
def received_requests(request):
    requests = MeatupRequest.objects.filter(receiver=request.user)
    return render(request, 'meatup/received_requests.html', {'requests': requests})

@login_required
def create_request(request, wishlist_id):
    wishlist = get_object_or_404(Wishlist, id=wishlist_id)

    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        receiver = get_object_or_404(User, id=receiver_id)

        new_request = MeatupRequest.objects.create(
            sender=request.user,
            receiver=receiver,
            wishlist=wishlist
        )

        return JsonResponse({
            'id': new_request.id,
            'sender': new_request.sender.username,
            'wishlist': wishlist.item,
            'status': new_request.status
        })

    users = User.objects.exclude(id=request.user.id)  
    return render(request, 'meatup/create_request.html', {'wishlist': wishlist, 'users': users})

@login_required
def update_request_status(request, pk):
    meatup_request = get_object_or_404(MeatupRequest, pk=pk)

    if request.method == 'POST':
        data = json.loads(request.body) 
        new_status = data.get('status')

        if new_status in dict(MeatupRequest.STATUS_CHOICES):
            meatup_request.status = new_status
            meatup_request.save()

            return JsonResponse({'message': 'Status updated successfully!', 'status': new_status})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_request(request, pk):
    meatup_request = get_object_or_404(MeatupRequest, pk=pk)

    if request.method == 'POST':
        meatup_request.delete()

        return JsonResponse({'message': 'Request deleted successfully!', 'id': pk})

    return JsonResponse({'error': 'Invalid request'}, status=400)