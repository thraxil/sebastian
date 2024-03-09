from django.forms import ModelForm

from .models import Face


class AddFaceForm(ModelForm):
    class Meta:
        model = Face
        exclude = []  # type: ignore
