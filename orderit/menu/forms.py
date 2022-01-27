from django import forms
from .models import *


class NewMenuItem(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'image', 'price', 'category', 'day', 'status']