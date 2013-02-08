from django.conf.urls.defaults import patterns, include, url
from views     import *
from yard.api import Api

api = Api()
api.include( 'books', BookResourceVersions )
api.include( 'authors', AuthorResource )

urlpatterns = patterns('',
    url( r'^', include( api.urls ) )
)

