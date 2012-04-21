from django.views.decorators.csrf import csrf_exempt
from yard   import Resource
from models import Book
from params import BookParameters

class Order(Resource):
    @staticmethod
    def show(request, order_id, **kwargs):
        return 200


@csrf_exempt
class Books(Resource):
    parameters = BookParameters()
    fields     = ('id', 'title', 'publication_date', 'genres', ('author', ('name','age','gender_')) )
    
    @staticmethod
    def index(request, params):
        print params
        return Book.objects.filter( **params ) #returns a JsonResponse-200

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
