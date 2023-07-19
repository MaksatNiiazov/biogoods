from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'company', 'address', 'password1', 'password2')

