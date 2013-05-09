#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from yard.version import ResourceVersions
from yard.utils.http import JsonResponse
from yard.exceptions import NoResourceMatch
from yard.utils.functions import get_entry_paths


class Api(object):
    __collection_routes = {
        'GET':'index', 
        'POST':'create',
        'OPTIONS': 'options'
    }
    __single_routes = {
        'GET':'show', 
        'PUT':'update', 
        'POST':'update', 
        'DELETE': 'destroy',
        'OPTIONS': 'options', 
    }

    def __init__(self, path=r'^', discover=False):
        self.__urlpatterns = []
        self.__mapping = {}
        self.__path = path
        self.discoverable = discover
        self.__discoverable_paths = None

    def include(self, resource_path, resource_class, single_name=None, collection_name=None):
        def build_single_pattern():
            name = single_name or "single."+resource_class.__name__
            path = r'%s%s/(?P<pk>[0-9]+)/?$' %(self.__path, resource_path)
            resource = resource_class( self, self.__single_routes )
            return url( path, csrf_exempt( resource ), name=name )
        
        def build_collection_pattern():
            name = collection_name or "collection."+resource_class.__name__
            path = r'%s%s/?$' %(self.__path, resource_path)
            resource = resource_class( self, self.__collection_routes )
            return url( path, csrf_exempt( resource ), name=name )

        if resource_class.has_any_method(self.__single_routes.values()):
            self.__urlpatterns.append( build_single_pattern() )
        if resource_class.has_any_method(self.__collection_routes.values()):
            self.__urlpatterns.append( build_collection_pattern() )
        if hasattr(resource_class, 'model'):
            self.__mapping[ resource_class.model ] = resource_class

    def extend(self, path, to_include, name=None):
        urlpattern = url(self.__path+path, include(to_include), name=name)
        self.__urlpatterns.append( urlpattern )

    def get_uri(self, modelinstance):
        if modelinstance.__class__ in self.__mapping:
            resource = self.__mapping[ modelinstance.__class__ ]
            return reverse( "single."+resource.__name__, kwargs={'pk':modelinstance.pk} )
        raise NoResourceMatch( modelinstance.__class__ )

    def __discover_callback(self, request):
        if self.__discoverable_paths == None:
            self.__discoverable_paths = self.discoverable_paths
        return JsonResponse(content=self.__discoverable_paths, context=request)
    
    @property
    def urlpatterns(self):
        urlpatterns = self.__urlpatterns
        if self.discoverable:
            urlpatterns.append( url(self.__path+"$", self.__discover_callback) )
        return patterns( '', *urlpatterns )

    @property
    def discoverable_paths(self):
        return {
            "Resources": get_entry_paths(self.__urlpatterns, lambda entry: {
                "uri": entry.clean_pattern,
                "description": entry._callback.__dict__["description"]
            })
        }    
