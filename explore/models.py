from django.db import models

# Create your models here.

CATEGORY_CHOICES = [
    ('beef', 'Beef'),
    ('chicken', 'Chicken'),
    ('fish', 'Fish'),
    ('lamb', 'Lamb'),
    ('other', 'Other'),
    ('pork', 'Pork'),
    ('rib_eye', 'Rib Eye'),
    ('sirloin', 'Sirloin'),
    ('t_bone', 'T-Bone'),
    ('tenderloin', 'Tenderloin'),
    ('wagyu', 'Wagyu'),
]

CITY_CHOICES = [
    ('central_jakarta', 'Central Jakarta'),
    ('east_jakarta', 'East Jakarta'),
    ('north_jakarta', 'North Jakarta'),
    ('south_jakarta', 'South Jakarta'),
    ('west_jakarta', 'West Jakarta'),
]

SPECIALIZED_CHOICES = [
    ('argentinian', 'Argentinian'),
    ('brazilian', 'Brazilian'),
    ('breakfast_cafe', 'Breakfast Cafe'),
    ('british', 'British'),
    ('french', 'French'),
    ('fushioned', 'Fushioned'),
    ('italian', 'Italian'),
    ('japanese', 'Japanese'),
    ('local', 'Local'),
    ('local_westerned', 'Local Westerned'),
    ('mexican', 'Mexican'),
    ('western', 'Western'),
    ('singaporean', 'Singaporean'),
]

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.TextField(null = True, blank = True)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        null=True,
        blank=True
    )
    restaurant_name = models.TextField(null = True, blank = True)
    image = models.URLField(null = True, blank = True)
    city = models.CharField(
        max_length=50,
        choices=CITY_CHOICES,
        null=True,
        blank=True
    )

    price = models.IntegerField(null = True, blank = True)
    rating = models.FloatField(null = True, blank = True)
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
