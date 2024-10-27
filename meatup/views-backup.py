import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import MeatupRequest, Wishlist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

@login_required(login_url='/login')
def show_requests(request):
    requests = MeatupRequest.objects.filter(receiver=request.user)

    context = {
        'nama': 'steak',
        'lokasi': 'jaksel',
        'rating': '5',
        'requests': requests,  # Include requests in context
    }
    return render(request, 'meatup.html', context)

@login_required
def request_list(request):
    requests = MeatupRequest.objects.filter(receiver=request.user)
    context = {
        'requests': requests,
    }
    return render(request, 'meatup/request_list.html', context)

@login_required
def received_requests(request):
    requests = MeatupRequest.objects.filter(receiver=request.user)
    return render(request, 'received_requests.html', {'requests': requests})

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
            'wishlist': wishlist.item_name,  # Adjusted based on Wishlist field
            'status': new_request.status
        })

    users = User.objects.exclude(id=request.user.id)  
    return render(request, 'meatup/create_request.html', {'wishlist': wishlist, 'users': users})

@login_required(login_url='/login')
def wishlist_list(request):
    wishlist_items = Wishlist.objects.filter(owner=request.user)  # Fetch user's wishlist items
    
    context = {
        'wishlist_items': wishlist_items,
        'last_login': request.COOKIES.get('last_login', 'Unknown'),  # Ensure 'last_login' cookie is handled
    }

    return render(request, 'wishlist_list.html', context)

@require_POST
@login_required
def add_to_wishlist(request):
    try:
        data = json.loads(request.body)
        item_name = data.get('item_name')
        description = data.get('description', '')
        is_public = data.get('is_public', True)

        if not item_name:
            return JsonResponse({'error': 'Item name is required'}, status=400)

        new_item = Wishlist.objects.create(
            owner=request.user,
            item_name=item_name,
            description=description,
            is_public=is_public
        )
        return JsonResponse({
            'id': new_item.id,
            'item_name': new_item.item_name,
            'description': new_item.description,
            'is_public': new_item.is_public,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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