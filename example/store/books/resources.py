from yard.resources.decorators import (
    validate, resource_decorator, login_required)
from yard import forms, fields
from yard.version import VersionController
from yard.resources import Resource
from yard.resources.decorators import key_required
from .models import Book, Author
from .forms import CreateBook, ListBook, QueryBookForm
    

@resource_decorator( key_required() )
class AuthorResource(Resource):
    model  = Author
    fields = {
        'name': fields.Unicode,
        'book_set': fields.RelatedManager,
    }
    
    def list(self, request):
        return Author.objects.all()
        
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
    
    class Meta:
        maximum = (('longest_title', 'title'),)
        average = (('average_pages', 'number_of_pages'),)
    
    @validate(ListBook)
    # @key_required()
    def list(self, request):
        params = request.form.parameters
        return Book.objects.filter( **params )

    @key_required()
    def detail(self, request, book_id):
        return Book.objects.get( id=book_id )
    
    # @validate(CreateBook)
    def create(self, *args, **kwargs):
        return 401
    
    # @validate(CreateBook)
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
