from django.urls import path
from spinthewheel.views import spin_view, history_json, add_spin_history, delete_spin_history, option_json
from spinthewheel.views import secret_view, add_secret_history, delete_secret_history, secret_json
from spinthewheel.views import add_spin_history_mobile

app_name = 'spinthewheel'

urlpatterns = [
    path('', spin_view, name='spin_view'),
    path('history-json/', history_json, name='history_json'),
    path('add-spin-history/', add_spin_history, name='add_spin_history'),
    path('delete/<uuid:id>', delete_spin_history, name='delete_spin_history'),
    path('option-json/<str:selected_category>/', option_json, name='option_json'),
    path('secret/', secret_view, name='secret_view'),
    path('secret-json/', secret_json, name='secret_json'),
    path('add-secret-history/', add_secret_history, name='add_secret_history'),
    path('delete-secret/<uuid:id>', delete_secret_history, name='delete_secret_history'),
    path('add-spin-history-mobile/', add_spin_history_mobile, name='add_spin_history_mobile'),
]

