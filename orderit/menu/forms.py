from django import forms
from .models import *


class NewMenuItem(forms.ModelForm):
    #image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'image', 'price', 'category', 'day', 'status']
