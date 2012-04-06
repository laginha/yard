from django.conf.urls.defaults import patterns, include, url
from views     import Books, Order
from yard.urls import include_resource

urlpatterns = patterns('django_yard.app.views.',
    url( r'^books',                           include_resource( Books ) ),
    url( r'^books/(?P<book_id>[0-9]+)/order', include_resource( Order ) ),
)
