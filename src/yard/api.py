#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from easy_response.http import JsonResponse
from .exceptions import NoResourceMatch
from .utils.swagger import build_swagger_object
import re


class Api(object):
    '''
    Class responsible for generating the urlpatterns for the Resources
    '''
    
    def __init__(self, path=r'^', discover=False):
        self.list_of_urlpatterns = []
        self.model_to_urlname = {}
        self.path = path
        self.discoverable = discover
        if self.discoverable:
            self.list_of_urlpatterns.append(
                url(self.path+r'$', self.discover_view, name="api_documentation")
            )
        self.discoverable_paths = None

    @property
    def urlpatterns(self):
        '''
        Get the urlpatterns for this Api object
        '''
        return patterns( '', *self.list_of_urlpatterns )

    def include(self, resource_path, resource_class, name=None):
        '''
        Include url pattern for a given Resource
        '''
        
        class Dispatcher(object):
            def __init__(self, resource_class, routes):
                self.resource_class = resource_class
                self.routes = routes
                
            def __call__(self, *args, **kwargs):
                resource_instance = self.resource_class(self.routes)
                return resource_instance.handle_request(*args, **kwargs)
        
            def get_documentation(self):
                resource_instance = self.resource_class(self.routes)
                return resource_instance.get_documentation()
        
        resource_class.preprocess(self)
        for info in resource_class.get_views():
            items = info['routes'].iteritems()
            # if not any(hasattr(resource_class, v) for k,v in items):
            #     continue
            viewname = "%s.%s" %(name or resource_class.__name__, info['name'])
            self.list_of_urlpatterns.append(
                url(
                    self.path + resource_path + info['path'], 
                    Dispatcher(resource_class, info['routes']),
                    name = viewname,
                )
            )
            model = getattr(resource_class, 'model', None)
            if info['name'] == 'detail' and model:
                self.model_to_urlname[ resource_class.model ] = viewname

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
    
    def clean_pattern(self, pattern, sub='{pk}'):
        pattern = re.sub(r'\(\?P<(.+)>.+\)', sub, pattern)
        return re.sub(r'\?|\$|\^', '', pattern)
        
    def get_link(self, modelinstance):
        '''
        GET the to-fill-in-URL link
        '''
        def get_path_by_name(urlpatterns, name):
            for entry in urlpatterns:
                if hasattr(entry, 'url_patterns'):
                    path = get_path_by_name(entry.url_patterns, name)
                    if path:
                        return entry._regex + path
                if hasattr(entry, 'name') and entry.name == name:
                    return entry._regex
        
        if modelinstance.__class__ in self.model_to_urlname:
            name = self.model_to_urlname[ modelinstance.__class__ ]
            path = get_path_by_name(self.list_of_urlpatterns, name)
            return self.clean_pattern(path, sub="%s")
        raise NoResourceMatch( modelinstance.__class__ )

    def discover_view(self, request):
        '''
        Callback to return discoverable response from this Api object
        '''
        if self.discoverable_paths == None:
            self.discoverable_paths = self.get_discoverable_paths()
        content = build_swagger_object(request, paths=self.discoverable_paths)
        return JsonResponse(content=content, context=request)

    def get_discoverable_paths(self):
        '''
        JSON response with the discoveble Resources from this Api object
        '''
        def get_entry_paths(urllist, lambda_):
            pathlist = {}
            for entry in urllist:
                entry.clean_pattern = self.clean_pattern( entry.regex.pattern )
                if hasattr(entry, 'url_patterns'):
                    for each in get_entry_paths( entry.url_patterns, lambda_ ):
                        pathlist.append( entry.clean_pattern + each )
                elif not entry.clean_pattern:
                    continue
                else:
                    if not entry.clean_pattern.startswith('/'):
                        entry.clean_pattern = '/' + entry.clean_pattern
                    pathlist.update( lambda_(entry) )
            return pathlist
        
        return get_entry_paths(self.list_of_urlpatterns, lambda entry: {
            entry.clean_pattern: entry._callback.get_documentation()
        })
