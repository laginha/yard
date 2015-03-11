#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from easy_response.utils.process import to_http
from yard.forms import Form
from yard.consts import (
    DEFAULT_STATUS_CODE, JSON_OBJECTS_KEYNAME, JSON_META_KEYNAME, 
    JSON_LINKS_KEYNAME,)
from yard.fields import (
    SELECT_RELATED_FIELDS, PREFETCH_RELATED_FIELDS,
    get_field as get_json_field)
from yard.utils import (
    is_tuple, is_queryset, is_modelinstance, is_generator, is_list,
    is_valuesset, is_dict,)
from .builders import JSONbuilder
from .uglify import uglify_json
from .meta import ResourceMeta
from .page import ResourcePage
from .mixins import DocumentationMixin


def include_metadata(f):
    '''
    Paginates and appends Meta data into the json response if in index view
    '''
    def wrapper(self, request, resources, fields, parameters):
        if hasattr(parameters, 'validated'):
            page = self.paginate( request, resources, parameters )
            objects, links = f(self, request, page, fields, parameters)
            meta = self.meta.generate(request, resources, page, parameters)
            return self.to_json(objects=objects, meta=meta, links=links)
        return f(self, request, resources, fields, parameters)[0]
    return wrapper 


def model_to_fields(model):
    fields = model._meta.fields
    return dict([
        (each.name, get_json_field(each)) for each in fields
    ])


class BaseResource(DocumentationMixin):
    '''
    API Resource object
    '''
    json_builder_class = JSONbuilder

    @classmethod
    def preprocess(cls, api, version_name=None):

        def get_resource_attribute(name):
            return getattr(cls, name, type(name, (), {}))
    
        def get_fields():
            if hasattr(cls, "fields"):
                return cls.fields
            return model_to_fields(cls.model)
    
        def get_resource_page():
            return ResourcePage( get_resource_attribute('Pagination') )
    
        def get_resource_meta():
            return ResourceMeta(cls.pagination, get_resource_attribute('Meta'))

        def get_json_builders():
            fields = [
                cls.list_fields, 
                cls.detail_fields, 
                cls.fields,
            ]
            builder = cls.json_builder_class
            return {
                id(i): builder(cls.api, i) for i in fields if not callable(i)
            }
        
        def get_parameters():
            if hasattr(cls, "Parameters"):
                return Form( cls.Parameters )

        cls.api           = api
        cls.version_name  = version_name
        cls.fields        = get_fields()
        cls.detail_fields = getattr(cls, "detail_fields", cls.fields)
        cls.list_fields   = getattr(cls, "list_fields", cls.fields)
        cls.description   = getattr(cls, "description", "not provided")
        cls.uglify        = getattr(cls, "uglify", False)
        cls.pagination    = get_resource_page()
        cls.meta          = get_resource_meta()
        cls.builders      = get_json_builders()
        cls.parameters    = get_parameters()

    @classmethod
    def get_views(cls):
        for each in dir(cls):
            if each.startswith('as_') and each.endswith('_view'):
                yield getattr(cls, each)()
    
    def __init__(self, routes):
        self.routes = routes

    @property
    def tagname(self):
        return self.model.__name__.lower()
        
    def handle_request(self, request, **kwargs):
        '''
        Called in every request made to Resource
        '''
        try:
            if request.method not in self.routes:
                return to_http(request, status=404)
            method = self.routes[request.method]
            if not hasattr(self, method):
                return HttpResponse(status=405)
            return getattr(self, 'handle_'+method)(request, kwargs)
        except (ObjectDoesNotExist, IOError):
            # ObjectDoesNotExist: if return model instance does not exist
            # IOError: if return file not found
            return HttpResponse(status=404)

    def get_builder(self, fields):
        '''
        Get JSON builder for the given fields
        '''
        return self.builders.get(id(fields) ) or \
            self.json_builder_class( self.api, fields )

    def handle_response(self, request, response, fields, parameters):
        '''
        Proccess response into a JSON serializable object
        '''
        current_fields = fields(kwargs) if callable(fields) else fields
        status = DEFAULT_STATUS_CODE
        if is_tuple(response):
            status, response = response
        if is_valuesset(response):
            response = self.handle_list_response(
                request, list(response), current_fields, parameters)
        elif is_queryset(response):
            response = self.select_related(response, current_fields)
            response = self.handle_queryset_response(
                request, response, current_fields, parameters)
        elif is_modelinstance(response):
            response = self.handle_model_response(response, current_fields)
        elif is_generator(response) or is_list(response):
            response = self.handle_list_response(
                request, response, current_fields, parameters)
        
        response = self.uglify_json(response) if self.uglify else response
        return to_http(request, response, status)

    @include_metadata
    def handle_queryset_response(self, request, resources, fields, parameters):
        '''
        Serialize queryset based response
        '''
        builder = self.get_builder(fields)
        serialized = self.serialize_all( resources, fields, builder )
        return serialized, builder.links

    @include_metadata
    def handle_list_response(self, request, resources, fields, parameters):
        '''
        Serialize list based response
        '''
        builder = self.get_builder(fields)
        serialized = []
        for each in resources:
            if is_modelinstance(each):
                serialized.append( self.serialize(each, fields, builder) )
            else:
                serialized.append( each )
        return serialized, builder.links

    def handle_model_response(self, resource, fields):
        '''
        Serialize model instance based response
        '''
        builder = self.get_builder(fields)
        response = self.serialize(resource, fields, builder, collection=False)
        if builder.links:
            response = {
                JSON_OBJECTS_KEYNAME: response, 
                JSON_LINKS_KEYNAME: builder.links
            }
        return response
    
    def to_json(self, objects, meta=None, links=None):
        if meta or links:
            result = {JSON_OBJECTS_KEYNAME: objects}
            if meta:
                result[JSON_META_KEYNAME] = meta
            if links:
                result[JSON_LINKS_KEYNAME] = links
            return result
        return objects
        
    def paginate(self, request, resources, parameters):
        '''
        Return page of resources according to default or parameter values
        '''
        page_objects, page_params = self.pagination.select(request, resources)
        parameters.validated.update( page_params )
        return page_objects

    def select_related(self, resources, current_fields):
        '''
        Optimize queryset according to current response fields
        '''
        def find_related(items, prefix=''):
            for name,fieldtype in items:
                related = prefix + name
                if fieldtype in SELECT_RELATED_FIELDS:
                    resources.query.select_related[ related ] = {}
                elif fieldtype in PREFETCH_RELATED_FIELDS:
                    resources._prefetch_related_lookups.append( related )
                elif isinstance(fieldtype, dict):
                    resources.query.select_related[ related ] = {}
                    resources._prefetch_related_lookups.append( related )
                    find_related( fieldtype.iteritems(), related + '__' )
                   
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
        response.update(
            uglify_json(response.pop(JSON_OBJECTS_KEYNAME))
        )
        return response
