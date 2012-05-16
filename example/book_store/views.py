from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Max
from yard   import Resource
from models import Book
from params import BookParameters

@csrf_exempt
class Books(Resource):
    parameters = BookParameters()
    fields     = ('id', 'title', 'publication_date', 'genres', ('author', ('name','age','gender_')) )
    
    class Meta:
        longest_title = lambda x: x.aggregate(longest=Max('title'))['longest']
        average_number_of_pages = lambda x: x.aggregate(pages=Avg('number_of_pages'))['pages']
    
    @staticmethod
    def index(request, params):
        return Book.objects.filter( **params ) #returns a JsonResponse-200
        #else:
        #    return 400, params.errors()

    @staticmethod
    def show(request, book_id):
        return Book.objects.get( id=book_id )
    
    @staticmethod
    def create(request):
        #HttpResponse(status=405)
        return 405
        
    @staticmethod
    def update(request, book_id):
        #defaults to HttpResponse(status=200)
        return
        
    @staticmethod
    def destroy(request, book_id):
        #HttpResponse('You are not authorize', status=401)
        return 401, 'You are not authorize'
