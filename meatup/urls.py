from django.urls import path, include
from . import views
from meatup.views import (
    show_requests, received_requests, create_request, update_request_status, delete_request,
    wishlist_list, agree_request, decline_request, add_to_wishlist 
)

app_name = 'meatup'

urlpatterns = [
    path('', show_requests, name='show_requests'),
    path('requests/', views.received_requests, name='received_requests'),
    path('requests/new/<int:wishlist_id>/', views.create_request, name='create_request'),
    path('requests/update/<int:pk>/', update_request_status, name='update_request_status'),
    path('requests/delete/<int:pk>/', delete_request, name='delete_request'),
    path('main_wishlist/', wishlist_list, name='wishlist_list'),
    path('requests/agree/<int:request_id>/', views.agree_request, name='agree_request'),
    path('requests/decline/<int:request_id>/', views.decline_request, name='decline_request'),
    path('add_to_wishlist/', add_to_wishlist, name='add_to_wishlist'),  
]