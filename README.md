# Yet Another Restful Django Framework

**Yard** is an *API* oriented framework that aims to simplify the developer's work when implementing complex *API design*. It provides a neat, familiar and easy way to control the logic for acceptable parameters in each http-GET-request.


## Motivations

I've been working with a fairly complex project, with equally complex API design. *Django forms* weren't enough for what i needed, i still had too much code on my resources validating the input parameters. That was when I started to developed my own resource, inspired by the [Dagny](https://github.com/zacharyvoase/dagny) project, that would relieve my views from the ugliness of input validations.

With a few extra inspirations, *Yard* was born.

Other frameworks and applications, more mature and solid, such as [Django-Piston](https://bitbucket.org/jespern/django-piston/wiki/Home), [Tastypie](http://django-tastypie.readthedocs.org/en/latest/) and [Django-Rest-Framework](http://django-rest-framework.org/), can be enough for most needs. But i think *Yard* brings something new. In the end, I'm just having fun really and keeping it simple.


## Usage

*urls.py*
<pre>
from django.conf.urls.defaults import patterns, include, url
from views     import Books
from yard.urls import include_resource

urlpatterns = patterns('django_yard.app.views.',
    url( r'^books', include_resource( Books ) ),
)
</pre>

*params.py*
<pre>
from yard.forms import *    

class BookParameters(Form):
    year   = IntegerParam( alias='publication_date__year', min=1970, max=2012 )
    title  = CharParam( required=True )
    genre  = CharParam( alias='genres' )
    author = CharParam( alias='author__id' )
    house  = CharParam( alias='publishing_house__id' ) 

    __logic__ = year, title, genre & (author|house)
</pre>

*views.py*
<pre>
from yard.resources import Resource
from models import Book

class Books(Resource):
    # used in the index method
    parameters = BookParameters
    # used in the index and show methods
    fields = ( 'id', 'title', 'publication_date', 'genres', ('author', ('name', 'age',)) )
    
    # index's response metadata
    class Meta:
        maximum = (('longest_title', 'title'),)
        average = (('average_pages', 'number_of_pages'),)
    
    # index's pagination configuration  
    class Page:
        offset_parameter = 'offset'
        results_per_page = {
            'parameter': 'results',
            'default': 25,
            'limit': 50,
        }

    def index(self, request, params):
        #GET /resource/
        return Book.objects.filter( **params )

    def show(self, request, book_id):
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
</pre>

For more information, check the [documentation](docs/index.md).

