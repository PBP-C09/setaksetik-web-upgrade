from django.urls import path
from . import views

app_name = 'meatup'

urlpatterns = [
    path('', views.meatup_home, name='meatup_home'),
    path('create/', views.create_message_entry, name='create_message_entry'),
    path('edit/<int:id>/', views.edit_message, name='edit_message'),
    path('delete/<int:id>/', views.delete_message, name='delete_message'),
]
