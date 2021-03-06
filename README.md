# Yet Another Restful Django Framework

**Yard** is an *API* oriented framework that aims to simplify the developer's work when implementing complex *API design*. It provides a neat, familiar and easy way to control the logic for acceptable parameters in each http-GET-request.


## Install

    pip install yard-framework==2.2.0

**Check the [version 3.x](https://github.com/laginha/yard/tree/develop)**

## Usage

*views.py*

```python
from yard import resources, forms, fields
from models import Book

class BooksResource(resources.Resource):
    # model associated with the resource (mandatory)
    model = Book
    # used in the index and show methods
    fields = {
        'id': fields.Integer, 
        'title': fields.Unicode, 
        'publication_date': fields.Unicode, 
        'author': {
            'age': fields.Integer,
            'name': fields.Unicode
        }        
    }
    
    class Parameters:
        year   = forms.IntegerParam( alias='publication_date__year', min=1970, max=2012 )
        title  = forms.CharParam( required=True )
        genre  = forms.CharParam( alias='genres' )
        author = forms.CharParam( alias='author__id' )
        house  = forms.CharParam( alias='publishing_house__id' )
        __logic__ = year, title, genre & (author|house)

    def list(self, request, params):
        #GET /resource/
        return Book.objects.filter( **params )

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

*urls.py*

```python
from views    import AuthorResource, BookResource
from yard.api import Api

api = Api()
api.include( 'books', BookResource )
api.include( 'authors', AuthorResource )

urlpatterns = api.urlpatterns
```


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

