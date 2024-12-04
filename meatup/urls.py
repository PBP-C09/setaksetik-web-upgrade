from django.urls import path
from . import views

app_name = 'meatup'

urlpatterns = [
    path('', views.show_requests, name='show_requests'),
    path('requests/', views.received_requests, name='received_requests'),
    path('requests/new/<int:wishlist_id>/', views.create_request, name='create_request'),
    path('requests/list/', views.request_list, name='request_list'),  
    path('requests/update/<int:pk>/', views.update_request_status, name='update_request_status'),
    path('requests/delete/<int:pk>/', views.delete_request, name='delete_request'),
    path('main_wishlist/', views.wishlist_list, name='wishlist_list'),
    path('requests/agree/<int:request_id>/', views.agree_request, name='agree_request'),
    path('requests/decline/<int:request_id>/', views.decline_request, name='decline_request'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),  
]