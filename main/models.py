from django.db import models

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