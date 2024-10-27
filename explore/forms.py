from django import forms
from .models import Menu
from django.utils.html import strip_tags

CATEGORY_CHOICES = [
    ('beef', 'Beef'),
    ('chicken', 'Chicken'),
    ('fish', 'Fish'),
    ('lamb', 'Lamb'),
    ('other', 'Other'),
    ('pork', 'Pork'),
    ('rib eye', 'Rib Eye'),
    ('sirloin', 'Sirloin'),
    ('t-bone', 'T-Bone'),
    ('tenderloin', 'Tenderloin'),
    ('wagyu', 'Wagyu'),
]

CITY_CHOICES = [
    ('Central Jakarta', 'Central Jakarta'),
    ('East Jakarta', 'East Jakarta'),
    ('North Jakarta', 'North Jakarta'),
    ('South Jakarta', 'South Jakarta'),
    ('West Jakarta', 'West Jakarta'),
]

SPECIALIZED_CHOICES = [
    ('argentinian', 'Argentinian'),
    ('brazilian', 'Brazilian'),
    ('breakfast cafe', 'Breakfast Cafe'),
    ('british', 'British'),
    ('french', 'French'),
    ('fushioned', 'Fushioned'),
    ('italian', 'Italian'),
    ('japanese', 'Japanese'),
    ('local', 'Local'),
    ('local westerned', 'Local Westerned'),
    ('mexican', 'Mexican'),
    ('western', 'Western'),
    ('singaporean', 'Singaporean'),
]

class MenuFilterForm(forms.Form):
    menu = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'menu'}))
    category = forms.ChoiceField(choices=[('', 'Select category')] + CATEGORY_CHOICES, required=False, widget=forms.Select(attrs={'style': 'color: #5B3E39; background-color: white;'}))
    restaurant= forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'restaurant name'}))
    city = forms.ChoiceField(choices=[('', 'Select city')] + CITY_CHOICES, required=False, widget=forms.Select(attrs={'style': 'color: #5B3E39; background-color: white;'}))
    specialize = forms.ChoiceField(choices=[('', 'Select specialized')] + SPECIALIZED_CHOICES, required=False, widget=forms.Select(attrs={'style': 'color: #5B3E39; background-color: white;'}))
    price = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'price'}))
    rating = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'rating'}))
    min_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '1000',      # Nilai minimum
            'max': '1800000',   # Nilai maksimum
            'step': '1000',    # Langkah
            'value': '1000',    # Nilai awal
            'oninput': "this.nextElementSibling.value = this.value" # Menampilkan nilai
        })
    )

    max_price = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '1000',      # Nilai minimum
            'max': '1800000',   # Nilai maksimum
            'step': '1000',    # Langkah
            'value': '1800000', # Nilai awal
            'oninput': "this.nextElementSibling.value = this.value" # Menampilkan nilai
        })
    )
    min_rating = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '0',     # Atur nilai minimum
            'max': '5',     # Atur nilai maksimum (ubah sesuai kebutuhan)
            'step': '0.1',  # Atur langkah perubahan
            'value': '0',   # Nilai awal slider
            'oninput': "this.nextElementSibling.value = this.value" # Untuk menampilkan nilai
        })
    )
    # Menampilkan nilai di samping slider
    max_rating = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'type': 'range',
            'min': '0',     # Atur nilai minimum
            'max': '5',     # Atur nilai maksimum (ubah sesuai kebutuhan)
            'step': '0.1',  # Atur langkah perubahan
            'value': '5',   # Nilai awal slider
            'oninput': "this.nextElementSibling.value = this.value" # Untuk menampilkan nilai
        })
    )
    # Menampilkan nilai di samping slider

class AddMenuForm(forms.ModelForm):
   class Meta:
       model = Menu
       fields = ['menu', 'restaurant_name', 'price', 'rating', 'city', 'category', 'specialized', 'takeaway', 'delivery', 'outdoor', 'smoking_area', 'wifi', 'image']
       
       def clean_menu(self):
            menu = self.cleaned_data["menu"]
            return strip_tags(menu)
       def clean_restaurant(self):
            restaurant = self.cleaned_data["restaurant"]
            return strip_tags(restaurant)