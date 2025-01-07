from django.urls import path
from . import views

app_name = 'meatup'

urlpatterns = [
    path('', views.meatup_home, name='meatup_home'),
    path('create/', views.create_message_entry, name='create_message_entry'),
    path('edit/<int:id>/', views.edit_message, name='edit_message'),
    path('delete/<int:id>/', views.delete_message, name='delete_message'),
    path('accept/<int:id>/', views.accept_message, name='accept_message'),
    path('reject/<int:id>/', views.reject_message, name='reject_message'),
    path('flutter/', views.meatup_home_flutter, name='meatup_home_flutter'),
    path('create-flutter/', views.create_message_flutter, name='create_message_flutter'),
    path('flutter/edit/<int:id>/', views.edit_message_flutter, name='edit_message_flutter'),
    path('flutter/delete/<int:id>/', views.delete_message_flutter, name='delete_message_flutter'),
    path('flutter/accept/<int:id>/', views.accept_message_flutter, name='accept_message_flutter'),
    path('flutter/reject/<int:id>/', views.reject_message_flutter, name='reject_message_flutter'),
    path('flutter/get-receivers/', views.get_receivers, name='get_receivers'),
]