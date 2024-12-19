from django.urls import path
from explore.views import get_menu, show_menu, menu_detail, add_menu, get_menu_by_id, filter_menu, admin_detail, owner_detail, edit_menu, delete_menu, show_xml, show_json, show_xml_by_id, show_json_by_id, add_menu_flutter
from booking.views import booking_form, lihat_booking
from review.views import show_review
from claim.views import claim_restaurant

app_name = "explore"

urlpatterns = [
    path("", show_menu, name='show_menu'),
    path('menu_detail/<int:menu_id>/', menu_detail, name='menu_detail'),
    path('admin_detail/<int:menu_id>/', admin_detail, name='admin_detail'),
    path('owner_detail/<int:menu_id>/', owner_detail, name='owner_detail'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
    path('get_menu/', get_menu, name='get_menu'),
    path('get_menu/<int:id>/', get_menu_by_id, name="get_menu_by_id"),
    path('add_menu/', add_menu, name='add_menu'),
    path('form/<int:menu_id>/', booking_form, name='booking_form'),
    path('filter_menu/', filter_menu, name='filter_menu'),
    path('', show_review, name='show_review'),
    path('lihat/', lihat_booking, name='lihat_booking'),
    path('edit-menu/<int:menu_id>/', edit_menu, name='edit_menu'),
    path('delete/<int:menu_id>', delete_menu, name='delete_menu'),
    path('claim_restaurant/<int:restaurant_id>/', claim_restaurant, name='claim_restaurant'),
    path('add_menu-flutter/', add_menu_flutter, name='add_menu_flutter'),
]