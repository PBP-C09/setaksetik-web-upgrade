from django import forms
from .models import Message

class MessageEntryForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'content']  
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'subject': 'Subject',
            'body': 'Message',
        }