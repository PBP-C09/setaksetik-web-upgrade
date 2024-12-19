from django.urls import path
from booking.views import create_booking, lihat_booking, booking_form, delete_booking, edit_booking, pantau_booking_owner, approve_booking
from booking.views import show_booking_xml, show_booking_json, show_booking_xml_by_id, show_booking_json_by_id
from booking.views import get_bookings_json, delete_booking_flutter, add_booking_flutter, edit_booking_flutter


app_name = 'booking'

urlpatterns = [
    path('', create_booking, name='create_booking'),
    path('create/', create_booking, name='create_booking'),
    path('lihat/', lihat_booking, name='lihat_booking'),
    path('form/<int:menu_id>/', booking_form, name='booking_form'),
    path('edit/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('delete/<int:booking_id>/', delete_booking, name='delete_booking'),
    path('pantau/', pantau_booking_owner, name='pantau_booking_owner'),
    path('approve/<int:booking_id>/', approve_booking, name='approve_booking'),
    path('booking/xml/', show_booking_xml, name='show_booking_xml'),
    path('booking/json/', show_booking_json, name='show_booking_json'),
    path('booking/xml/<int:booking_id>/', show_booking_xml_by_id, name='show_booking_xml_by_id'),
    path('booking/json/<int:booking_id>/', show_booking_json_by_id, name='show_booking_json_by_id'),
    path('json/all/', get_bookings_json, name='get_bookings_json'),
    path('delete_flutter/<int:booking_id>/', delete_booking_flutter, name='delete_booking_flutter'),
    path('add_flutter/<int:menu_id>/', add_booking_flutter, name='add_booking_flutter'),
    path('edit_flutter/<int:booking_id>/', edit_booking_flutter, name='edit_booking_flutter'),
]