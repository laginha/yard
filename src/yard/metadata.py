#!/usr/bin/env python
# encoding: utf-8
from django.db.models import Avg, Max, Min, Count
from yard.exceptions import NoMeta
from yard.utils import is_generator


class MetadataDict(dict):
    '''
    Per-request resource's metadata
    '''
    def __init__(self, request, resources, page, params, pagination):
        self.request   = request
        self.resources = resources
        self.params    = params
        self.page      = page
        self.results_name = pagination.results_parameter
        self.offset_name  = pagination.offset_parameter
        if is_generator(self.resources):
            self.total_objects = lambda: None
            self.previous_page = lambda: None

    @property
    def page_count(self):
        '''
        Get the number of objects paginated in the response
        '''
        if not hasattr(self, '_page_count'):
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
        if not hasattr(self, '_resource_count'):
            if isinstance(self.resources, (list, tuple)):
                self._resource_count = len( self.resources )
            else:
                self._resource_count = self.resources.count()
        return self._resource_count

    def get_page_uri(self, offset):
        '''
        Get the URI with the offset value
        '''
        dic_to_query = lambda x,y: "%s&%s=%s" % (x, y[0], y[1])
        get = self.request.GET.copy()
        get[self.offset_name] = offset
        query_string = reduce(dic_to_query, get.items(), '?')[2:]
        return self.request.path + "?" + query_string

    def next_page(self, value):
        '''
        Adds the URI for the next page
        '''
        params = self.params.validated
        if not self.page_count:
            self['next_page'] = None
        elif self.page_count < params[ self.results_name ]:
            self['next_page'] = None
        else:
            next_offset = params[ self.offset_name ] + self.page_count
            if next_offset > self.resource_count:
                self['next_page'] = None
            else:
                self['next_page'] = self.get_page_uri(next_offset)

    def previous_page(self, value):
        '''
        Adds the URI for the previous page
        '''
        params = self.params.validated
        offset = min( self.resource_count, params[ self.offset_name ] )
        sub = (self.page_count or params[ self.results_name ])
        previous_offset = offset - sub
        if previous_offset < 0 and offset <= 0:
            self['previous_page'] = None
        else:
            previous_offset = max( previous_offset, 0 )
            self['previous_page'] = self.get_page_uri(previous_offset)

    def total_objects(self, value):
        '''
        Adds the total number of the response (not-paginated)
        '''
        self['total_objects'] = self.resource_count

    def paginated_objects(self, value):
        '''
        Adds the number of paginated objects in the response
        '''
        self['paginated_objects'] = self.page_count

    def validated_parameters(self, value):
        '''
        Adds the parameters validated according to Resource.Parameters
        '''
        self['validated_parameters'] = self.params.validated

    def set_aggregation(self, value, call):
        '''
        Auxiliar method for aggregation based metadata options
        '''
        if not value: 
            return
        for a,b in value:
            self[a] = self.resources.aggregate(_yard_=call(b))['_yard_']

    def minimum(self, value):
        '''
        Adds the returned queryset's Min aggregation of value
        '''
        self.set_aggregation(value, Min)

    def maximum(self, value):
        '''
        Adds the returned queryset's Max aggregation of value
        '''
        self.set_aggregation(value, Max)

    def average(self, value):
        '''
        Adds the returned queryset's Avg aggregation of value
        '''
        self.set_aggregation(value, Avg)

    def count(self, value):
        '''
        Adds the queryset's Count aggregation of value
        '''
        self.set_aggregation(value, Count)

    def custom(self, name, call):
        '''
        Add custom made metadata
        '''
        try:
            self[name] = call(self.resources)
        except Exception as e:
            return


class Metadata(object):
    '''
    Class responsible for generating resource's metadata 
    '''
    METADATA_OPTIONS = {
        'no_meta': False,
        'validated_parameters': True,
        'total_objects': True,
        'paginated_objects': True,
        'next_page': True,
        'previous_page': True,
        'average': None,
        'minimum': None,
        'maximum': None,
        'count': None,
        'custom': {},
    }
    
    def __init__(self, pagination):
        self.pagination = pagination
        self.default = {}
        for key,value in self.METADATA_OPTIONS.iteritems():
            if key == 'custom':
                self.custom = getattr(self, key, value)
            else:
                self.default[key] = getattr(self, key, value)
            
    def generate(self, request, resources, page, params):
        '''
        Generate metadata according to given args
        '''
        try:
            meta = MetadataDict( 
                request, resources, page, params, self.pagination
            )
            self.generate_defaults( meta )
            self.generate_custom_meta( meta )
            return meta
        except NoMeta:
            return meta

    def generate_defaults(self, meta):
        '''
        Generate metadata available by default
        '''
        for name,value in self.default.iteritems():
            if name == 'no_meta' and value:
                raise NoMeta()
            elif value:
                getattr(meta, name)( value )
        return meta

    def generate_custom_meta(self, meta):
        '''
        Generate custom made metadata
        '''
        for name,call in self.custom.iteritems():
            meta.custom( name, call )
