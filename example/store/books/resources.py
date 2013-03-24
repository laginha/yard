from yard import forms, version, resources
from yard.resources.decorators import validate
from models import Book, Author

class AuthorResource(resources.Resource):
    model  = Author
    fields = ['name']
    
    def show(self, request, author_id):
        return Author.objects.get( pk=author_id )
    
    
class BookResource(resources.Resource):
    model  = Book
    fields = {
        'id': None, 
        'title': None, 
        'publication_date': None, 
        'genres': None, 
        'author': {
            'name': None,
            'age': None,
            'gender_': None,
        }
    }

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
    
    @validate    
    def index(self, request, params):
        return Book.objects.filter( **params ) #returns a JsonResponse-200

    def show(self, request, book_id):
        return Book.objects.get( id=book_id )


class BookResourceV2(BookResource):
    fields = ['title', 'author', 'publication_date']


class BookResourceVersions(version.ResourceVersions):
    v1 = default = BookResource
    v2 = latest = BookResourceV2    
