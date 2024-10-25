import uuid
from django.db import models
from django.contrib.auth.models import User


class ReviewEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    menu = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    rating = models.IntegerField()
    description= models.TextField()
    

    @property
    def is_menu_recommended(self):
        return self.rating > 4