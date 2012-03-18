# Yet Another Restful Django-app


## Inspirations

1. [Django-Piston](https://bitbucket.org/jespern/django-piston/wiki/Home)
2. [Dagny](https://github.com/zacharyvoase/dagny)
3. [This snippet](http://djangosnippets.org/snippets/1071/)

Check those out, *yard* is rather simple actually


## Motivations

- I like some things of *Piston* 
- I like *Dagny*
- I wanted something neat to control the logic for acceptable parameters in each http-GET-requests

et voilá


## How to

*urls.py*
<pre>
from django.conf.urls.defaults import patterns, url
from yard.urls import include
from views import Books # my resource

urlpatterns = patterns('django_yard.app.views.',
    url( r'^books', include( Books ) ),
)
</pre>

*views.py*
<pre>
from django.views.decorators.csrf import csrf_exempt
from yard import Resource
from models import Book

@csrf_exempt #need this to enable http-POST-requests
class Books(Resource):
    #only for index method
    parameters = (
        {'name': 'year', # query parameter name - required
         'alias': 'publication_date', # actual name within server's logic - not required
         'required': False, # defaults to False - not required
         'limit': lambda x: max(1970, min(2012, x)) # parameter's logic - not required
        },
    )
    #fields returned in json response - only for index and show methods 
    fields = (('author', ('name','gender')), 'name' )

    @staticmethod
    def index(request, params):
        '''GET /books/'''
        return Book.objects.filter( **params )

    @staticmethod
    def show(request, book_id):
        '''GET /books/:id/'''
        return Book.objects.filter( id=book_id )

    @staticmethod
    def create(request):
        '''POST /books/'''
        return

    @staticmethod
    def update(request, book_id):
        '''PUT/POST /books/:id/'''
        return

    @staticmethod
    def destroy(request, book_id):
        '''DELETE /books/:id/'''
        return
</pre>
