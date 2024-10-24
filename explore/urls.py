from django.urls import path
from explore.views import get_menu, show_menu, menu_detail, add_menu, get_menu_by_id, filter_menu
from booking.views import booking_form

app_name = "explore"

urlpatterns = [
    path("", show_menu, name='show_menu'),
    path("detail/", menu_detail, name='menu_detail'),

    path('menu_detail/<int:menu_id>/', menu_detail, name='menu_detail'),
    path('add_menu/<int:menu_id>/<int:user_id>/', add_menu, name='add_menu'),
    path('get_menu/', get_menu, name='get_menu'),
    path('get_menu/<int:id>/', get_menu_by_id, name="get_menu_by_id"),
   # path('add_menu/', add_menu, name='add_menu'),
    path('form/<int:menu_id>/', booking_form, name='booking_form'),
    path('filter_menu/', filter_menu, name='filter_menu'),
]