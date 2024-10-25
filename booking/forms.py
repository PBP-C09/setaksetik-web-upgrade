from django import forms
from booking.models import Booking

city_choices = [
    ('central jakarta', 'Central Jakarta'),
    ('east jakarta', 'East Jakarta'),
    ('north jakarta', 'North Jakarta'),
    ('south jakarta', 'South Jakarta'),
    ('west jakarta', 'West Jakarta'),
]

class BookingForm(forms.ModelForm):  # Input user
    class Meta:
        model = Booking
        fields = ['booking_date', 'number_of_people']
    
class FilterForm(forms.Form):  # Filter untuk di create booking
    takeaway = forms.BooleanField(required=False)
    delivery = forms.BooleanField(required=False)
    outdoor = forms.BooleanField(required=False)
    wifi = forms.BooleanField(required=False)
    city = forms.ChoiceField(
        choices=[('', 'All Cities')] + city_choices,  # Tambahkan 'All Cities' sebagai opsi default
        required=False,
        label="City"
    )


