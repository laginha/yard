from yard.resources.decorators import validate, decorator_for_response_methods
from yard import forms, version, resources, fields
from yard.apps.keyauth.decorators import key_required
from models import Book, Author


@decorator_for_response_methods( key_required )
class AuthorResource(resources.Resource):
    model  = Author
    fields = {
        'name': fields.Unicode,
        'book_set': fields.RelatedManager,
    }
    def index(self, request, params):
        return Author.objects.filter( **params )
        
    def show(self, request, author_id):
        return Author.objects.get( pk=author_id )


class BookResource(resources.Resource):
    description = "Search books in our store."
    model  = Book
    fields = {
        'id': fields.Auto,
        'title': fields.Auto, 
        'publication_date': fields.Auto, 
        'genres': fields.Auto,
        'author': {
            'name': fields.Auto,
            'age': fields.Auto,
            'gender_': fields.Auto,
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
        return Book.objects.filter( **params )

    @key_required
    def show(self, request, book_id):
        return Book.objects.get( id=book_id )
        
    def create(self, *args, **kwargs):
        return 401


class BookResourceV2(BookResource):
    fields = {
        'title': fields.Unicode,
        'author': fields.URI,
        'publication_date': fields.Unicode
    }


class BookResourceVersions(version.ResourceVersions):
    v1 = default = BookResource
    v2 = latest = BookResourceV2    
