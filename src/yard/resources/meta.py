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
        if is_generator(self.resources):
            self.total_objects     = self.__no_support
            self.paginated_objects = self.__paginated_list
        elif is_list(self.resources):
            self.total_objects     = self.__total_in_list
            self.paginated_objects = self.__paginated_list
    
    @property
    def page_count(self):
        if self._page_count == None:
            self._page_count = self.page.count()
        return self._page_count
        
    @property
    def resource_count(self):
        if self._resource_count == None:
            self._resource_count = self.resources.count()
        return self._resource_count
    
    def __no_support(self):
        pass

    def with_errors(self):
        self.update( self.params.errors() )
    
    def __page_uri(self, offset, params):
        dic_to_query = lambda x,y: "%s&%s=%s" % (x, y[0], y[1] if y[0]!='offset' else offset) 
        query = reduce(dic_to_query, self.request.GET.items(), '?')
        return self.request.path + "?" + query[2:]
    
    def next_page(self):
        params = self.params.validated
        if not self.page_count:
            self['next_page'] = None
        elif self.page_count < params['results']:
            self['next_page'] = None
        else:
            next_offset = params['offset'] + self.page_count
            self['next_page'] = self.__page_uri(next_offset, params)
        
    def previous_page(self):
        params = self.params.validated
        offset = min( self.resource_count, params['offset'] )
        previous_offset = offset - (self.page_count or params['results'])
        if previous_offset < 0 and offset <= 0:
            self['previous_page'] = None
        else:
            previous_offset = max( previous_offset, 0 )
            self['previous_page'] = self.__page_uri(previous_offset, params)
    
    def total_objects(self):
        self['total_objects'] = self.resource_count
    
    def __total_in_list(self):
        self['total_objects'] = len(self.resources)
    
    def paginated_objects(self):
        self['paginated_objects'] = self.page_count
    
    def __paginated_list(self):
        self['paginated_objects'] = len(self.page)
    
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
