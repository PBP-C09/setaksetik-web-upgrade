from django.db import models
from django.contrib.auth.models import User

class Wishlist(models.Model):
    owner = models.ForeignKey(User, related_name='meatup_wishlists', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    item_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.item_name

class MeatupRequest(models.Model):
    sender = models.ForeignKey(User, related_name='meatup_sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='meatup_received_requests', on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)  
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Request from {self.sender} to {self.receiver} - {self.status}'