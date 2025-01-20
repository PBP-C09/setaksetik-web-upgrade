from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('explore/', include('explore.urls')),
    path('spinthewheel/', include('spinthewheel.urls')),
    path('review/', include('review.urls')),
    path('meatup/', include('meatup.urls')),
    path('booking/', include('booking.urls')),
    path('claim/', include('claim.urls')),
]
