#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls.defaults    import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers     import reverse
from yard.version import ResourceVersions


class Api(object):
    __collection = {'get':'index', 'post':'create'}
    __single     = {'get':'show', 'put':'update', 'post':'update', 'delete':'destroy'}

    def __init__(self):
        self.__urlpatterns = []
        self.__mapping = {}

    def include(self, resource_name, resource_class, single_name=None, collection_name=None):
        def single_pattern():
            path     = r'^%s/(?P<pk>[0-9]+)/?$' %resource_name
            resource = resource_class( self, self.__single )
            name     = single_name or "single."+resource_name
            return url( path, csrf_exempt( resource ), name=name )

        def collection_pattern():
            path     = r'^%s/?$' %resource_name
            resource = resource_class( self, self.__collection )
            name     = collection_name or "collection."+resource_name
            return url( path, csrf_exempt( resource ), name=name )

        self.__urlpatterns.append( single_pattern() )
        self.__urlpatterns.append( collection_pattern() )
        if hasattr(resource_class, 'model'):
            self.__mapping[ resource_class.model ] = resource_name

    def extend(self, path, to_include):
        self.__urlpatterns.append( url(path, include(to_include)) )

    def get_uri(self, model):
        if model.__class__ in self.__mapping:
            resource_name = self.__mapping[ model.__class__ ]
            return reverse( "single."+resource_name, kwargs={'pk':model.pk} )

    @property
    def urls(self):
        return patterns( '', *self.__urlpatterns )
