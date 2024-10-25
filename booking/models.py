from django.db import models
from django.contrib.auth.models import User
from explore.models import Menu # Import from explore.modelspy
import uuid

# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_items = models.ForeignKey(Menu, on_delete=models.CASCADE) # One to many
    booking_date = models.DateTimeField()
    number_of_people = models.PositiveIntegerField()

def __str__(self):
    return f"Booking oleh {self.user.username} pada tanggal {self.booking_date} sejumlah {self.number_of_people} orang"