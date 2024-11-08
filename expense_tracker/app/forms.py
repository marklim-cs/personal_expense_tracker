from django import forms
from .models import PROFESSION

class SignupForm(forms.Form):
    username = forms.CharField(max_length=20, label="Username")
    fname = forms.CharField(max_length=20, label="First name")
    lname = forms.CharField(max_length=20, label="Last name")
    email = forms.EmailField(max_length=100, label="Email")
    profession = forms.ChoiceField(widget=forms.RadioSelect, choices=PROFESSION)
    savings = forms.IntegerField(required=False)
    income = forms.IntegerField(required=True)