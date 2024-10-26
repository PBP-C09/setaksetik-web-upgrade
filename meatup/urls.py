from django.urls import path
from . import views

app_name = 'meatup'

urlpatterns = [
    path('requests/', views.received_requests, name='received_requests'),
    path('requests/new/<int:wishlist_id>/', views.create_request, name='create_request'),
    path('requests/update/<int:pk>/', views.update_request_status, name='update_request_status'),
    path('requests/delete/<int:pk>/', views.delete_request, name='delete_request'),
    path('main_wishlist/', wishlist_list, name='wishlist_list'),
    path('requests/<int:id>/agree/', agree_request, name='agree_request'),
    path('requests/<int:id>/decline/', decline_request, name='decline_request'),
    path('meatup/', include('meatup.urls', namespace='meatup')),
]