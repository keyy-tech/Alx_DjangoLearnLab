from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author"]
