from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()  # Field untuk pesan
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp untuk saat pesan dibuat

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"