import uuid
from django.db import models
from django.contrib.auth.models import User
from explore.models import Menu

class ReviewEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    place = models.CharField(max_length=255)
    rating = models.IntegerField()
    description= models.TextField()
    owner_reply = models.TextField(null=True, blank=True)

    @property
    def nama_menu(self):
        return self.menu.menu if self.menu else None