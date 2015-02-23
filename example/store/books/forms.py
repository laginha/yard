from django import forms
from yard.forms import QueryModelForm, QueryForm, AND, OR
from .models import Book


class CreateBook(forms.ModelForm):
    class Meta:
        model = Book
        

class QueryBookForm(QueryModelForm):
    class Meta:
        model = Book
        fields = (
            'publication_date', 'title', 'genres', 
            'author', 'publishing_house'
        )
        aliases = {
            'publication_date': 'publication_date__year',
            'title': 'title__icontains',
        }
        extralogic = [
            AND('genres', OR('author', 'publishing_house'))   
        ]


class ListBook(QueryForm):
    year   = forms.IntegerField(required=False, min_value=1970, max_value=2012)
    title  = forms.CharField(required=False)
    genre  = forms.CharField(required=False)
    author = forms.CharField(required=False)
    house  = forms.CharField(required=False)
    
    class Meta:
        aliases = {
            'year': 'publication_date__year',
            'title': 'title__icontains',
            'genre': 'genres',
            'author': 'author_id',
            'house': 'publishing_house__id',
        }
        extralogic = [
            AND('genre', OR('author', 'house'))   
        ]
    