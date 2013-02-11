from yard import forms, version, resources
from models import Book, Author

class AuthorResource(resources.Resource):
    model  = Author
    fields = ['name']
    
    def show(self, request, author_id):
        return Author.objects.get( pk=author_id )
    
    
class BookResource(resources.Resource):
    model  = Book
    fields = ['id', 'title', 'publication_date', 'genres', 
             ('author', ('name','age','gender_')) ]

    class Parameters:
        year   = forms.IntegerParam( alias='publication_date__year', min_value=1970, max_value=2012 )
        title  = forms.CharParam()
        genre  = forms.CharParam( alias='genres' )
        author = forms.CharParam( alias='author__id' )
        house  = forms.CharParam( alias='publishing_house__id' ) 

        __logic__ = year, title, genre & (author|house)    
    
    class Meta:
        maximum = (('longest_title', 'title'),)
        average = (('average_pages', 'number_of_pages'),)

    class Pagination:
        offset_parameter = 'offset'
        results_per_page = {        
            'parameter': 'results', 
            'default': 25,          
            'limit': 50,            
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


class BookResourceV2(BookResource):
    fields = ['title', 'author', 'publication_date']


class BookResourceVersions(version.ResourceVersions):
    v1 = default = BookResource
    v2 = latest = BookResourceV2    
