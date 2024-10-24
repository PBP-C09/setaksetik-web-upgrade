from django.urls import path
from booking.views import main_booking_page, create_booking, lihat_booking, booking_form, delete_booking, edit_booking

app_name = 'booking'

urlpatterns = [
    path('', main_booking_page, name='main_booking_page'),
    path('create/', create_booking, name='create_booking'),
    path('lihat/', lihat_booking, name='lihat_booking'),
    path('form/<int:menu_id>/', booking_form, name='booking_form'),
    path('edit/<int:booking_id>/', edit_booking, name='edit_booking'),
    path('delete/<int:booking_id>/', delete_booking, name='delete_booking'),
]