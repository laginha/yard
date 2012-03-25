# Yet Another Restful Django-app


## Inspirations

1. [Django-Piston](https://bitbucket.org/jespern/django-piston/wiki/Home)
2. [Dagny](https://github.com/zacharyvoase/dagny)
3. [This snippet](http://djangosnippets.org/snippets/1071/)

Check those out.


## Motivations

- I like some things in *Piston*.
- I like *Dagny*.
- I wanted something neat to control the logic for acceptable parameters in each http-GET-requests.


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


*views.py*
<pre>
from django.views.decorators.csrf import csrf_exempt
from yard   import Resource
from models import Book

@csrf_exempt
class Books(Resource):
    #allowed query parameters - only used in index method
    parameters = (
        { 'name':     'year',                           #query parameter name - required
          'alias':    'publication_date__year',         #actual name within server's logic - not required
          'required': False,                            #defaults to False - not required
          'limit':    lambda x: max(1970, min(2012, x)) #parameter's logic - not required
        },
        { 'name': 'title' },
        { 'and': (                                      # genre AND ( author OR house )
            { 'name': 'genre', 'alias': 'genres'},
            { 'or': (
                { 'name': 'author', 'alias': 'author__id' },                                      
                { 'name': 'house',  'alias': 'publishing_house__id' }, ) 
            }, )
        },
    )
    #fields returned in json response - only used in index and show methods
    fields = ('id', 'title', 'publication_date', ('author', ('name',)) )
    
    @staticmethod
    def index(request, params):
        #GET /resource/
        return Book.objects.filter( **params )

    @staticmethod
    def show(request, book_id):
        #GET /resource/:id/
        return Book.objects.filter( id=book_id )
    
    @staticmethod
    def create(request):
        #POST /resource/
        ...
    
    @staticmethod
    def update(request):
        #PUT /resource/:id/
        ...
            
    @staticmethod
    def destroy(request):
        #DELETE /resource/:id/
        ...
</pre>

