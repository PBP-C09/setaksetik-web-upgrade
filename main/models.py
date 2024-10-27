from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLES = [
        ('steak lover', 'Steak Lover'),
        ('steakhouse owner', 'Steakhouse Owner'),
        ('admin', 'Admin')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES)