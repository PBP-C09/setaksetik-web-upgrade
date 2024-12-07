from django import forms
from .models import Message

class MessageEntryForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender', 'content']  
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),

        }
        labels = {
            'content': 'Message',
        }