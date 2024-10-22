from django import forms
from .models import Menu

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

class MenuFilterForm(forms.Form):
    menu = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'menu'}))
    category = forms.ChoiceField(choices=[('', 'Select category')] + CATEGORY_CHOICES, required=False)
    price = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'price'}))
    restaurant= forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'restaurant name'}))
    city = forms.ChoiceField(choices=[('', 'Select city')] + CITY_CHOICES, required=False)
    specialize = forms.ChoiceField(choices=[('', 'Select specialized')] + SPECIALIZED_CHOICES, required=False)
    rating = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'rating'}))

class AddMenuForm(forms.Form):
   class Meta:
       model = Menu
       fields = ['menu', 'category', 'restaurant_name', 'image', 'city', 'price', 'rating', 'specialized', 'takeaway', 'delivery', 'outdoor', 'smoking_area', 'wifi']