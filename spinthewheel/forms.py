from django.forms import ModelForm
from spinthewheel.models import SpinHistory
from django.utils.html import strip_tags

class SpinHistoryForm(ModelForm):
    class Meta:
        model = SpinHistory
        fields = ["winner", "winnerId", "note"]

    def clean_note(self):
        note = self.cleaned_data["note"]
        return strip_tags(note)