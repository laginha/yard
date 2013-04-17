#!/usr/bin/env python
# encoding: utf-8
from django.conf.urls.defaults    import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers     import reverse
from yard.version    import ResourceVersions
from yard.utils.http import ProperJsonResponse
import re


class Api(object):
    __collection_routes = {'get':'index', 'post':'create'}
    __single_routes     = {'get':'show', 'put':'update', 'post':'update', 'delete':'destroy'}

    def __init__(self, path=r'^', discover=False):
        self.__urlpatterns = []
        self.__mapping     = {}
        self.__path        = path
        self.discoverable  = discover #TODO

    def include(self, resource_path, resource_class, single_name=None, collection_name=None):
        
        def single_pattern():
            path     = r'%s%s/(?P<pk>[0-9]+)/?$' %(self.__path, resource_path)
            resource = resource_class( self, self.__single_routes )
            name     = single_name or "single."+resource_class.__name__
            return url( path, csrf_exempt( resource ), name=name )
        
        def collection_pattern():
            path     = r'%s%s/?$' %(self.__path, resource_path)
            resource = resource_class( self, self.__collection_routes )
            name     = collection_name or "collection."+resource_class.__name__
            return url( path, csrf_exempt( resource ), name=name )

        has_methods = lambda x: [i for i in x if hasattr(resource_class, i)]
        if has_methods( self.__single_routes.values() ):
            self.__urlpatterns.append( single_pattern() )
        if has_methods( self.__collection_routes.values() ):
            self.__urlpatterns.append( collection_pattern() )
            
        if hasattr(resource_class, 'model'):
            self.__mapping[ resource_class.model ] = resource_class.__name__
        elif issubclass(resource_class, ResourceVersions):
            model = resource_class.get_resource_attribute('model')
            self.__mapping[ model ] = resource_class.__name__

    def extend(self, path, to_include, name=None):
        urlpattern = url(self.__path+path, include(to_include), name=name)
        self.__urlpatterns.append( urlpattern )

    def get_uri(self, model):
        if model.__class__ in self.__mapping:
            resource_name = self.__mapping[ model.__class__ ]
            return reverse( "single."+resource_name, kwargs={'pk':model.pk} )

    #def api_paths(self, request):
    #    def get_paths(urllist):
    #        pathlist = []
    #        for entry in urllist:
    #            regex   = r'\?|\$|\^|\(|P|\)|\+|\*|\[.+\]'
    #            urlpath = re.sub( regex, '', entry.regex.pattern )
    #            if hasattr(entry, 'url_patterns'):
    #                for i in get_paths( entry.url_patterns ):
    #                    pathlist.append( urlpath+i )
    #            else:
    #                pathlist.append( urlpath )
    #        return pathlist
    #    return ProperJsonResponse(request)(content=get_paths(self.__urlpatterns))

    @property
    def urlpatterns(self):
        urlpatterns = self.__urlpatterns
        #if self.discoverable:
        #    urlpatterns += [url( self.__path+"$", self.api_paths )]
        return patterns( '', *urlpatterns )
    
