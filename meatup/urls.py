from django.urls import path
from . import views

app_name = 'meatup'

urlpatterns = [
    path('', views.show_main, name='show_main'),
    path('messages/', views.show_message_list, name='show_message_list'),
    path('messages/create/', views.create_meatup_message, name='create_message'),
    path('messages/edit/<int:id>/', views.edit_message, name='edit_message'),
    path('messages/delete/<int:id>/', views.delete_message, name='delete_message'),
    path('messages/detail/<int:id>/', views.show_message_detail, name='show_message_detail'),
    path('card_info/', views.card_info, name='card_info'),
    path('card_message/', views.card_message, name='card_message'),
]
