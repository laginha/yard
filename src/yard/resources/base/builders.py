#!/usr/bin/env python
# encoding: utf-8
from django.core.urlresolvers import NoReverseMatch
from yard.utils import is_related_manager, is_method, is_dict
from yard.fields import URI, Link
from yard.exceptions import NoResourceMatch
from yard.consts import RESOURCE_URI_KEYNAME, RESOURCE_PK_KEYNAME


class JSONbuilder(object):
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
        try:
            json = self.init_json( resource ) if is_part_of_collection else {}
        except (NoReverseMatch, NoResourceMatch):
            json = {}
        for key, value in self.fields.iteritems():
            json.update( self.handle_field(resource, key, value) )
        return json
    
    def init_json(self, resource):
        '''
        init JSON for the resource
        '''
        return {RESOURCE_URI_KEYNAME: self.api.get_uri(resource)}

    def handle_field(self, resource, key, value):
        '''
        Handler for each field
        '''
        if is_dict( value ):
            return self.handle_dict_field( resource, key, value )
        return self.handle_field_type( resource, key, value )

    def handle_dict_field(self, resource, field_name, subfields):
        '''
        Handle fields of type dict - subfields
        '''
        sub_resource = getattr( resource, field_name, None )
        builder = self.__class__( self.api, subfields )
        json = { field_name: builder.to_json( sub_resource ) }
        self.links.update( builder.links )
        return json

    def handle_field_type(self, resource, field_name, field_type):
        '''
        Handle field_names of type string
        '''
        args      = field_name.split()
        attribute = getattr( resource, args[0], None )
        if is_method( attribute ):
            attribute = attribute( *args[1:] )
        try:
            if field_type is URI:
                return {args[0]: field_type( attribute, self.api )}
            if field_type is Link:
                pk, link = field_type( attribute, self.api )
                self.links[args[0]] = link
                return {args[0]: pk}
        except (NoReverseMatch, NoResourceMatch):
            return {args[0]: None}
        return {args[0]: field_type( attribute )}


class JSONbuilderForMobile(JSONbuilder):
    '''
    Responsible for creating the JSON response optimized for mobile
    '''
    def init_json(self, resource):
        '''
        init JSON for the resource for mobile-driven response 
        '''
        self.links[resource.__class__.__name__] = self.api.get_link( resource )
        return {RESOURCE_PK_KEYNAME: resource.pk}
