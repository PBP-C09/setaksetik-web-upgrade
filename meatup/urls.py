from django.urls import path
# from . import views
from meatup.views import show_requests, received_requests, create_request, update_request_status, delete_request

app_name = 'meatup'

urlpatterns = [
    path('', show_requests, name='show_requests'),
    path('requests/', received_requests, name='received_requests'),
    path('requests/new/<int:wishlist_id>/', create_request, name='create_request'),
    path('requests/update/<int:pk>/', update_request_status, name='update_request_status'),
    path('requests/delete/<int:pk>/', delete_request, name='delete_request'),
    # path('main_wishlist/', wishlist_list, name='wishlist_list'),
    # path('requests/<int:id>/agree/', agree_request, name='agree_request'),
    # path('requests/<int:id>/decline/', decline_request, name='decline_request'),
    # path('meatup/', include('meatup.urls', namespace='meatup')),
]