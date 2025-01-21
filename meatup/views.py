
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from .models import Message
from .forms import MessageEntryForm
from main.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.db import models
import json

@csrf_exempt
@login_required(login_url='/login')
def meatup_home(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    
    sent_messages = Message.objects.filter(
        sender=user_profile,
        status='PENDING' 
    ).order_by('-timestamp')
    received_messages = Message.objects.filter(
        receiver=user_profile, 
        status='PENDING'
    ).order_by('-timestamp')
    accepted_messages = Message.objects.filter(
        status='ACCEPTED'
    ).filter(
        models.Q(sender=user_profile) | models.Q(receiver=user_profile)
    ).order_by('-timestamp')
    rejected_messages = Message.objects.filter(
        status='REJECTED'
    ).filter(
        models.Q(sender=user_profile) | models.Q(receiver=user_profile)
    ).order_by('-timestamp')

    context = {
        'sent_messages': sent_messages,
        'received_messages': received_messages,
        'accepted_messages': accepted_messages,
        'rejected_messages': rejected_messages,
    }
    return render(request, 'meatup.html', context)

@csrf_exempt
@login_required(login_url='/login')
def create_message_entry(request):
    if request.method == "POST":
        form = MessageEntryForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            user_profile = UserProfile.objects.get(user=request.user)
            new_message.sender = user_profile
            new_message.status = 'PENDING'
            new_message.save()
            return redirect(reverse('meatup:meatup_home'))
    else:
        form = MessageEntryForm()
    
    context = {'form': form}
    return render(request, 'create_message_entry.html', context)

@csrf_exempt
@login_required(login_url='/login')
def delete_message(request, id):
    message = get_object_or_404(Message, id=id)
    message.delete()
    return redirect('meatup:meatup_home')

@csrf_exempt
@login_required(login_url='/login')
def edit_message(request, id):
    message = get_object_or_404(Message, id=id)
    if request.method == "POST":
        form = MessageEntryForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('meatup:meatup_home'))
    else:
        form = MessageEntryForm(instance=message)

    context = {'form': form, 'message_id': id}
    return render(request, 'create_message_entry.html', context)

@csrf_exempt
@login_required(login_url='/login')
def accept_message(request, id):
    message = get_object_or_404(Message, id=id)
    if request.user == message.receiver.user:
        message.status = 'ACCEPTED'
        message.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=403)

@csrf_exempt
@login_required(login_url='/login')
def reject_message(request, id):
    message = get_object_or_404(Message, id=id)
    if request.user == message.receiver.user:
        message.status = 'REJECTED'
        message.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=403)

@csrf_exempt
@login_required(login_url='/login')
def meatup_home_flutter(request):
    user = request.user
    sender_user_profile = UserProfile.objects.get(user=user)
    
    sent_messages = Message.objects.filter(sender=sender_user_profile).select_related('receiver__user', 'sender__user').order_by('-timestamp')
    received_messages = Message.objects.filter(receiver=sender_user_profile).select_related('receiver__user', 'sender__user').order_by('-timestamp')

    sent_messages_data = [{
        'id': msg.id,
        'sender': msg.sender.user.username,
        'receiver': msg.receiver.user.username,
        'receiver_id': msg.receiver.id,
        'title': msg.title,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        'status': message.status,
    } for msg in sent_messages]

    received_messages_data = [{
        'id': msg.id,
        'sender': msg.sender.user.username,
        'sender_id': msg.sender.id,
        'receiver': msg.receiver.user.username,
        'title': msg.title,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        'status': message.status
    } for msg in received_messages]

    response_data = {
        'sent_messages': sent_messages_data,
        'received_messages': received_messages_data,
    }
    return JsonResponse(response_data)

@csrf_exempt
@login_required(login_url='/login')
def create_message_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            sender_user_profile = UserProfile.objects.get(user=request.user)
            
            try:
                receiver_username = data.get("receiver")
                receiver_user_profile = UserProfile.objects.get(user=User.objects.get(username=receiver_username))
            except UserProfile.DoesNotExist:
                return JsonResponse({
                    "status": "error",
                    "message": "Receiver not found"
                }, status=404)
            
            new_message = Message.objects.create(
                sender=sender_user_profile,
                receiver=receiver_user_profile,
                title=data.get("title"),
                content=data.get("content")
            )
            
            return JsonResponse({
                "status": "success",
                "message": "Message sent successfully"
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON format"
            }, status=400)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=500)
    
    return JsonResponse({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)

@csrf_exempt
@login_required(login_url='/login')
def delete_message_flutter(request, id):
    message = get_object_or_404(Message, id=id)
    message.delete()
    return JsonResponse({"status": "success", "message": "Message deleted successfully."}, status=200)

@csrf_exempt
@login_required(login_url='/login')
def edit_message_flutter(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = get_object_or_404(Message, id=id)

        if message.sender.user == request.user:
            message.title = data.get("title", message.title)
            message.content = data.get("content", message.content)
            message.save()

            return JsonResponse({"status": "success", "message": "Message updated successfully."}, status=200)

        return JsonResponse({"status": "error", "message": "Unauthorized action."}, status=403)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

@csrf_exempt
@login_required(login_url='/login')
def get_receivers(request):
    steak_lovers = UserProfile.objects.filter(role="steak lover")
    receivers = [{
        'username': profile.user.username,
        'full_name': profile.full_name
    } for profile in steak_lovers]
    return JsonResponse(receivers, safe=False)

@csrf_exempt
def get_messages_json(request):
    user = request.user
    sender_user_profile = UserProfile.objects.get(user=user)
    receiver_user_profile = UserProfile.objects.get(user=user)

    sent_messages = Message.objects.filter(sender=sender_user_profile).order_by('-timestamp')
    received_messages = Message.objects.filter(receiver=receiver_user_profile).order_by('-timestamp')

    sent_messages_data = [{
        'id': message.id,
        'sender': message.sender.full_name,
        'receiver': message.receiver.full_name,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M'),
        'title': message.title,
        'content': message.content,
        'status': message.status,
    } for message in sent_messages]

    received_messages_data = [{
        'id': message.id,
        'sender': message.sender.full_name,
        'receiver': message.receiver.full_name,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M'),
        'title': message.title,
        'content': message.content,
        'status': message.status
    } for message in received_messages]

    return JsonResponse({
        'status': 'success',
        'sent_messages': sent_messages_data,
        'received_messages': received_messages_data,
    })

@csrf_exempt
@login_required(login_url='/login')
def accept_message_flutter(request, id):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=id)
        if request.user == message.receiver.user:
            message.status = 'ACCEPTED'
            message.save()
            return JsonResponse({"status": "success", "message": "Message accepted successfully."}, status=200)
        return JsonResponse({"status": "error", "message": "Unauthorized action."}, status=403)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

@csrf_exempt
@login_required(login_url='/login')
def reject_message_flutter(request, id):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=id)
        if request.user == message.receiver.user:
            message.status = 'REJECTED'
            message.save()
            return JsonResponse({"status": "success", "message": "Message rejected successfully."}, status=200)
        return JsonResponse({"status": "error", "message": "Unauthorized action."}, status=403)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)