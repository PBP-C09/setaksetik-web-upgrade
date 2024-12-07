from django import forms
from .models import Message
from main.models import UserProfile

class MessageEntryForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'title', 'content']
        widgets = {
            'receiver': forms.Select(attrs={
                'class': 'block w-full p-2 rounded-md text-white bg-[#3E2723] border border-[#6D4C41] text-center'
            }),
            'title': forms.TextInput(attrs={
                'class': 'block w-full p-2 rounded-md text-white bg-[#3E2723] border border-[#6D4C41] text-center'
            }),
            'content': forms.Textarea(attrs={
                'class': 'block w-full p-2 rounded-md text-white bg-[#3E2723] border border-[#6D4C41] text-center',
                'rows': 5
            }),
        }
        labels = {
            'content': 'Message',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter UserProfile with role 'steak lover' and use their user.full_name for display
        steak_lovers = UserProfile.objects.filter(role="steak lover")
        self.fields['receiver'].queryset = steak_lovers
        self.fields['receiver'].label_from_instance = lambda obj: obj.full_name
