from django.db import models
from django.contrib.auth.models import User
from main.models import UserProfile

class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="received_messages")
    title = models.CharField(max_length=255)
    content = models.TextField()  # Field untuk pesan
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp untuk saat pesan dibuat

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"