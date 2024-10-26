from django.forms import ModelForm
from review.models import ReviewEntry
from django.utils.html import strip_tags

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