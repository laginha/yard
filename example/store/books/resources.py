from yard.resources.decorators import (
    validate, validate_form,resource_decorator, login_required)
from yard import forms, fields
from yard.version import VersionController
from yard.resources import Resource
from yard.resources.decorators import key_required
from .models import Book, Author
from .forms import CreateBook


@resource_decorator( key_required() )
class AuthorResource(Resource):
    model  = Author
    fields = {
        'name': fields.Unicode,
        'book_set': fields.RelatedManager,
    }
    def list(self, request, params):
        return Author.objects.filter( **params )
        
    def detail(self, request, author_id):
        return Author.objects.get( pk=author_id )


class BookResource(Resource):
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
        title  = forms.CharParam( alias='title__icontains' )
        genre  = forms.CharParam( alias='genres' )
        author = forms.CharParam( alias='author__id' )
        house  = forms.CharParam( alias='publishing_house__id' ) 
        datetime = forms.DateTimeParam()

        __logic__ = year, title, genre & (author|house), datetime  
    
    class Meta:
        maximum = (('longest_title', 'title'),)
        average = (('average_pages', 'number_of_pages'),)
    
    @validate
    # @key_required()
    def list(self, request, params):
        return Book.objects.filter( **params )

    @key_required()
    def detail(self, request, book_id):
        return Book.objects.get( id=book_id )
    
    # @validate_form(CreateBook)
    def create(self, *args, **kwargs):
        return 401
    
    # @validate_form(CreateBook)
    def update(self, *args, **kwargs):
        return 405

    def edit(self, *args, **kwargs):
        return 405


class BookResourceV2(BookResource):
    fields = {
        'title': fields.Unicode,
        'author': fields.URI,
        'publication_date': fields.Unicode
    }


class BookResourceVersions(VersionController):
    versions = {
        '1.0': BookResource, 
        '2.0': BookResourceV2,
    } 
    default = '1.0'
    latest  = '2.0'   
