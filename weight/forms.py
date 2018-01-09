from django import forms
from .models import *

class WeightForm(forms.ModelForm):
    class Meta:
        model=Weight
        exclude = [""]
