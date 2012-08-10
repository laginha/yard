#!/usr/bin/env python
# encoding: utf-8
from django.forms.models import model_to_dict
from yard.utils          import is_tuple, is_str, is_list, is_dict, is_geo_value
from yard.utils          import is_method, is_valuesset, is_queryset
import json


class JSONbuilder:
    '''
    Responsible for creating the JSON response
    '''
    def __init__(self, fields):
        self.fields = fields
        
    def __serialize(self, x):
        '''
        Converts to JSON-serializable object
        '''
        return x if isinstance(x, (list,dict)) else (
            json.loads(x.geojson) if is_geo_value(x) else unicode(x) )
    
    def __resource_to_dict(self, resource):
        '''
        Converts resource/model to dict according to fields
        '''
        is_attr  = lambda x: is_str(x) and not callable(x)
        keyvalue = lambda a,b: (a,self.__serialize(getattr(b,a)))
        attrs    = filter( is_attr, self.fields )
        return dict( 
            [ keyvalue(i, resource) for i in attrs if hasattr(resource, i)]
        )
    
    def __handle_method(self, method, args):
        '''
        Handle fields of type str that are instance method
        '''
        result = method( *args )
        if is_queryset( result ):
            return { method.__name__: [unicode(i) for i in result] }
        elif is_valuesset( result ):
            return { method.__name__: list( result ) }
        elif isinstance(result, (int, str, unicode)):
            return { method.__name__: result }
        return { method.__name__: self.__serialize(result) }
    
    def __handle_tuple(self, resource, field ):
        '''
        Handle fields of type tuple - subfields
        '''
        sub_resource = getattr( resource, field[0], None )
        # build sub-json
        return {
            field[0]: self.__class__( field[1] ).to_json( sub_resource )
        }
    
    def __handler(self, resource, field):
        '''
        Handler for each field
        '''
        if is_tuple( field ):
            return self.__handle_tuple( resource, field )
        #split method name from arguments
        args   = field.split()
        method = getattr( resource, args[0], None )
        if not is_method( method ):
            return {}
        return self.__handle_method( method, args[1:] )
    
    def __fields_to_json(self, resource, fields, dic={}):
        '''
        Builds (sub) json response according to given fields and resource
        '''
        for field in fields:
            dic.update( self.__handler(resource, field) )
        return dic
    
    def to_json(self, resource):
        '''
        Builds JSON for resource according to fields attribute
        '''
        if not resource:
            return
        try:
            json_  = self.__resource_to_dict( resource )
            fields = self.fields() if callable(self.fields) else self.fields
            return self.__fields_to_json( resource, fields, json_ )
        except AttributeError as e:
            # resource is a RelatedManager
            builder = self.__class__( self.fields )
            return [builder.to_json( i ) for i in resource.all()]   
