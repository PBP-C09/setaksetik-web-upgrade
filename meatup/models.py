from django.db import models 
from django.contrib.auth.models import User 
from main.models import UserProfile 
 
class Message(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected')
    ]
    
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sent_messages") 
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="received_messages") 
    title = models.CharField(max_length=255) 
    content = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
 
    def __str__(self): 
        return f"Message from {self.sender.user.username} at {self.timestamp}"