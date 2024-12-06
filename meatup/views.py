from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Message
from .forms import MessageEntryForm

@login_required(login_url='/login')
def meatup_home(request):
    all_messages = Message.objects.all()  # Menampilkan semua pesan tanpa filter
    context = {
        'all_messages': all_messages,
    }
    return render(request, 'meatup.html', context)

@login_required(login_url='/login')
def create_message_entry(request):
    if request.method == "POST":
        form = MessageEntryForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user  # Menggunakan user yang sedang login sebagai pengirim
            new_message.save()
            return HttpResponseRedirect(reverse('meatup:meatup_home'))
    else:
        form = MessageEntryForm()

    context = {'form': form}
    return render(request, 'create_message_entry.html', context)

@login_required(login_url='/login')
def delete_message(request, id):
    # Hapus pesan tertentu
    message = get_object_or_404(Message, id=id)
    message.delete()
    return HttpResponseRedirect(reverse('meatup:meatup_home'))

@login_required(login_url='/login')
def edit_message(request, id):
    # Edit pesan tertentu
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