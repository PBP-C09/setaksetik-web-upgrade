from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile

class UserProfileForm(UserCreationForm):
    role = forms.ChoiceField(choices = (("customer", "Customer"), ("admin", "Admin"), ("steakhouse owner", "Steakhouse Owner")),label="Choose your role!", required=True)
    full_name = forms.CharField(label = "What's your name?", required=True)

    class Meta:
        model = User
        fields = ("role", "full_name", "username","password1", "password2")
        labels = {
            'username': 'Create a unique username!',
            'password1': 'Type a password',
            'password2': 'Retype your password'
        }
        help_texts = {
            'username': ''
        }

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        if commit:
            user.save()
        UserProfile.objects.create(user = user, full_name = self.cleaned_data["full_name"], role = self.cleaned_data["role"]
        )
        return user