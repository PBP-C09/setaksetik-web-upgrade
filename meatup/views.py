from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MeatupMessage

# Halaman utama yang menampilkan semua pesan
@login_required(login_url='/login')
def show_main(request):
    messages = MeatupMessage.objects.all()
    return render(request, 'meatup/show_main.html', {'messages': messages})

# Menampilkan daftar pesan
@login_required
def show_message_list(request):
    messages = MeatupMessage.objects.filter(receiver=request.user)
    return render(request, 'meatup/show_message_list.html', {'messages': messages})

# Membuat pesan baru
@login_required
def create_meatup_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        MeatupMessage.objects.create(sender=request.user, content=content)
        return redirect('meatup:show_main')
    return render(request, 'meatup/create_message.html')

# Mengedit pesan
@login_required
def edit_message(request, id):
    message = get_object_or_404(MeatupMessage, id=id)
    if message.sender != request.user:
        return redirect('meatup:show_main')
    if request.method == 'POST':
        message.content = request.POST.get('content')
        message.save()
        return redirect('meatup:show_main')
    return render(request, 'meatup/edit_message.html', {'message': message})

# Menghapus pesan
@login_required
def delete_message(request, id):
    message = get_object_or_404(MeatupMessage, id=id)
    if message.sender != request.user:
        return redirect('meatup:show_main')
    if request.method == 'POST':
        message.delete()
        return redirect('meatup:show_main')
    return render(request, 'meatup/delete_message.html', {'message': message})

# Menampilkan detail pesan
@login_required
def show_message_detail(request, id):
    message = get_object_or_404(MeatupMessage, id=id)
    return render(request, 'meatup/show_message_detail.html', {'message': message})

# Menampilkan kartu informasi
@login_required
def card_info(request):
    return render(request, 'meatup/card_info.html')

# Menampilkan kartu pesan
@login_required
def card_message(request):
    messages = MeatupMessage.objects.all()
    return render(request, 'meatup/card_message.html', {'messages': messages})