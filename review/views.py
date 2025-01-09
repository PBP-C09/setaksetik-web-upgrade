from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from review.forms import ReviewEntryForm
from review.models import ReviewEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from django.contrib import messages
from explore.models import Menu
from explore.forms import MenuFilterForm
from main.models import UserProfile
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


# batasan
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

@csrf_exempt
@login_required(login_url='/login')
def show_review(request):

    context = {
        'nama' : 'steak',
        'lokasi' : 'jaksel',
        'rating' : '5',
        # 'is_admin': request.is_admin,
    }

    if request.user.userprofile.role == "admin":
        return render(request, 'review_admin.html', context)



    if request.user.userprofile.role == "steakhouse owner":
        return render(request, 'review_owner.html', context)
    return render(request, 'review.html', context)

@csrf_exempt
@login_required(login_url='/login')
def show_xml(request):
    data = ReviewEntry.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@csrf_exempt
@login_required(login_url='/login')
def show_json(request):
    data = ReviewEntry.objects.filter(user=request.user)
    data = ReviewEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
def get_review(request):
    data = ReviewEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@login_required(login_url='/login')
def show_xml_by_id(request, id):
    data = ReviewEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@csrf_exempt
@login_required(login_url='/login')
def show_json_by_id(request, id):
    data = ReviewEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
@csrf_exempt
@require_POST
def add_review_entry_ajax(request):
    menu = strip_tags(request.POST.get("menu"))
    place = strip_tags(request.POST.get("place"))
    rating = float(strip_tags(request.POST.get("rating")))
    description = request.POST.get("description")
    user = request.user

    # Manage perubahan rating menu
    themenu = Menu.objects.get(menu=menu)
    if (themenu.total_rating == 0):
        themenu.total_rating += themenu.rating

    themenu.total_rating += rating
    themenu.review_count += 1
    themenu.rating = themenu.total_rating / (themenu.review_count + 1)
    themenu.save()

    new_review = ReviewEntry(
        menu=menu, place=place,
        rating=rating,
        user=user, description=description
    )
    new_review.save()

    return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@login_required(login_url='/login')
def create_review_entry(request):
    # Retrieve all menu entries without filtering
    menus = Menu.objects.all()
    
    # Context data for rendering the template
    context = {
        'menus': menus,  # Pass the query result
    }

    return render(request, 'create_review_entry.html', context)

@csrf_exempt
@login_required(login_url='/login')
def edit_review(request, id):
    # Get the review entry based on id
    review = ReviewEntry.objects.get(pk=id)
    # user_profile = UserProfile.objects.get(user=request.user)

    # Allow only admins to edit
    # if user_profile.role != "admin":
    #     messages.error(request, "You do not have permission to edit this review.")
    #     return redirect('review:show_review')

    # Set review entry as an instance of the form
    form = ReviewEntryForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('review:show_review'))

    context = {'form': form}
    return render(request, "edit_review.html", context)

@csrf_exempt
@login_required(login_url='/login')
def delete_review(request, id):
    # Get review berdasarkan id
    review = ReviewEntry.objects.get(pk=id)

    # Manage perubahan rating menu
    themenu = Menu.objects.get(menu=review.menu)
    themenu.total_rating -= review.rating
    themenu.review_count -= 1
    themenu.rating = themenu.total_rating / (themenu.review_count + 1)
    themenu.save()

    review.delete()

    return HttpResponseRedirect(reverse('review:show_review'))



@csrf_exempt
@require_POST
@login_required(login_url='/login')
def submit_reply(request):
    if request.user.userprofile.role != "steakhouse owner":
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        review_id = data.get('review_id')
        reply_text = data.get('reply_text')
        
        # Verifikasi bahwa review ini milik steakhouse owner yang bersangkutan
        review = ReviewEntry.objects.get(pk=review_id)
        # Uncomment jika sudah ada relasi ke steakhouse
        # if review.steakhouse != request.user.steakhouse:
        #     return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
        review.owner_reply = reply_text
        review.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Reply submitted successfully'
        })
    except ReviewEntry.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Review not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def update_reply(request):
    if request.user.userprofile.role != "steakhouse owner":
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        review_id = data.get('review_id')
        reply_text = data.get('reply_text')
        
        review = ReviewEntry.objects.get(pk=review_id)
        # Verifikasi ownership
        # if review.steakhouse != request.user.steakhouse:
        #     return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
        
        review.owner_reply = reply_text
        review.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Reply updated successfully'
        })
    except ReviewEntry.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Review not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@csrf_exempt
@require_POST
def create_review_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_review = ReviewEntry.objects.create(
                user = request.user,
                menu=data["menu"],
                place=data["place"],
                rating=float(data["rating"]),
                description=data["description"],
                owner_reply=data["owner_reply"],
            )

            # Manage perubahan rating menu
            themenu = Menu.objects.get(menu=data["menu"])
            if (themenu.total_rating == 0):
                themenu.total_rating += themenu.rating

            themenu.total_rating += float(data["rating"])
            themenu.review_count += 1
            themenu.rating = themenu.total_rating / (themenu.review_count + 1)
            themenu.save()
            new_review.save()
            return JsonResponse({"status": "success"}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def submit_reply_flutter(request):
    # Pastikan hanya steakhouse owner yang bisa mengakses
    if request.user.userprofile.role != "steakhouse owner":
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    try:
        # Parse data dari request body
        data = json.loads(request.body)
        review_id = data.get('review_id')
        reply_text = data.get('reply_text')

        # Validasi data
        if not review_id or not reply_text:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

        # Cari review berdasarkan ID
        review = ReviewEntry.objects.get(pk=review_id)

        # Optional: Verifikasi bahwa review ini terkait dengan steakhouse owner (jika ada relasi)
        # if review.steakhouse != request.user.steakhouse:
        #     return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

        # Perbarui kolom owner_reply
        review.owner_reply = reply_text
        review.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Reply submitted successfully'
        }, status=200)

    except ReviewEntry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Review not found'}, status=404)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def delete_review_flutter(request):
    try:
        # Parse request body
        data = json.loads(request.body)
        review_id = data.get('review_id')

        # Validasi input
        if not review_id:
            return JsonResponse({'status': 'error', 'message': 'Review ID is required'}, status=400)

        # Cari review berdasarkan ID
        review = ReviewEntry.objects.get(pk=review_id)

        # Manage rating pada menu 
        themenu = Menu.objects.get(menu=review.menu)
        themenu.total_rating -= review.rating
        themenu.review_count -= 1
        themenu.rating = themenu.total_rating / (themenu.review_count + 1)
        themenu.save()

        # Optional: Validasi role atau kepemilikan
        if request.user.userprofile.role != "admin":
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

        # Hapus review
        review.delete()
        return JsonResponse({'status': 'success', 'message': 'Review deleted successfully'}, status=200)

    except ReviewEntry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Review not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_POST
@login_required(login_url='/login')
def update_reply_flutter(request):
    # Pastikan hanya steakhouse owner yang bisa mengakses
    if request.user.userprofile.role != "steakhouse owner":
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

    try:
        # Parse data dari request body
        data = json.loads(request.body)
        review_id = data.get('review_id')
        reply_text = data.get('reply_text')

        # Validasi input
        if not review_id or not reply_text:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

        # Cari review berdasarkan ID
        review = ReviewEntry.objects.get(pk=review_id)

        # Optional: Verifikasi bahwa review ini terkait dengan steakhouse owner (jika ada relasi)
        # if review.steakhouse != request.user.steakhouse:
        #     return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)

        # Perbarui kolom owner_reply
        review.owner_reply = reply_text
        review.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Reply updated successfully'
        }, status=200)

    except ReviewEntry.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Review not found'}, status=404)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
