from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, AddMoneyInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ["user", "expenses"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

class AddMoneyForm(forms.ModelForm):
    class Meta:
        model = AddMoneyInfo
        fields = ["expense_type", "quantity", "date", "category"]