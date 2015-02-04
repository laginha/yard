#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from yard.exceptions import HttpMethodNotAllowed, RequiredParamMissing
from yard.utils import is_tuple, is_queryset, is_modelinstance, is_generator, is_list
from yard.utils import is_valuesset, is_dict, is_many_related_manager
from yard.utils.http import to_http
from yard.resources.utils import (
    ResourceParameters, JSONbuilder, with_pagination_and_meta
)
from yard.resources.utils.uglify import uglify_json
from yard.resources.utils.parameters import ResourceParameters
from yard.resources.utils.mixins import (
    DetailMixin, ListMixin, EditMixin, NewMixin, OptionsMixin
)
from yard import fields as YardFields
     

class BaseResource(object): 
    @classmethod
    def get_views(cls, api):
        for each in dir(cls):
            if each.startswith('as_') and each.endswith('_view'):
                yield getattr(cls, each)(api)
    
    def __init__(self, **kwargs):
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
    
    def handle_request(self, request, **kwargs):
        '''
        Called in every request made to Resource
        '''
        try:
            if request.method not in self.routes:
                return to_http(request, status=404)
            method = self.routes[request.method]
            if not getattr(self, method, None):
                # method not implemented
                return HttpResponse(status=405)
            return getattr(self, 'handle_'+method)(request, **kwargs)
        except (ObjectDoesNotExist, IOError):
            # ObjectDoesNotExist: if return model instance does not exist
            # IOError: if return file not found
            return HttpResponse(status=404)  
    
    def handle_show(self, request, **kwargs):
        return self.show(request, kwargs.pop('pk'), **kwargs)
    
    def handle_update(self, request, **kwargs):
        return self.update(request, kwargs.pop('pk'), **kwargs)
    
    def handle_destroy(self, request, **kwargs):
        return self.destroy(request, kwargs.pop('pk'), **kwargs)
    
    def handle_index(self, request, **kwargs):
        return self.index(request, **kwargs)
    
    def handle_create(self, request, **kwargs):
        return self.create(request, **kwargs)
    
    def handle_new(self, request, **kwargs):
        return self.new(request, **kwargs)
        
    def handle_edit(self, request, **kwargs):
        return self.edit(request, **kwargs)
        
    def handle_options(self, request, **kwargs):
        return self.options(request, **kwargs)
    
    def handle_response(self, request, response, fields, kwargs):
        return response
    
        
    
class JsonResource(BaseResource):
    '''
    API Resource object
    '''
    json_builder_class = JSONbuilder

    def get_builder(self, fields):
        '''
        Get JSON builder for the given fields
        '''
        return self.builders.get( id(fields) ) or self.json_builder_class( self.api, fields )

    def handle_response(self, request, response, fields, parameters):
        '''
        Proccess response into a JSON serializable object
        '''
        current_fields = fields(kwargs) if callable(fields) else fields
        status = self.default_status
        if is_tuple(response):
            status, response = response
        if is_valuesset(response):
            response = self.handle_list(request, list(response), parameters, current_fields)
        elif is_queryset(response):
            response = self.select_related(response, current_fields)
            response = self.handle_queryset(request, response, parameters, current_fields)
        elif is_modelinstance(response):
            response = self.handle_instance(response, current_fields)
        elif is_generator(response) or is_list(response):
            response = self.handle_list(request, response, parameters, current_fields)
        
        response = self.uglify_json(response) if self.uglify else response
        return to_http(request, response, status)

    @with_pagination_and_meta
    def handle_queryset(self, request, resources, parameters, fields):
        '''
        Serialize queryset based response
        '''
        builder = self.get_builder(fields)
        serialized = self.serialize_all( resources, fields, builder )
        return serialized, builder.links

    @with_pagination_and_meta
    def handle_list(self, request, resources, parameters, fields):
        '''
        Serialize list based response
        '''
        builder = self.get_builder(fields)
        serialized = [self.serialize(i, fields, builder) if is_modelinstance(i) else i for i in resources]
        return serialized, builder.links

    def handle_instance(self, resource, fields):
        '''
        Serialize model instance based response
        '''
        builder = self.get_builder(fields)
        response = self.serialize(resource, fields, builder, collection=False)
        if builder.links:
            response = {'Object': response, 'Links': builder.links}
        return response
        
    def paginate(self, request, resources, parameters):
        '''
        Return page of resources according to default or parameter values
        '''
        page_resources, page_parameters = self.pagination.select( request, resources )
        parameters.validated.update( page_parameters )
        return page_resources

    def select_related(self, resources, current_fields):
        '''
        Optimize queryset according to current response fields
        '''
        def find_related(items, prefix=''):
            for k,v in items:
                related = prefix+k
                if v in [YardFields.URI, YardFields.Link, YardFields.ForeignKey]:
                    resources.query.select_related[ related ] = {}
                elif v in [YardFields.GenericForeignKey, YardFields.RelatedManager]:
                    resources._prefetch_related_lookups.append( related )
                elif isinstance(v, dict):
                    resources.query.select_related[ related ] = {}
                    resources._prefetch_related_lookups.append( related )
                    find_related( v.iteritems(), related+'__' )
                   
        if resources.query.select_related == False:
            resources.query.select_related = {}
        find_related( current_fields.iteritems() )
        return resources

    def serialize_all(self, resources, fields, builder=None):
        '''
        Serializes each resource (within page) into json
        '''
        if builder == None:
            builder = self.get_builder(fields)
        return [builder.to_json(i) for i in resources]

    def serialize(self, resource, fields, builder=None, collection=True):
        '''
        Creates json for given resource
        '''
        if builder == None:
            builder = self.get_builder(fields)
        return builder.to_json(resource, collection)
    
    def uglify_json(self, response):
        response.update( uglify_json(response.pop('Objects')) )
        return response
        

class Resource(DetailMixin, ListMixin, EditMixin, NewMixin, OptionsMixin, JsonResource):
    pass
