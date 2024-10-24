from django import forms
from booking.models import Booking

class BookingForm(forms.ModelForm): # Input user
    class Meta:
        model = Booking
        fields = ['booking_date', 'number_of_people']
    
class FilterForm(forms.Form): # Filter untuk di create booking
    takeaway = forms.BooleanField(required=False)
    delivery = forms.BooleanField(required=False)
    outdoor = forms.BooleanField(required=False)
    wifi = forms.BooleanField(required=False)

