#!/usr/bin/env python
# encoding: utf-8
from yard.utils import is_tuple, is_geo_value, is_relatedmanager, is_manyrelatedmanager
from yard.utils import is_method, is_valuesset, is_queryset, is_serializable
import json


class JSONbuilder:
    '''
    Responsible for creating the JSON response
    '''
    def __init__(self, fields):
        self.fields = fields() if callable(fields) else fields
    
    def to_json(self, resource):
        '''
        Builds JSON for resource according to fields attribute
        '''
        if not resource: 
            return
        elif is_relatedmanager(resource) or is_manyrelatedmanager(resource):
            return [self.to_json( i ) for i in resource.all()]
        return self.__fields_to_json( resource )
        
    def __fields_to_json(self, resource):
        '''
        Builds (sub) json response according to given fields and resource
        '''
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
        builder      = self.__class__( field[1] ) # build sub-json
        return { field[0]: builder.to_json( sub_resource ) }

    def __handle_string_field(self, resource, field):
        '''
        Handle fields of type string
        '''
        args      = field.split()
        attribute = getattr( resource, args[0], None )
        if is_method( attribute ):
            return self.__handle_method_field( attribute, args[1:] )
        return {args[0]: self.__serialize( attribute )}

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
        elif is_relatedmanager(x) or is_manyrelatedmanager(x):
            return [unicode(i) for i in x.all()]
        return unicode(x)

