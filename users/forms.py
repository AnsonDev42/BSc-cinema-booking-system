import datetime

from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'short_password': "Passwords length are less than 8 characters long."
    }
    email = forms.EmailField()
    birthday = forms.DateField(initial=datetime.date.today)
    accept_tos = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password1',
            'password2',
            'birthday',
            'accept_tos',
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    
    def check_password_length(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if len(password1) < 8 and len(password2) < 8:
            raise forms.ValidationError(
                self.error_messages['short_password'],
                code='short_password',
            ) 