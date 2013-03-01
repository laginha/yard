# Yet Another Restful Django Framework

**Yard** is an *API* oriented framework that aims to simplify the developer's work when implementing complex *API design*. It provides a neat, familiar and easy way to control the logic for acceptable parameters in each http-GET-request.


## Install

*Yard* is available on Pypi:

Other frameworks and applications, more mature and solid, such as [Tastypie](http://django-tastypie.readthedocs.org/en/latest/) and [Django-Rest-Framework](http://django-rest-framework.org/), can be enough for most needs. But i think *Yard* brings something new. In the end, I'm just having fun really and keeping it simple.
<<<<<<< HEAD

## Install

*Yard* is available on Pypi:

    pip install yard-framework
    
You can also install from source:

    python setup.py install
=======
>>>>>>> update and improve docs

## Install

*Yard* is available on Pypi:

<<<<<<< HEAD
*urls.py*

```python
<<<<<<< HEAD
from views    import AuthorResource, BookResource
from yard.api import Api
=======
from yard.forms import *    
=======
    pip install yard-framework
    
You can also install from source:

    python setup.py install


## Usage

*urls.py*
<pre>
```python
from views    import AuthorResource, BookResource
from yard.api import Api
>>>>>>> update and improve docs
>>>>>>> update and improve docs

api = Api()
api.include( 'books', BookResource )
api.include( 'authors', AuthorResource )

<<<<<<< HEAD
urlpatterns = api.urlpatterns
=======
<<<<<<< HEAD
    __logic__ = year, title, genre & (author|house)
>>>>>>> update and improve docs
```

*views.py*

```python
<<<<<<< HEAD
from yard import resources, forms
=======
from yard.resources import Resource
=======
urlpatterns = api.urlpatterns
```
</pre>

*views.py*
<pre>
```python
from yard import resources, forms
>>>>>>> update and improve docs
>>>>>>> update and improve docs
from models import Book

class BooksResource(resources.Resource):
    # model associated with the resource
    model = Book
    # used in the index and show methods
    fields = ( 'id', 'title', 'publication_date', 'genres', ('author', ('name', 'age',)) )
    
    class Parameters:
        year   = forms.IntegerParam( alias='publication_date__year', min=1970, max=2012 )
        title  = forms.CharParam( required=True )
        genre  = forms.CharParam( alias='genres' )
        author = forms.CharParam( alias='author__id' )
        house  = forms.CharParam( alias='publishing_house__id' )
        __logic__ = year, title, genre & (author|house)

    def index(self, request, params):
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
<<<<<<< HEAD
=======
</pre>
>>>>>>> update and improve docs

## Main features

- Resource and API oriented 
- Complex API logic
- Hypermedia API
- JSON serialization
- Pagination
- Metadata
- Resource versioning
- Django Debug Toolbar support


## Main features

- Resource and API oriented 
- Complex API logic
- Hypermedia API
- JSON serialization
- Pagination
- Metadata
- Resource versioning
- Django Debug Toolbar support

For more information, check the [documentation](docs/index.md).
