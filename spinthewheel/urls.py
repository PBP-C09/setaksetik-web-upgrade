from django.urls import path, re_path
from spinthewheel.views import menu_view, history_json, add_spin_history, delete_spin_history, option_json

app_name = 'spinthewheel'

urlpatterns = [
    path('', menu_view, name='menu_view'),
    path('history-json/', history_json, name='history_json'),
    path('add-spin-history/', add_spin_history, name='add_spin_history'),
    path('delete/<uuid:id>', delete_spin_history, name='delete_spin_history'),
    path('option-json/<str:selected_category>/', option_json, name='option_json'),
]

