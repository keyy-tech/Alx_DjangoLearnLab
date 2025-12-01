from calendar import c
from tkinter import N
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields in self.fields.values():
            fields.widget.attrs.update({"class": "form-control"})
            fields.help_text = None


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fields in self.fields.values():
            fields.widget.attrs.update({"class": "form-control"})