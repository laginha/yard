#!/usr/bin/env python
# encoding: utf-8
from django.core.urlresolvers import NoReverseMatch
from yard.utils import is_related_manager, is_method, is_dict
from yard import fields
from yard.exceptions import NoResourceMatch
import json

class JSONbuilder:
    '''
    Responsible for creating the JSON response
    '''
    def __init__(self, api, fields, mobile=False):
        self.fields = fields() if callable(fields) else fields
        self.api = api
        self.links = {}
    
    def to_json(self, resource, is_part_of_collection=True):
        '''
        Builds JSON for resource according to fields attribute
        '''
        if not resource: 
            return
        elif is_related_manager(resource):
            return [self.to_json( i ) for i in resource.all()]
        return self.__fields_to_json( resource, is_part_of_collection )
                
    def __fields_to_json(self, resource, is_part_of_collection):
        '''
        Builds (sub) json response according to given fields and resource
        '''
        try:
            json_ = self._init_json( resource ) if is_part_of_collection else {}
        except (NoReverseMatch, NoResourceMatch):
            json_ = {}
        for key, value in self.fields.iteritems():
            json_.update( self.__handle_field(resource, key, value) )
        return json_
    
    def _init_json(self, resource):
        '''
        init JSON for the resource
        '''
        return {'resource_uri': self.api.get_uri(resource)}

    def __handle_field(self, resource, key, value):
        '''
        Handler for each field
        '''
        if is_dict( value ):
            return self.__handle_dict_field( resource, key, value )
        return self.__handle_string_field( resource, key, value )

    def __handle_dict_field(self, resource, field, subfields):
        '''
        Handle fields of type dict - subfields
        '''
        sub_resource = getattr( resource, field, None )
        builder = self.__class__( self.api, subfields )
        json_ = { field: builder.to_json( sub_resource ) }
        self.links.update( builder.links )
        return json_

    def __handle_string_field(self, resource, field, type_):
        '''
        Handle fields of type string
        '''
        args      = field.split()
        attribute = getattr( resource, args[0], None )
        if is_method( attribute ):
            attribute = attribute( *args[1:] )
        try:
            if type_ is fields.URI:
                return {args[0]: type_( attribute, self.api )}
            if type_ is fields.Link:
                pk, link = type_( attribute, self.api )
                self.links[args[0]] = link
                return {args[0]: pk}
        except (NoReverseMatch, NoResourceMatch):
            return {args[0]: None}
        return {args[0]: type_( attribute )}


class JSONbuilderForMobile(JSONbuilder):
    '''
    Responsible for creating the JSON response optimized for mobile
    '''
    def _init_json(self, resource):
        '''
        init JSON for the resource for mobile-driven response 
        '''
        self.links[resource.__class__.__name__] = self.api.get_link( resource )
        return {'pk': resource.pk}
