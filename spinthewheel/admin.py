from django.contrib import admin
from spinthewheel.models import SpinHistory, SecretHistory

admin.site.register(SpinHistory)
admin.site.register(SecretHistory)