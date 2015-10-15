#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from easy_response.utils.process import to_http
from yard.forms import Form
from yard.consts import DEFAULT_STATUS_CODE
from yard.consts import JSON_OBJECTS_KEYNAME
from yard.consts import JSON_METADATA_KEYNAME
from yard.consts import JSON_LINKS_KEYNAME
from yard.utils import is_tuple
from yard.utils import is_queryset
from yard.utils import is_modelinstance
from yard.utils import is_generator
from yard.utils import is_list
from yard.utils import is_valuesset
from yard.utils import is_dict
from yard.serializers import uglify_json
from yard.decorators.django_alo_forms import validate
from .mixins import OptionsMixin
from .meta import ResourceMeta


def include_metadata(f):
    '''
    Paginates and appends Meta data into the json response if in index view
    '''
    def wrapper(self, request, resources, fields, parameters):
        if parameters != None:
            page = self.paginate( request, resources, parameters )
            objects, links = f(self, request, page, fields, parameters)
            meta = self._meta.metadata.generate(request, resources, page, parameters)
            return self.to_json(objects=objects, meta=meta, links=links)
        return f(self, request, resources, fields, parameters)[0]
    return wrapper 


class BaseResource(OptionsMixin):
    '''
    API Resource object
    '''
    class Meta:
        pass

    @classmethod
    def get_views(cls):
        for each in dir(cls):
            if each.startswith('as_') and each.endswith('_view'):
                yield getattr(cls, each)()
    
    def __init__(self, api, routes, version_name=None):
        self.routes = routes
        self.api = api
        self.version_name = version_name
        self._meta = ResourceMeta(self)
        if self._meta.query_form and hasattr(self, 'list'):
            self.list = validate(self._meta.query_form)(self.list)
        if self._meta.create_form and hasattr(self, 'create'):
            self.create = validate(self._meta.create_form)(self.create)
        if self._meta.update_form and hasattr(self, 'update'):
            self.update = validate(self._meta.update_form)(self.update)

    @property
    def tagname(self):
        if self._meta.model:
            return self._meta.model.__name__.lower()
        return self.__class__.__name__.lower()
    
    def handle_request(self, request, **kwargs):
        '''
        Called in every request made to Resource
        '''
        try:
            if request.method not in self.routes:
                return to_http(request, None, status=405)
            method = self.routes[request.method]
            if not hasattr(self, method):
                return HttpResponse(status=405)
            return getattr(self, 'handle_'+method)(request, kwargs)
        except (ObjectDoesNotExist, IOError):
            # ObjectDoesNotExist: if return model instance does not exist
            # IOError: if return file not found
            return HttpResponse(status=404)

    def get_serializer(self, fields):
        '''
        Get JSON builder for the given fields
        '''
        return self._meta.serializer(self.api, fields)

    def handle_response(self, request, response, fields, parameters=None):
        '''
        Proccess response into a JSON serializable object
        '''
        if callable(fields):
            current_fields = fields(self.Meta(), request)
        else:
            current_fields = fields
        status = DEFAULT_STATUS_CODE
        if is_tuple(response):
            status, response = response
        # if is_valuesset(response):
        #     response = self.handle_list_response(
        #         request, list(response), current_fields, parameters)
        if is_queryset(response) or is_valuesset(response):
            response = self.select_related(response, current_fields)
            response = self.handle_queryset_response(
                request, response, current_fields, parameters)
        elif is_modelinstance(response):
            response = self.handle_model_response(response, current_fields)
        elif is_generator(response) or is_list(response):
            response = self.handle_list_response(
                request, response, current_fields, parameters)
        
        if self._meta.uglify:
            response = self.uglify_json(response)
        return to_http(request, response, status)

    @include_metadata
    def handle_queryset_response(self, request, resources, fields, kwargs):
        '''
        Serialize queryset based response
        '''
        builder = self.get_serializer(fields)
        serialized = self.serialize_all( resources, fields, builder )
        return serialized, builder.links

    @include_metadata
    def handle_list_response(self, request, resources, fields, kwargs):
        '''
        Serialize list based response
        '''
        builder = self.get_serializer(fields)
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
        builder = self.get_serializer(fields)
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
                result[JSON_METADATA_KEYNAME] = meta
            if links:
                result[JSON_LINKS_KEYNAME] = links
            return result
        return objects
        
    def paginate(self, request, resources, parameters):
        '''
        Return page of resources according to default or parameter values
        '''
        pagination = self._meta.pagination
        page_objects, page_params = pagination.select(request, resources)
        parameters.update( page_params )
        return page_objects

    def select_related(self, resources, current_fields):
        '''
        Optimize queryset according to current response fields
        '''
        
        def find_related(items, prefix=''):
            for name,fieldtype in items:
                related = prefix + name
                if isinstance(fieldtype, dict):
                    if related in select_related_choices:
                        resources.query.select_related[ related ] = {}
                    else:
                        resources._prefetch_related_lookups.append( related )
                    find_related( fieldtype.iteritems(), related + '__' )
                elif fieldtype.use_in_select_related:
                    resources.query.select_related[ related ] = {}
                elif fieldtype.use_in_prefetch_related:
                    resources._prefetch_related_lookups.append( related )
        
        if self._meta.model:
            if resources.query.select_related:
                return resources
            if resources._prefetch_related_lookups:
                return resources
            resources.query.select_related = {}
            opts = self._meta.model._meta
            select_related_choices = [f.name for f in opts.fields if f.is_relation]
            find_related( current_fields.iteritems() )
        return resources

    def serialize_all(self, resources, fields, builder=None):
        '''
        Serializes each resource (within page) into json
        '''
        if builder == None:
            builder = self.get_serializer(fields)
        return [builder.to_json(i) for i in resources]

    def serialize(self, resource, fields, builder=None, collection=True):
        '''
        Creates json for given resource
        '''
        if builder == None:
            builder = self.get_serializer(fields)
        return builder.to_json(resource, collection)
    
    def uglify_json(self, response):
        response.update(
            uglify_json(response.pop(JSON_OBJECTS_KEYNAME))
        )
        return response
