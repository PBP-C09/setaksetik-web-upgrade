from django.urls import path
from explore.views import get_menu, show_menu, menu_detail, add_menu, get_menu_by_id, filter_menu, admin_detail, owner_detail
from booking.views import booking_form, lihat_booking
from review.views import show_review

app_name = "explore"

urlpatterns = [
    path("", show_menu, name='show_menu'),
    path("detail/", menu_detail, name='menu_detail'),
    path('menu_detail/<int:menu_id>/', menu_detail, name='menu_detail'),
    path('admin_detail/<int:menu_id>/', admin_detail, name='admin_detail'),
    path('owner_detail/<int:menu_id>/', owner_detail, name='owner_detail'),
    path('add_menu/<int:menu_id>/<int:user_id>/', add_menu, name='add_menu'),
    path('get_menu/', get_menu, name='get_menu'),
    path('get_menu/<int:id>/', get_menu_by_id, name="get_menu_by_id"),
    path('add_menu/', add_menu, name='add_menu'),
    path('form/<int:menu_id>/', booking_form, name='booking_form'),
    path('filter_menu/', filter_menu, name='filter_menu'),
    path('', show_review, name='show_review'),
    path('lihat/', lihat_booking, name='lihat_booking'),
]