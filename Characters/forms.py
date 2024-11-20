from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Heroe


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='')

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]
        help_texts = {k: "" for k in fields}

class HeroeForm(forms.ModelForm):
    class Meta:
        model = Heroe
        fields = ['nombre', 'raza']
