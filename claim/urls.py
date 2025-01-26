from django.urls import path
from claim.views import claim_restaurant, owned_restaurant, delete_ownership, manage_ownership
from claim.views import get_claimable_json, add_menu, claim_resto_flutter, get_owned_restaurant_flutter, delete_ownership_flutter, manage_ownership_flutter, revoke_ownership_flutter, add_menu_flutter, edit_flutter

app_name = 'claim'

urlpatterns = [
    path('', owned_restaurant, name='owned_restaurant'),  
    path('claim/<int:restaurant_id>/', claim_restaurant, name='claim_restaurant'),
    path('owned/', owned_restaurant, name='owned_restaurant'),
    path('delete/<int:restaurant_id>/', delete_ownership, name='delete_ownership'),
    path('manage/', manage_ownership, name='manage_ownership'),
    path('json/', get_claimable_json, name='get_claimable_json'),
    path('claim_flutter/<int:restaurant_id>/', claim_resto_flutter, name='claim_resto_flutter'),
    path('owned_flutter/', get_owned_restaurant_flutter, name='get_owned_restaurant_flutter'),
    path('delete_flutter/<int:restaurant_id>/', delete_ownership_flutter, name='delete_ownership_flutter'),
    path('manage_flutter/', manage_ownership_flutter, name='manage_ownership_flutter'),
    path('revoke_flutter/', revoke_ownership_flutter, name='revoke_ownership_flutter'),
    path('add_menu/', add_menu, name='add_menu'),
    path('add-menu-flutter/', add_menu_flutter, name='add_menu_flutter'),
    path('edit-flutter/<int:menu_id>/', edit_flutter, name='edit_flutter'),
]
