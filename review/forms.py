from django.forms import ModelForm
from explore import forms
from review.models import ReviewEntry
from django.utils.html import strip_tags
from explore.models import Menu

# class MenuForm(forms.ModelForm):
#     class Meta:
#         model = Menu
#         fields = ['menu', 'restaurant_name', 'price', 'rating', 'category']

#     def clean_menu(self):
#         menu = self.cleaned_data["menu"]
#         return menu  # Kembali ke objek model Menu

#     def clean_restaurant_name(self):
#         restaurant_name = self.cleaned_data["restaurant_name"]
#         return restaurant_name

#     def clean_price(self):
#         price = self.cleaned_data["price"]
#         return price

#     def clean_rating(self):
#         rating = self.cleaned_data["rating"]
#         return rating

class ReviewEntryForm(ModelForm):
    class Meta:
        model = ReviewEntry
        fields = ["menu", "place", "rating", "description"]  # Tambahkan image

    # Pastikan untuk menambahkan validasi untuk field image jika diperlukan

        fields = ["menu", "place", "rating", "description"]
        
    def clean_menu(self):
        menu = self.cleaned_data["menu"]
        return strip_tags(menu)

    def clean_price(self):
        place = self.cleaned_data["place"]
        return strip_tags(place)
    
    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        return strip_tags(rating)