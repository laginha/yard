#!/usr/bin/env python
# encoding: utf-8
from django.core.urlresolvers import NoReverseMatch
from yard.utils import is_tuple, is_geo_value, is_relatedmanager, is_manyrelatedmanager, is_genericrelatedobjectmanager
from yard.utils import is_method, is_valuesset, is_queryset, is_serializable, is_modelinstance
import json


class JSONbuilder:
    '''
    Responsible for creating the JSON response
    '''
    def __init__(self, api, fields):
        self.fields = fields() if callable(fields) else fields
        self.api    = api
    
    def to_json(self, resource):
        '''
        Builds JSON for resource according to fields attribute
        '''
        if not resource: 
            return
        elif is_relatedmanager(resource) or is_manyrelatedmanager(resource) or is_genericrelatedobjectmanager(resource):
            return [self.to_json( i ) for i in resource.all()]
        return self.__fields_to_json( resource )
        
    def __fields_to_json(self, resource):
        '''
        Builds (sub) json response according to given fields and resource
        '''
        try:
            json_ = {'resource_uri': self.api.get_uri( resource )}
        except NoReverseMatch:
            json_ = {}
        for field in self.fields:
            json_.update( self.__handle_field(resource, field) )
        return json_

    def __handle_field(self, resource, field):
        '''
        Handler for each field
        '''
        if is_tuple( field ):
            return self.__handle_tuple_field( resource, field )
        return self.__handle_string_field( resource, field )

    def __handle_tuple_field(self, resource, field ):
        '''
        Handle fields of type tuple - subfields
        '''
        sub_resource = getattr( resource, field[0], None )
        builder = self.__class__( self.api, field[1] )
        return { field[0]: builder.to_json( sub_resource ) }

    def __handle_string_field(self, resource, field):
        '''
        Handle fields of type string
        '''
        args      = field.split()
        attribute = getattr( resource, args[0], None )
        try:
            if is_method( attribute ):
                return self.__handle_method_field( attribute, args[1:] )
            return {args[0]: self.__serialize( attribute )}
        except NoReverseMatch:
            return {}

    def __handle_method_field(self, method, args):
        '''
        Handle fields of type str that are instance method
        '''
        result = method( *args )
        if is_valuesset( result ):
            return { method.__name__: list( result ) }
        elif is_queryset( result ):
            return { method.__name__: [unicode(i) for i in result] }
        return { method.__name__: self.__serialize(result) }
        
    def __serialize(self, x):
        '''
        Converts to JSON-serializable object
        '''
        if is_serializable(x):
            return x
        elif is_geo_value(x):
            return json.loads(x.geojson)
        elif is_relatedmanager(x) or is_manyrelatedmanager(x) or is_genericrelatedobjectmanager(x):
            return [unicode(i) for i in x.all()]
        elif is_modelinstance(x):
            return self.api.get_uri(x) or unicode(x)
        return unicode(x)

