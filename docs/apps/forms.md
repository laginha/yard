# Django ALO Form

Check out [this project](https://github.com/laginha/django-alo-forms)!

```python
from yard import forms # just a wrapper

class ListBook(forms.QueryForm):
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
```

```python
from yard.resources import Resource
from yard.decorators import validate

class Book(Resource):

    class Meta:
        model = models.Book

    @validate(ListBook)
    def list(self, request):
        return models.Book.objects.filter(**request.form.parameters)
```

As explained [here](meta/documentation.md), the `validate` decorator plays a part in the API documentation. Thus, when you use `alo.forms.QueryForm` or `alo.forms.QueryModelForm`, that module includes in the documentation JSON each field as parameter  of type `query` (instead of type 'form').

