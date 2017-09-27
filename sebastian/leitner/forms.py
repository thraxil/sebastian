from .models import Face
from django.forms import ModelForm


class AddFaceForm(ModelForm):
    class Meta:
        model = Face
        exclude = []
