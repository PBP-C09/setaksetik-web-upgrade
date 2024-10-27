from django.forms import ModelForm
from spinthewheel.models import SpinHistory, SecretHistory
from django.utils.html import strip_tags

class SpinHistoryForm(ModelForm):
    class Meta:
        model = SpinHistory
        fields = ["winner", "winnerId", "note"]

    def clean_note(self):
        note = self.cleaned_data["note"]
        return strip_tags(note)
    
class SecretHistoryForm(ModelForm):
    class Meta:
        model = SecretHistory
        fields = ["winner", "note"]

    def clean_note(self):
        note = self.cleaned_data["note"]
        return strip_tags(note)