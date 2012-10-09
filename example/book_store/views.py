from yard.resources import Resource
from models import Book
from params import BookParameters


class Books(Resource):
    parameters = BookParameters
    fields     = ['id', 'title', 'publication_date', 'genres', 
                 ('author', ('name','age','gender_')) ]
    
    class Meta:
        with_errors = True
        maximum = (('longest_title', 'title'),)
        average = (('average_pages', 'number_of_pages'),)

    class Page:
        offset_parameter = 'offset' #Required
        results_per_page = {
            'parameter': 'results', #Optional
            'default': 25,          #Required
            'limit': 50,            #Optional
        }
        
    def index(self, request, params):
        if params.is_valid():
            return Book.objects.filter( **params ) #returns a JsonResponse-200
        else:
            return 400, params.errors()

    def show(self, request, book_id):
        return Book.objects.get( id=book_id )
    
    def create(self, request):
        #HttpResponse(status=405)
        return 405
        
    def update(self, request, book_id):
        #defaults to HttpResponse(status=200)
        return
        
    def destroy(self, request, book_id):
        #HttpResponse('You are not authorize', status=401)
        return 401, 'You are not authorize'
