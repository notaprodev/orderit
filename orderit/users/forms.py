from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, Customer, Restaurant, Item, Dep, UserRole, Menu
from django.contrib.auth.forms import UserCreationForm

class CustomerSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_customer = True
            if commit:
                user.save()
            return user


class RestuarantSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_restaurant = True
            if commit:
                user.save()
            return user


class NewUser(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_restaurant = True
            if commit:
                user.save()
            return user


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['f_name', 'l_name', 'city', 'phone', 'address']


class RestuarantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['rname', 'info', 'location', 'r_logo', 'min_ord', 'status', 'approved']


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'no_cel', 'money', 'user_role', 'dep']

