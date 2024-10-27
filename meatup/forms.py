from django import forms
from .models import Wishlist, MeatupRequest

class MeatupRequestForm(forms.ModelForm):
    class Meta:
        model = MeatupRequest
        fields = ['receiver', 'wishlist', 'status']

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['item_name', 'description', 'is_public']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_name'].widget.attrs.update({
            'placeholder': 'Enter the item name...',
            'class': 'form-input',
        })
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Describe what you want to do...',
            'class': 'form-input',
        })
        self.fields['is_public'].label = "Make Wishlist Public"

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description

class MeatupRequestForm(forms.ModelForm):
    note = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Add a note for the receiver...',
            'class': 'form-input',
        }),
        label='Request Note',
        required=False
    )

    class Meta:
        model = MeatupRequest
        fields = ['note'] 