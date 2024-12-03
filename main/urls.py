from django.urls import path
from main.views import show_main, register, login_user, logout_user, forbidden
from main.views import register_mobile, login_mobile, logout_mobile

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('register-admin/', register, name='register-admin'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('forbidden/', forbidden, name='forbidden'),
    path('register-mobile/', register_mobile, name='register-mobile'),
    path('login-mobile/', login_mobile, name='login-mobile'),
    path('logout-mobile/', logout_mobile, name='logout-mobile'),
]