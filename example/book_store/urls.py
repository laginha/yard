from django.conf.urls.defaults import patterns, include, url
from views     import *
from yard.api import Api

api = Api(discover=True)
api.include( 'books', BookResourceVersions )
api.include( 'authors', AuthorResource )

urlpatterns = api.urlpatterns
