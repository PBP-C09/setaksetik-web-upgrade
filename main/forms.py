from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from main.models import UserProfile

class UserProfileForm(UserCreationForm):
    role = forms.ChoiceField(choices = (("steak lover", "Steak Lover"), ("steakhouse owner", "Steakhouse Owner")),label="Choose your role!", required=True)
    full_name = forms.CharField(label = "What's your name?", required=True)

    class Meta:
        model = User
        fields = ("role", "username","full_name", "password1", "password2")
        labels = {
            'username': 'Create a unique username!',
            'password1': 'Type a password',
            'password2': 'Retype your password'
        }
        error_messages = {
            'username': {
                'unique': "This username is already taken :( Is it you tho?",
                'invalid': "Username can only contain letters, numbers, and @/./+/-/_ characters >:(",
            },
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the help texts
        self.fields['username'].help_text = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""

        self.fields['username'].label = self.Meta.labels['username']
        self.fields['password1'].label = self.Meta.labels['password1']
        self.fields['password2'].label = self.Meta.labels['password2']

        self.fields['username'].widget.attrs.update({
            'placeholder': 'No spaces, no weird characters; eg. kevinmoon'
        })
        self.fields['full_name'].widget.attrs.update({
            'placeholder': 'You are not Kevin Moon'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'At least 8 chars, no full numerics!'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Make sure its exactly the same'
        })

    # def save(self, commit=True):
    #     user = super(UserProfileForm, self).save(commit=False)
    #     if commit:
    #         user.save()
    #     UserProfile.objects.create(user = user, full_name = self.cleaned_data["full_name"], role = self.cleaned_data["role"]
    #     )
    #     return user