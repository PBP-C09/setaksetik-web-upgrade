from django.urls import path
from explore.views import get_menu, show_menu, menu_detail, add_menu, get_menu_by_id, add_to_cart, filter_menu

app_name = "explore"

urlpatterns = [
    path("", show_menu, name='show_menu'),
    path('menu_detail/<int:menu_id>/', menu_detail, name='menu_detail'),
    path('add_menu/<int:menu_id>/<int:user_id>/', add_menu, name='add_menu'),
    path('get_menu/', get_menu, name='get_menu'),
    path('get_menu/<int:id>/', get_menu_by_id, name="get_menu_by_id"),
   # path('add_menu/', add_menu, name='add_menu'),
    path('add_to_cart/<int:menu_id>/<int:user_id>/', add_to_cart, name='add_to_cart'),
    path('filter_menu/', filter_menu, name='filter_menu'),
]