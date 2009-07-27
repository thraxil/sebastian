from django import forms
from models import *
from django.forms import ModelForm

class AddFaceForm(ModelForm):
    class Meta:
        model = Face
