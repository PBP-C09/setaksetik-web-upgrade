from django.db import models
from django.contrib.auth.models import User # Import user untuk keperluan claim resto

# Create your models here.

CATEGORY_CHOICES = [
    ('Beef', 'Beef'),
    ('Chicken', 'Chicken'),
    ('Fish', 'Fish'),
    ('Lamb', 'Lamb'),
    ('Pork', 'Pork'),
    ('Rib Eye', 'Rib Eye'),
    ('Sirloin', 'Sirloin'),
    ('T-bone', 'T-Bone'),
    ('Tenderloin', 'Tenderloin'),
    ('Wagyu', 'Wagyu'),
    ('Other', 'Other'),
]

CITY_CHOICES = [
    ('Central Jakarta', 'Central Jakarta'),
    ('East Jakarta', 'East Jakarta'),
    ('North Jakarta', 'North Jakarta'),
    ('South Jakarta', 'South Jakarta'),
    ('West Jakarta', 'West Jakarta'),
]

SPECIALIZED_CHOICES = [
    ('Argentinian', 'Argentinian'),
    ('Brazilian', 'Brazilian'),
    ('Breakfast Cafe', 'Breakfast Cafe'),
    ('British', 'British'),
    ('French', 'French'),
    ('Fushioned', 'Fushioned'),
    ('Italian', 'Italian'),
    ('Japanese', 'Japanese'),
    ('Local', 'Local'),
    ('Local Westerned', 'Local Westerned'),
    ('Mexican', 'Mexican'),
    ('Western', 'Western'),
    ('Singaporean', 'Singaporean'),
]

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.CharField(max_length=50, null = True, blank = True)
    restaurant_name = models.CharField(max_length=50, null = True, blank = True)
    price = models.IntegerField(null = True, blank = True)
    rating = models.FloatField(null = True, blank = True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=50,
        choices=CITY_CHOICES,
        null=True,
        blank=True
    )
    specialized = models.CharField(
        max_length=50,
        choices=SPECIALIZED_CHOICES,
        null=True,
        blank=True
    )
    takeaway = models.BooleanField(null = True, blank = True)
    delivery = models.BooleanField(null = True, blank = True)
    outdoor = models.BooleanField(null = True, blank = True)
    smoking_area = models.BooleanField(null = True, blank = True)
    wifi = models.BooleanField(null = True, blank = True)
    claimed_by = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL) # Nambah atribut models.py claimed_by (bismillah)
    image = models.URLField(null = True, blank = True)
