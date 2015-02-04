#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from yard.forms import Form
from yard.utils import is_tuple, is_queryset, is_modelinstance, is_generator, is_list
from yard.utils import is_valuesset, is_dict, is_many_related_manager
from yard.resources.utils.parameters import ResourceParameters
# from yard.resources.resource import JsonResource
from yard.resources.utils import (
    ResourceMeta, ResourcePage, model_to_fields
)


class ResourcePreprocessor(object):
    def __init__(self, resource_class, api, routes, show_fields=None, index_fields=None):  
        self.attributes = {} 
        self.attributes['resource_class'] = resource_class
        self.attributes['api']            = api
        self.attributes['routes']         = routes
        
        # if issubclass(resource_class, JsonResource):
        
        self.attributes['fields']         = self.get_fields()
        self.attributes['show_fields']    = show_fields or self.attributes['fields'] 
        self.attributes['index_fields']   = index_fields or self.attributes['fields'] 
        self.attributes['default_status'] = getattr(settings, 'DEFAULT_STATUS_CODE', 200)
        self.attributes['description']    = getattr(resource_class, "description", "not provided")
        self.attributes['uglify']         = getattr(resource_class, "uglify", False)
        self.attributes['pagination']     = self.get_resource_page()
        self.attributes['meta']           = self.get_resource_meta()
        self.attributes['builders']       = self.get_json_builders()
        self.attributes['parameters']     = self.get_parameters()
    
    def get_resource_attribute(self, name):
        resource_class = self.attributes['resource_class']
        return getattr(resource_class, name, type(name, (), {}))
    
    def get_fields(self):
        resource_class = self.attributes['resource_class']
        if hasattr(resource_class, "fields"):
            return resource_class.fields
        elif hasattr(resource_class, "model"):
            return model_to_fields(resource_class.model)
        return {}
    
    def get_resource_page(self):
        return ResourcePage( self.get_resource_attribute('Pagination') )
    
    def get_resource_meta(self):
        pagination = self.attributes['pagination']
        return ResourceMeta( pagination, self.get_resource_attribute('Meta') )

    def get_json_builders(self):
        fields = [
            self.attributes['index_fields'], 
            self.attributes['show_fields'], 
            self.attributes['fields'],
        ]
        api = self.attributes['api']
        resource_class = self.attributes['resource_class']
        json_builder = resource_class.json_builder_class
        return {
            id(i): json_builder(api, i) for i in fields if not callable(i)
        }
        
    def get_parameters(self):
        resource_class = self.attributes['resource_class']
        if hasattr(resource_class, "Parameters"):
            return Form( resource_class.Parameters )
    
    def create_resource_instance(self):
        return self.get_resource_class()(**self.attributes)
    
    def get_resource_class(self):
        return self.attributes['resource_class']
    
    def __call__(self, request, **kwargs):
        resource = self.attributes['resource_class'](**self.attributes)
        return resource.handle_request(request, **kwargs)
