from django import forms
from .models import Book

class CreateBook(forms.ModelForm):
    class Meta:
        model = Book