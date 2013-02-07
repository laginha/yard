from django.conf.urls.defaults import patterns, include, url
from views     import *
from yard.urls import include_resource

urlpatterns = patterns('',
    url( r'^books',  include_resource( BookResourceVersions ) ),
    #url( r'^books',  include_resource( BookResource ) ),
)
