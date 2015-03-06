# Yet Another Restful Django Framework

**Yard** is an *API* oriented framework that aims to simplify the developer's work when implementing complex *API design*.


## Usage

*views.py*

```python
from yard import resources, fields
from .models import Book
from .forms import BookListForm

class BooksResource(resources.Resource):

    class Meta:
        # model associated with the resource (mandatory)
        model = Book
        # used in the list and detail methods
        fields = {
            'id': fields.Integer, 
            'title': fields.Unicode, 
            'publication_date': fields.Unicode, 
            'author': {
                'age': fields.Integer,
                'name': fields.Unicode
            }        
        }

    @validate(BookListForm)
    def list(self, request):
        #GET /resource/
        return Book.objects.filter(**request.form.parameters)

    def detail(self, request, pk):
        #GET /resource/:pk/
        return Book.objects.get(pk=pk)
```

*forms.py*

```python
from yard import forms

class ListBook(forms.QueryForm):
    year   = forms.IntegerField(required=False, min_value=1970, max_value=2012)
    title  = forms.CharField(required=False) # Django's fields
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

*urls.py*

```python
from views import AuthorResource, BookResource
from yard.api import Api

api = Api(discover=True) # Swagger support
api.include( 'books', BookResource )
api.include( 'authors', AuthorResource )

urlpatterns = api.urlpatterns
```


## Install

*Yard* is available on Pypi:

    pip install yard-framework
    
You can also install from source:

    python setup.py install
    
    
## Main features

- Resource and API oriented 
- Complex API logic
- JSON serialization
- Hypermedia and API discovery (Swagger support)
- Resource versioning
- Pagination
- Metadata

For more information, check the [documentation](docs/index.md)!


## Motivations

Just having fun while learning :) Nonetheless, I think *Yard* brings something new.

Be aware, there are other frameworks and applications more mature and solid, such as [Tastypie](http://django-tastypie.readthedocs.org/en/latest/) and [Django-Rest-Framework](http://django-rest-framework.org/), which are awesome.
