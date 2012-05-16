from django.conf.urls.defaults import patterns, include, url
from views     import Books
from yard.urls import include_resource

urlpatterns = patterns('django_yard.app.views.',
    url( r'^books', include_resource( Books ) ),
)
