#!/usr/bin/env python
# encoding: utf-8
from django.core.urlresolvers import NoReverseMatch
from yard.utils import is_related_manager, is_method, is_dict
from yard.resources import fields
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
        elif is_related_manager(resource):
            return [self.to_json( i ) for i in resource.all()]
        return self.__fields_to_json( resource )
        
    def __fields_to_json(self, resource):
        '''
        Builds (sub) json response according to given fields and resource
        '''
        try:
            uri   = self.api.get_uri( resource )
            json_ = {'resource_uri': uri} if uri else {}
        except NoReverseMatch:
            json_ = {}
        for key, value in self.fields.iteritems():
            json_.update( self.__handle_field(resource, key, value) )
        return json_

    def __handle_field(self, resource, key, value):
        '''
        Handler for each field
        '''
        if is_dict( value ):
            return self.__handle_dict_field( resource, key, value )
        return self.__handle_string_field( resource, key, value )

    def __handle_dict_field(self, resource, field, subfields):
        '''
        Handle fields of type tuple - subfields
        '''
        sub_resource = getattr( resource, field, None )
        builder = self.__class__( self.api, subfields )
        return { field: builder.to_json( sub_resource ) }

    def __handle_string_field(self, resource, field, type_):
        '''
        Handle fields of type string
        '''
        args      = field.split()
        attribute = getattr( resource, args[0], None )
        if is_method( attribute ):
            attribute = attribute( *args[1:] )
        if type_ is fields.URI:
            try:
                return {args[0]: type_( attribute, self.api )}
            except NoReverseMatch:
                return {args[0]: None}
        return {args[0]: type_( attribute )}

