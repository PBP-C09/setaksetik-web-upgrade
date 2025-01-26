from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from review.forms import ReviewEntryForm
from review.models import ReviewEntry
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from explore.models import Menu
import json
from django.http import JsonResponse

@csrf_exempt
@login_required(login_url='/login')
def show_review(request, menu_id=None):    
    # Default context
    context = {
        'nama': 'steak',
        'lokasi': 'jaksel',
        'rating': '5',
    }
    # Filter reviews based on menu_id if provided
    if menu_id != None:
        menus = Menu.objects.all()
        menu = Menu.objects.get(id=menu_id)
        reviews = ReviewEntry.objects.filter(menu=menu)
        context['reviews'] = reviews
        context['menu'] = menu  # Optional: Detail menu untuk judul
        context['menus'] = menus
        # menus = Menu.objects.all()
    else:
        reviews = ReviewEntry.objects.all()
        context['reviews'] = reviews

    context['menu_id'] = menu_id

    # Role-based rendering
    if request.user.userprofile.role == "admin":
        return render(request, 'review_admin.html', context)
    elif request.user.userprofile.role == "steakhouse owner":
        return render(request, 'review_owner.html', context)
    else:
        return render(request, 'review.html', context)



@csrf_exempt
@login_required(login_url='/login')
def show_review_menu(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    reviews = ReviewEntry.objects.filter(menu = menu_id)

    context = {
        'menu' : menu,
        'reviews' : reviews,
    }

    if request.user.userprofile.role == "admin":
        return render(request, 'review_admin.html', context)

    if request.user.userprofile.role == "steakhouse owner":
        return render(request, 'review_owner.html', context)
    return render(request, 'review_menu.html', context)

def show_review_owner(request):
    user = request.user
    
    # Filter menu berdasarkan user
    restaurant_menus = Menu.objects.filter(claimed_by=user)

    # Context untuk menyimpan menu dan review
    context = {
        'restaurant_menus': restaurant_menus,
        'reviews': []
    }
    
    # Ambil review hanya jika ada menu yang diklaim
    if restaurant_menus.exists():
        all_reviews = []
        
        # Iterasi setiap menu untuk mengambil review
        for menu in restaurant_menus:
            reviews_for_menu = ReviewEntry.objects.filter(menu=menu)
            all_reviews.extend(reviews_for_menu)  # Menambahkan review ke list keseluruhan

        # Masukkan semua review ke dalam konteks
        context['reviews'] = all_reviews

    return render(request, 'review_owner.html', context)

@login_required(login_url='/login')
def get_review_from_owner(request): 
    user = request.user
    restaurant_menus = Menu.objects.filter(claimed_by=user)

    all_reviews = []
    for menu in restaurant_menus:
        reviews_for_menu = ReviewEntry.objects.filter(menu=menu)
        all_reviews.extend(reviews_for_menu)

    # Mengubah data sesuai kebutuhan
    final_reviews = []
    for review in all_reviews:
        review_data = {
            "id": str(review.id),
            "menu_name": review.menu.menu if review.menu else None,
            "place": review.place,
            "rating": review.rating,
            "description": review.description,
            "owner_reply": review.owner_reply or 'No reply yet',
            "user_id": review.user.id,
            "username": review.user.username,
        }
        final_reviews.append(review_data)

    return JsonResponse({
        'reviews': final_reviews,
    })

def show_review_flutter(request):
    data = ReviewEntry.objects.all()
    serialized_data = []
    
    for review in data:
        serialized_data.append({
            "model": "review",  # Menambahkan properti ini ke objek review
            "pk": str(review.pk),  # Primary key
            "fields": {
                "name": review.menu.menu,  # Menggunakan properti terkait menu
                "user": review.user.id,  # ID pengguna yang mengisi review
                "menu": review.menu.id,  # ID menu yang direview
                "place": review.place,
                "rating": review.rating,
                "description": review.description,
                "owner_reply": review.owner_reply or 'No reply yet',  # Mengatur nilai default jika null
            }
        })

    return HttpResponse(json.dumps(serialized_data), content_type="application/json")

def show_review_owner_flutter(request):
    user = request.user
    restaurant_menus = Menu.objects.filter(claimed_by=user)
    if not restaurant_menus:
        return JsonResponse({
            'status' : 'failed',
            'message' : 'Tidak ada menu yang sesuai'
        })
    
    # Debugging untuk memastikan menu yang ditemukan

    all_reviews = []
    
    # Iterasi setiap menu untuk mengambil review
    for menu in restaurant_menus:
        reviews_for_menu = ReviewEntry.objects.filter(menu=menu)
        all_reviews.extend(reviews_for_menu)  # Menambahkan review ke list keseluruhan

    final_reviews = []
    for review in all_reviews:
        review_data = {
            "model": "review",  # Misalnya properti ini ada pada objek review
            "pk": review.pk,  # Misalnya properti ini ada
            "fields": {
                "name" : review.menu.menu,
                "user": review.user.id,
                "menu": review.menu.id,
                "place": review.place,
                "rating": review.rating,
                "description": review.description,
                "owner_reply": review.owner_reply or 'No reply yet',  # Atur nilai default jika null
            }
        }
        final_reviews.append(review_data)

    # Masukkan semua review ke dalam konteks
    # context['reviews'] = all_reviews


    return JsonResponse({
        # 'status' : 'success',
        'reviews': final_reviews,
    })

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
    if (id != None):
        menu = Menu.objects.get(id=id)
        data = ReviewEntry.objects.filter(menu=menu)
    else:
        data = ReviewEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
@csrf_exempt
@require_POST
def add_review_entry_ajax(request):
    # name = strip_tags(request.POST.get("name"))
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
        menu=themenu, place=place,
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
    # Set review entry as an instance of the form
    form = ReviewEntryForm(request.POST or None, instance=review)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('review:show_review'))

    context = {'form': form}
    return render(request, "edit_review.html", context)

    
def get_review_entries(self, request, menu_id=None):
    if menu_id:
        reviews = ReviewEntry.objects.filter(menu__id=menu_id)
    else:
        reviews = ReviewEntry.objects.all()
    
    review_data = []
    for review in reviews:
        review_data.append({
            'id': str(review.id),
            'user': review.user.username,  # Mengambil nama pengguna
            'menu_name': review.menu.menu if review.menu else None,  # Mengambil nama menu
            'place': review.place,
            'rating': review.rating,
            'description': review.description,
            'owner_reply': review.owner_reply
        })
    
    return JsonResponse(review_data, safe=False)

@csrf_exempt
@login_required(login_url='/login')
def delete_review(request, id):
    # Get review berdasarkan id
    review = ReviewEntry.objects.get(pk=id)
    # Manage perubahan rating menu
    themenu = Menu.objects.get(menu=review.menu.menu)
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
            # Parse JSON body
            data = json.loads(request.body)
            
            # Extract fields from the request body
            user_id = request.user
            menu_id = data.get('menu')
            place = data.get('place')
            rating = data.get('rating')
            description = data.get('description')
            owner_reply = data.get('owner_reply')
            # Validate required fields
            if not all([user_id, menu_id, place, rating, description]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            # Get related User and Menu objects
            try:
                user = request.user
                menu = Menu.objects.get(id=menu_id)
            except user.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
            except Menu.DoesNotExist:
                return JsonResponse({'error': 'Menu not found'}, status=404)

            # Create a new ReviewEntry object
            review = ReviewEntry.objects.create(
                user=user,
                menu=menu,
                place=place,
                rating=rating,
                description=description,
                owner_reply=owner_reply
            )

            # Return success response
            return JsonResponse({
                'message': 'Review created successfully',
                'review': {
                    'id': str(review.id),
                    'user': review.user.id,
                    'menu': review.menu.id,
                    'place': review.place,
                    'rating': review.rating,
                    'description': review.description,
                    'owner_reply': review.owner_reply,
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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

# @login_required(login_url='/login')
# def delete_review(request, id):
#     # Get review berdasarkan id
#     review = ReviewEntry.objects.get(pk=id)
#     # Manage perubahan rating menu
#     themenu = Menu.objects.get(menu=review.menu.menu)
#     themenu.total_rating -= review.rating
#     themenu.review_count -= 1
#     themenu.rating = themenu.total_rating / (themenu.review_count + 1)
#     themenu.save()

#     review.delete()

#     return HttpResponseRedirect(reverse('review:show_review'))

@csrf_exempt
@require_POST
@login_required(login_url='/login')
@csrf_exempt
@login_required(login_url='/login')
def delete_review_flutter(request):
    if request.method == 'POST':
        try:
            # Decode and parse JSON
            data = json.loads(request.body.decode('utf-8'))
            review_id = data.get('review_id')

            # Validasi input
            if not review_id:
                return JsonResponse({'status': 'error', 'message': 'Review ID is required'}, status=400)

            # Cari review berdasarkan ID
            review = ReviewEntry.objects.get(pk=review_id)

            # Manage rating pada menu 
            themenu = Menu.objects.get(menu=review.menu.menu)
            themenu.total_rating -= review.rating
            themenu.review_count -= 1

            # Pastikan tidak ada pembagian dengan nol
            if themenu.review_count > 0:
                themenu.rating = themenu.total_rating / themenu.review_count
            else:
                themenu.rating = 0  # Atur rating ke 0 jika tidak ada review yang tersisa

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
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

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
