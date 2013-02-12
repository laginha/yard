#!/usr/bin/env python
# encoding: utf-8

from django.db.models    import Avg, Max, Min, Count
from yard.exceptions     import NoMeta
from yard.utils          import is_list, is_generator
from yard.resources.page import ResourcePage


class MetaDict(dict):
    def __init__(self, request, resources, page, params):
        self.request   = request
        self.resources = resources   
        self.params    = params
        self.page      = page 
        self._page_count     = None
        self._resource_count = None
        self.__results_name  = ResourcePage.defaults[0][1]
        self.__offset_name   = ResourcePage.defaults[1][1]['parameter']
        if is_generator(self.resources):
            self.total_objects     = self.__no_support
    
    #TEMPORARY
    def add_page_class(self, page_class):
        self.__results_name = page_class.results_per_page['parameter']
        self.__offset_name  = page_class.offset_parameter 
    
    @property
    def page_count(self):
        if self._page_count == None:
            if isinstance(self.page, (list, len)):
                self._page_count = len( self.page )
            else:
                self._page_count = self.page.count()
        return self._page_count
        
    @property
    def resource_count(self):
        if self._resource_count == None:
            if isinstance(self.resources, (list, tuple)) or is_generator(self.resources):
                self._resource_count = len( self.resources )
            else:
                self._resource_count = self.resources.count()
        return self._resource_count
    
    def __no_support(self):
        pass

    def with_errors(self):
        self.update( self.params.errors() )
    
    def __page_uri(self, offset):
        dic_to_query = lambda x,y: "%s&%s=%s" % (x, y[0], y[1]) 
        get = self.request.GET.copy()
        get[self.__offset_name] = offset
        query_string = reduce(dic_to_query, get.items(), '?')[2:]
        return self.request.path + "?" + query_string
    
    def next_page(self):
        params = self.params.validated
        if not self.page_count:
            self['next_page'] = None
        elif self.page_count < params[ self.__results_name ]:
            self['next_page'] = None
        else:
            next_offset = params[ self.__offset_name ] + self.page_count
            self['next_page'] = self.__page_uri(next_offset)
        
    def previous_page(self):
        params = self.params.validated
        offset = min( self.resource_count, params[ self.__offset_name ] )
        previous_offset = offset - (self.page_count or params[ self.__results_name ])
        if previous_offset < 0 and offset <= 0:
            self['previous_page'] = None
        else:
            previous_offset = max( previous_offset, 0 )
            self['previous_page'] = self.__page_uri(previous_offset)
    
    def total_objects(self):
        self['total_objects'] = self.resource_count

    def paginated_objects(self):
        self['paginated_objects'] = self.page_count

    def validated_parameters(self):
        self['validated_parameters'] = self.params.validated

    def __aggregation(self, value, call):
        if not value: return
        for a,b in value:
            self[a] = self.resources.aggregate(_yard_=call(b))['_yard_']

    def minimum(self, value):
        self.__aggregation(value, Min)

    def maximum(self, value):
        self.__aggregation(value, Max)

    def average(self, value):
        self.__aggregation(value, Avg)

    def count(self, value):
        self.__aggregation(value, Count)

    def custom(self, name, call):
        try:
            self[name] = call(self.resources)
        except Exception as e:
            return


class ResourceMeta(object):
    __defaults = [
        ('no_meta',               False),
        ('with_errors',           False),
        ('validated_parameters',  True),
        ('total_objects',         True),
        ('paginated_objects',     True),
        ('next_page',             True),
        ('previous_page',         True),
        ('average',               None),
        ('minimum',               None),
        ('maximum',               None),
        ('count',                 None)
    ]

    def __init__(self, meta=type('Meta', (), {})):
        self.__new_meta = [
            (k,v) for k,v in meta.__dict__.iteritems() if callable(v)
        ]
        for k,v in self.__defaults:
            setattr(self, k, getattr(meta,k) if hasattr(meta, k) else v)
                      
    def fetch(self, request, resources, page, params):
        try:
            meta = MetaDict( request, resources, page, params )
            meta.add_page_class( self.page_class ) #TEMPORARY
            self.__fetch_defaults( meta ) 
            self.__fetch_new_meta( meta )
            return meta
        except NoMeta:
            return meta

    def __fetch_defaults(self, meta):
        for name,default in self.__defaults:
            value = getattr(self, name)
            if name=='no_meta' and value:
                raise NoMeta()
            elif default==None:
                getattr(meta, name)( value )
            elif value:
                getattr(meta, name)()
        return meta

    def __fetch_new_meta(self, meta):
        for name,call in self.__new_meta:
            meta.custom( name, call )
