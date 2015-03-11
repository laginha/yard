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
        lookups = {
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

As explained [here](meta/documentation.md), the `validate` decorator plays a part in the API documentation. Thus, when you use `alo.forms.QueryForm` or `alo.forms.QueryModelForm`, that module includes in the documentation JSON each field as parameter of type `query` (instead of type 'form').


---


In addition to `django-alo-forms`, *Yard* provides a reimplementation of `PointField`.


```python
from yard.gis import forms

class ListStores(forms.QueryForm):
    location = forms.PointField(latitude_first=True)
    ...
```

This field expects the following input: 

- `<latitude.float>,<longitude.float>` if `latitude_first` set to `True` (e.g. `40.2,-8.41667`) 
- `<longitude.float>,<latitude.float>` if `latitude_first` set to `False`, as it is by default. (e.g. `-8.41667,40.2`)
 
