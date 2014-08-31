#!/usr/bin/env python
# encoding: utf-8
from django.db.models    import Avg, Max, Min, Count
from yard.exceptions     import NoMeta
from yard.utils          import is_list, is_generator
from yard.resources.utils.page import ResourcePage


class MetaDict(dict):
    '''
    Per-request resource's metadata
    '''
    def __init__(self, request, resources, page, params, pagination):
        self.request   = request
        self.resources = resources
        self.params    = params
        self.page      = page
        self._page_count     = None
        self._resource_count = None
        self.__results_name = pagination.results_per_page['parameter']
        self.__offset_name  = pagination.offset_parameter
        if is_generator(self.resources):
            self.total_objects = self.__no_support
            self.previous_page = self.__no_support

    @property
    def page_count(self):
        '''
        Get the number of objects paginated in the response
        '''
        if self._page_count == None:
            if isinstance(self.page, (list, tuple)) or is_generator(self.resources):
                self._page_count = len( self.page )
            else:
                self._page_count = self.page.count()
        return self._page_count

    @property
    def resource_count(self):
        '''
        Get the total number of objects in the resource
        '''
        if self._resource_count == None:
            if isinstance(self.resources, (list, tuple)):
                self._resource_count = len( self.resources )
            else:
                self._resource_count = self.resources.count()
        return self._resource_count

    def __no_support(self):
        '''
        No support available for self.resource given its type
        '''
        pass

    def with_errors(self):
        '''
        Adds the errors cought while processing the input parameters
        '''
        self.update( self.params.errors() )

    def __page_uri(self, offset):
        '''
        Get the URI with the offset value
        '''
        dic_to_query = lambda x,y: "%s&%s=%s" % (x, y[0], y[1])
        get = self.request.GET.copy()
        get[self.__offset_name] = offset
        query_string = reduce(dic_to_query, get.items(), '?')[2:]
        return self.request.path + "?" + query_string

    def next_page(self):
        '''
        Adds the URI for the next page
        '''
        params = self.params.validated
        if not self.page_count:
            self['next_page'] = None
        elif self.page_count < params[ self.__results_name ]:
            self['next_page'] = None
        elif self.page_count <= self.resource_count:
            self['next_page'] = None
        else:
            next_offset = params[ self.__offset_name ] + self.page_count
            if next_offset > self.resource_count:
                self['next_page'] = None
            else:
                self['next_page'] = self.__page_uri(next_offset)

    def previous_page(self):
        '''
        Adds the URI for the previous page
        '''
        params = self.params.validated
        offset = min( self.resource_count, params[ self.__offset_name ] )
        previous_offset = offset - (self.page_count or params[ self.__results_name ])
        if previous_offset < 0 and offset <= 0:
            self['previous_page'] = None
        else:
            previous_offset = max( previous_offset, 0 )
            self['previous_page'] = self.__page_uri(previous_offset)

    def total_objects(self):
        '''
        Adds the total number of the response (not-paginated)
        '''
        self['total_objects'] = self.resource_count

    def paginated_objects(self):
        '''
        Adds the number of paginated objects in the response
        '''
        self['paginated_objects'] = self.page_count

    def validated_parameters(self):
        '''
        Adds the parameters validated according to Resource.Parameters
        '''
        self['validated_parameters'] = self.params.validated

    def __aggregation(self, value, call):
        '''
        Auxiliar method for aggregation based metadata options
        '''
        if not value: return
        for a,b in value:
            self[a] = self.resources.aggregate(_yard_=call(b))['_yard_']

    def minimum(self, value):
        '''
        Adds the returned queryset's Min aggregation of value
        '''
        self.__aggregation(value, Min)

    def maximum(self, value):
        '''
        Adds the returned queryset's Max aggregation of value
        '''
        self.__aggregation(value, Max)

    def average(self, value):
        '''
        Adds the returned queryset's Avg aggregation of value
        '''
        self.__aggregation(value, Avg)

    def count(self, value):
        '''
        Adds the queryset's Count aggregation of value
        '''
        self.__aggregation(value, Count)

    def custom(self, name, call):
        '''
        Add custom made metadata
        '''
        try:
            self[name] = call(self.resources)
        except Exception as e:
            return


class ResourceMeta(object):
    '''
    Class responsible for generating resource's metadata 
    '''
    
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

    def __init__(self, pagination, meta=type('Meta', (), {})):
        self.__pagination = pagination
        self.__new_meta = [
            (k,v) for k,v in meta.__dict__.iteritems() if callable(v)
        ]
        for k,v in self.__defaults:
            setattr(self, k, getattr(meta, k, v))

    def generate(self, request, resources, page, params):
        '''
        Generate metadata according to given args
        '''
        try:
            meta = MetaDict( request, resources, page, params, self.__pagination )
            self.__generate_defaults( meta )
            self.__generate_custom_meta( meta )
            return meta
        except NoMeta:
            return meta

    def __generate_defaults(self, meta):
        '''
        Generate metadata available by default
        '''
        for name,default in self.__defaults:
            value = getattr(self, name)
            if name=='no_meta' and value:
                raise NoMeta()
            elif default==None:
                getattr(meta, name)( value )
            elif value:
                getattr(meta, name)()
        return meta

    def __generate_custom_meta(self, meta):
        '''
        Generate custom made metadata
        '''
        for name,call in self.__new_meta:
            meta.custom( name, call )
