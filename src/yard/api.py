#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from yard.version import ResourceVersions
from yard.utils.http import JsonResponse
from yard.exceptions import NoResourceMatch
from yard.utils.functions import get_entry_paths, get_path_by_name
import re


class Api(object):
    '''
    Class responsible for generating the urlpatterns for the Resources
    '''
    
    COLLECTION_ROUTES = {
        'GET':'index', 
        'POST':'create',
        'OPTIONS': 'options'
    }
    SINGLE_ROUTES = {
        'GET':'show', 
        'PUT':'update', 
        'POST':'update', 
        'DELETE': 'destroy',
        'OPTIONS': 'options', 
    }

    def __init__(self, path=r'^', discover=False):
        self.list_of_urlpatterns = []
        self.model_to_urlname = {}
        self.path = path
        self.discoverable = discover
        if self.discoverable:
            self.list_of_urlpatterns.append( url(self.path+"$", self.discover_view) )
        self.discoverable_response = None

    @property
    def urlpatterns(self):
        '''
        Get the urlpatterns for this Api object
        '''
        return patterns( '', *self.list_of_urlpatterns )

    def include(self, resource_path, resource_class, single_name=None, collection_name=None):
        '''
        Include url pattern for a given Resource
        '''
        def build_single_pattern():
            name = single_name or "single."+resource_class.__name__
            path = r'%s%s/(?P<pk>[0-9]+)/?$' %(self.path, resource_path)
            resource = resource_class( self, self.SINGLE_ROUTES )
            return url( path, csrf_exempt( resource ), name=name )
        
        def build_collection_pattern():
            name = collection_name or "collection."+resource_class.__name__
            path = r'%s%s/?$' %(self.path, resource_path)
            resource = resource_class( self, self.COLLECTION_ROUTES )
            return url( path, csrf_exempt( resource ), name=name )
        
        if resource_class.has_any_method(self.SINGLE_ROUTES.values()):
            self.list_of_urlpatterns.append( build_single_pattern() )
            if getattr(resource_class, 'model', None):
                self.model_to_urlname[ resource_class.model ] = self.list_of_urlpatterns[-1].name
        if resource_class.has_any_method(self.COLLECTION_ROUTES.values()):
            self.list_of_urlpatterns.append( build_collection_pattern() )

    def extend(self, path, to_include, name=None):
        '''
        Include urlpatterns from another path
        '''
        urlpattern = url(self.path+path, include(to_include), name=name)
        self.list_of_urlpatterns.append( urlpattern )

    def get_uri(self, modelinstance):
        '''
        Get the URI of a Resource according to a given model
        '''
        if modelinstance.__class__ in self.model_to_urlname:
            name = self.model_to_urlname[ modelinstance.__class__ ]
            return reverse( name, kwargs={'pk':modelinstance.pk} )
        raise NoResourceMatch( modelinstance.__class__ )
        
    def get_link(self, modelinstance):
        '''
        GET the to-fill-in-URL link
        '''
        if modelinstance.__class__ in self.model_to_urlname:
            name = self.model_to_urlname[ modelinstance.__class__ ]
            path = get_path_by_name(self.list_of_urlpatterns, name)
            path = re.sub(r'\(\?P<(.+)>.+\)', "%s", path)
            return re.sub(r'\?|\$|\^', '', path)
        raise NoResourceMatch( modelinstance.__class__ )

    def discover_view(self, request):
        '''
        Callback to return discoverable response from this Api object
        '''
        if self.discoverable_response == None:
            self.discoverable_response = self.get_discoverable_response()
        return JsonResponse(content=self.discoverable_response, context=request)

    def get_discoverable_response(self):
        '''
        JSON response with the discoveble Resources from this Api object
        '''
        return {
            "Resources": get_entry_paths(self.list_of_urlpatterns, lambda entry: {
                "uri": entry.clean_pattern,
                "description": entry._callback.__dict__["description"]
            })
        }    
