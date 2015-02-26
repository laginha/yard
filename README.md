# Yet Another Restful Django Framework

**Yard** is an *API* oriented framework that aims to simplify the developer's work when implementing complex *API design*. It provides a neat, familiar and easy way to control the logic for acceptable parameters in each http-GET-request.


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

    def detail(self, request, book_id):
        #GET /resource/:id/
        return Book.objects.get( id=book_id )

    def create(self, request):
        #POST /resource/
        return 401, 'You are not authorize'

    def update(self, request, book_id):
        #PUT /resource/:id/
        ...

    def destroy(self, request, book_id):
        #DELETE /resource/:id/
        ...
```

*forms.py*

```
from yard import forms

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

*urls.py*

```python
from views    import AuthorResource, BookResource
from yard.api import Api

api = Api()
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
- Hypermedia API
- JSON serialization
- API discovery
- Pagination
- Metadata
- Resource versioning

For more information, check the [documentation](docs/index.md).


## Motivations

I've been working with a fairly complex project, with equally complex API design. *Django forms* weren't enough for what i needed, i still had too much code on my resources validating the input parameters. That was when I started to developed my own resource, inspired by the [Dagny](https://github.com/zacharyvoase/dagny) project, that would relieve my views from the ugliness of input validations.

With a few extra inspirations, *Yard* was born.

Other frameworks and applications, more mature and solid, such as [Tastypie](http://django-tastypie.readthedocs.org/en/latest/) and [Django-Rest-Framework](http://django-rest-framework.org/), can be enough for most needs. But i think *Yard* brings something new. In the end, I'm just having fun really and keeping it simple.

