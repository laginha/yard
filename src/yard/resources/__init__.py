#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from yard.exceptions import HttpMethodNotAllowed, MethodNotImplemented, RequiredParamMissing
from yard.utils import is_tuple, is_queryset, is_modelinstance, is_generator, is_list, is_valuesset, is_dict
from yard.utils.http import to_http
from yard.forms import Form
from yard.resources.utils import *


DEFAULT_STATUS_CODE = getattr(settings, 'DEFAULT_STATUS_CODE', 200)


class Resource(object):
    '''
    API Resource object
    '''
    
    def __init__(self, api, routes):

        def get_class_attribute(name):
            return getattr(self, name, type(name, (), {}))
            
        def get_allowed_methods():
            return [k for k,v in self.__routes.items() if k!="OPTIONS" and hasattr(self, v)]

        def get_fields():
            return self.fields if hasattr(self, "fields") else (
                model_to_fields(self.model) if hasattr(self, "model") else {} )

        def get_json_builders():
            fields = [self.index_fields, self.show_fields, self.fields]
            return { id(i): JSONbuilder(self._api, i) for i in fields if not callable(i) }
            
        def get_parameters():
            parameters = Form( self.Parameters ) if hasattr(self, "Parameters") else None
            if not parameters:
                self.__get_resource_parameters = lambda r,p: ResourceParameters( p )
            return parameters
            
        # 'Public' attributes
        self._api         = api
        self._pagination  = ResourcePage( get_class_attribute('Pagination') )
        self._meta        = ResourceMeta( get_class_attribute('Meta'), self._pagination )
        self.fields       = get_fields()
        self.index_fields = getattr(self, "index_fields", self.fields)
        self.show_fields  = getattr(self, "show_fields", self.fields)
        self.description  = getattr(self, "description", "not provided")
        # 'Private' attributes
        self.__routes          = routes
        self.__parameters      = get_parameters()
        self.__builders        = get_json_builders()
        self.__allowed_methods = get_allowed_methods()
    
    @classmethod
    def has_any_method(self, routes):
        '''
        Check if Resource has any http method implemented
        '''
        return any([hasattr(self, i) for i in routes if i!='options'])
    
    def __call__(self, request, **parameters):
        '''
        Called in every request made to Resource
        '''
        try:
            if request.method not in self.__routes:
                return to_http(request, status=404)
            method = self.__routes[request.method]
            return getattr(self, 'handle_'+method)(request, parameters)
        except (MethodNotImplemented, ObjectDoesNotExist, IOError):
            # MethodNotImplemented: if view not implemented
            # ObjectDoesNotExist: if return model instance does not exist
            # IOError: if return file not found
            return HttpResponse(status=404)
        except RequiredParamMissing :
            # if required param missing from request
            return HttpResponse(status=403)

    def __get_resource_parameters(self, request, parameters):
        '''
        Gets parameters from resource request
        '''
        resource_params = ResourceParameters( parameters )
        for i in self.__parameters.get( request ):
            resource_params.update( i )
        return resource_params

    def __get_builder(self, fields):
        '''
        Get JSONbuilder for the given fields
        '''
        return self.__builders[ id(fields) ] or JSONbuilder( self._api, fields )

    def __handle_response(self, request, response, fields, parameters):
        '''
        Proccess response into a JSON serializable object
        '''
        current_fields = fields(parameters) if callable(fields) else fields
        status = DEFAULT_STATUS_CODE
        if is_tuple(response):
            status, response = response
        if is_valuesset(response):
            response = self.__handle_list(request, list(response), parameters, current_fields)
        elif is_queryset(response):
            response = self.select_related(response, current_fields)
            response = self.__handle_queryset(request, response, parameters, current_fields)
        elif is_modelinstance(response):
            response = self.serialize(response, current_fields)
        elif is_generator(response) or is_list(response):
            response = self.__handle_list(request, response, parameters, current_fields)
        return to_http(request, response, status)

    @with_pagination_and_meta
    def __handle_queryset(self, request, resources, parameters, fields):
        '''
        Serialize queryset based response
        '''
        return self.serialize_all( resources, fields )

    @with_pagination_and_meta
    def __handle_list(self, request, resources, parameters, fields):
        '''
        Serialize list based response
        '''
        return [self.serialize(i, fields) if is_modelinstance(i) else i for i in resources]

    def _paginate(self, request, resources, parameters):
        '''
        Return page of resources according to default or parameter values
        '''
        page_resources, page_parameters = self._pagination.select( request, resources )
        parameters.validated.update( page_parameters )
        return page_resources

    def select_related(self, resources, current_fields):
        '''
        Optimize queryset according to current response fields
        '''
        related_models = [k for k,v in current_fields.iteritems() if isinstance(v, dict)]
        return resources.select_related( *related_models )

    def serialize_all(self, resources, fields):
        '''
        Serializes each resource (within page) into json
        '''
        return [self.__get_builder(fields).to_json(i) for i in resources]

    def serialize(self, resource, fields):
        '''
        Creates json for given resource
        '''
        return self.__get_builder(fields).to_json(resource)
    
    @method_required('index')
    def handle_index(self, request, parameters):
        parameters = self.__get_resource_parameters( request, parameters )
        response = self.index(request, parameters)
        return self.__handle_response(request, response, self.index_fields, parameters)
    
    @method_required('show')
    def handle_show(self, request, parameters):
        response = self.show(request, parameters.pop('pk'), **parameters)
        return self.__handle_response(request, response, self.show_fields, parameters)
    
    @method_required('create')
    def handle_create(self, request, parameters):
        response = self.create(request, **parameters)
        return self.__handle_response(request, response, self.fields, parameters)
    
    @method_required('update')    
    def handle_update(self):
        response = self.update(request, parameters.pop('pk'), **parameters)
        return self.__handle_response(request, response, self.fields, parameters)
    
    @method_required('destroy')
    def handle_destroy(self, request, parameters):
        response = self.destroy(request, parameters.pop('pk'), **parameters)
        return self.__handle_response(request, response, self.fields, parameters)
    
    @method_required('options')
    def handle_options(self, request, parameters):
        response = self.options(request, **parameters)
        response = self.__handle_response(request, response, self.fields, parameters)
        response['Allow'] = self.allowed_methods
        return response
    
    def options(self, request, **parameters):
        return 200
