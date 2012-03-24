from django.views.decorators.csrf import csrf_exempt
from yard   import Resource
from models import Book


@csrf_exempt
class Books(Resource):
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
    fields = ('id', 'title', 'publication_date', 'genres_', ('author', ('name','age','gender_')) )
    
    @staticmethod
    def index(request, params):
        return Book.objects.filter( **params )

    @staticmethod
    def show(request, book_id):
        return Book.objects.filter( id=book_id )
    
    @staticmethod
    def create(request):
        return
        
    @staticmethod
    def update(request, book_id):
        return
        
    @staticmethod
    def destroy(request, book_id):
        return
