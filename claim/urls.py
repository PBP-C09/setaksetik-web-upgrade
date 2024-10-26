from django.urls import path
from claim.views import available_restaurants, claim_restaurant, owned_restaurant, delete_ownership

app_name = 'claim'

urlpatterns = [
    path('', available_restaurants, name='available_restaurants'),  # Mengganti home page menjadi available_restaurants
    path('claim/<int:restaurant_id>/', claim_restaurant, name='claim_restaurant'),
    path('owned/', owned_restaurant, name='owned_restaurant'),
    path('delete/<int:restaurant_id>/', delete_ownership, name='delete_ownership'),
]
