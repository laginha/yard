from yard.api import Api
from .resources import AuthorResource, BookResourceVersions

api = Api(discover=True)
api.include( 'books', BookResourceVersions )
api.include( 'authors', AuthorResource )

urlpatterns = api.urlpatterns
