from yard.resources import Resource
from models import Book
from params import BookParameters

class Books(Resource):
    parameters = BookParameters()
    fields     = ('id', 'title', 'publication_date', 'genres', 
                 ('author', ('name','age','gender_')) )
    
    class Meta:
        with_errors = True
        maximum = (('longest_title', 'title'),)
        average = (('average_pages', 'number_of_pages'),)
        
    @staticmethod
    def index(request, params):
        if params.is_valid():
            return Book.objects.filter( **params ) #returns a JsonResponse-200
        else:
            return 400, params.errors()

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
        print 'here'
        return
        
    @staticmethod
    def destroy(request, book_id):
        #HttpResponse('You are not authorize', status=401)
        return 401, 'You are not authorize'
