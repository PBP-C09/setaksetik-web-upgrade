from django.db import models
from django.contrib.auth.models import User
from explore.models import Menu
import uuid

class SpinHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.TextField()
    winnerId = models.IntegerField()
    spin_time = models.DateField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note = models.TextField(default="-")

class SecretHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    winner = models.TextField()
    spin_time = models.DateField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
