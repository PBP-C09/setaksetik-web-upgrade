from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    menu = models.TextField()
    category = models.CharField(max_length=255)
    restaurant_name = models.CharField(max_length=255)
    image = models.TextField()
    city = models.CharField(max_length=255)
    price = models.IntegerField()
    rating = models.FloatField()
    specialized = models.CharField(max_length=255)
    takeaway = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    outdoor = models.BooleanField(default=False)
    smoking_area = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.menu} at {self.restaurant_name} - {self.city}"

    @property
    def is_expensive(self):
        return self.price > 1000000

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        ordering = ['restaurant_name', 'category', '-rating']

class Wishlist(models.Model):
    owner = models.ForeignKey(User, related_name='main_wishlist', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.item_name

class MeatupRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    sender = models.ForeignKey(User, related_name='main_sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='main_received_requests', on_delete=models.CASCADE)
    wishlist_item = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} requests to meet {self.receiver} for {self.wishlist_item}"