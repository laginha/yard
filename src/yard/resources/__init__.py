#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from yard.exceptions import HttpMethodNotAllowed, InvalidStatusCode, MethodNotImplemented, RequiredParamMissing
from yard.utils import is_tuple, is_queryset, is_modelinstance, is_generator, is_list, is_valuesset
from yard.utils.http import to_http
from yard.forms import Form
from yard.resources.utils import *


DEFAULT_STATUS_CODE = getattr(settings, 'DEFAULT_STATUS_CODE', 200)


class Resource(object):
    '''
    API Resource object
    '''

    class Meta(object):
        pass

    class Pagination(object):
        pass

    def __init__(self, api, routes):
        self._api         = api
        self.__routes     = routes # maps http methods with respective views
        self.__meta       = ResourceMeta( self.Meta )
        self.__pagination = ResourcePage( self.Pagination )
        self.__parameters = Form( self.Parameters ) if hasattr(self, "Parameters") else None
        self.fields       = self.__get_fields()
        self.index_fields = self.index_fields if hasattr(self, "index_fields") else self.fields
        self.show_fields  = self.show_fields  if hasattr(self, "show_fields") else self.fields
        self.__meta.page_class = self.__pagination #TEMPORARY

    def __get_fields(self):
        if hasattr(self, "fields"):
            return self.fields
        elif not hasattr(self, "model"):
            return {}
        return model_to_fields(self.model)
    
    def __call__(self, request, **parameters):
        '''
        Called in every request made to Resource
        '''
        try:
            method = self.__method( request )
            return getattr(self, 'handle_'+method)(request, parameters)
        except (HttpMethodNotAllowed, MethodNotImplemented, ObjectDoesNotExist, IOError):
            # HttpMethodNotAllowed: if http_method not allowed for this resource
            # MethodNotImplemented: if view not implemented
            # ObjectDoesNotExist: if return model instance does not exist
            # IOError: if return file not found
            return HttpResponse(status=404)
        except RequiredParamMissing :
            # if required param missing from request
            return HttpResponse(status=403)

    def __method(self, request):
        '''
        Checks if http_method within possible routes
        '''
        if request.method not in self.__routes:
            raise HttpMethodNotAllowed(request.method)
        return self.__routes[request.method]

    def __resource_parameters(self, request, parameters):
        '''
        Gets parameters from resource request
        '''
        resource_params = ResourceParameters( parameters )
        if self.__parameters:
            for i in self.__parameters.get( request ):
                resource_params.update( i )
        return resource_params

    def __get_builder(self, fields, parameters):
        if callable(fields):
            current_fields = fields(parameters)
            return JSONbuilder( self._api, current_fields ), current_fields
        return JSONbuilder( self._api, fields ), fields

    def __handle_response(self, request, response, current_fields, resource_parameters, builder):
        '''
        Proccess response into a JSON serializable object
        '''
        status = DEFAULT_STATUS_CODE
        if is_tuple(response):
            status, response = response
        if is_queryset(response):
            response = self.select_related(response, current_fields)
            response = self.__queryset_with_meta(request, response, resource_parameters, builder)
        elif is_modelinstance(response):
            response = self.__serialize(response, builder)
        elif is_generator(response) or is_list(response):
            response = self.__list_with_meta(request, response, resource_parameters, builder)
        elif is_valuesset(response):
            response = self.__list_with_meta(request, list(response), resource_parameters)
        return to_http(request, response, status)
        
    def select_related(self, resources, current_fields):
        '''
        Optimize queryset according to current response fields
        '''
        related_models = [k for k,v in current_fields.iteritems() if isinstance(v, dict)]
        return resources.select_related( *related_models )

    def queryset_with_meta(self, request, resources, resource_parameters, builder):
        '''
        Appends Meta data into the json response
        '''
        if hasattr(resource_parameters, 'validated'):
            page = self.__paginate( request, resources, resource_parameters )
            objects = self.__serialize_all( page, builder )
            meta = self.__meta.fetch(request, resources, page, resource_parameters)
            return objects if not meta else {'Objects': objects,'Meta': meta}
        return self.__serialize_all( resources, builder )

    def __list_with_meta(self, request, resources, resource_parameters, builder):
        '''
        Appends Meta data into list based response
        '''
        if hasattr(resource_parameters, 'validated'):
            page = self.__paginate( request, resources, resource_parameters )
            objects = [self.__serialize(i, builder) if is_modelinstance(i) else i for i in page]
            meta = self.__meta.fetch(request, resources, page, resource_parameters)
            return objects if not meta else {'Objects': objects,'Meta': meta}
        return [self.__serialize(i, builder) if is_modelinstance(i) else i for i in resources]

    def __paginate(self, request, resources, resource_parameters):
        '''
        Return page of resources according to default or parameter values
        '''
        page_resources, page_parameters = self.__pagination.select( request, resources )
        resource_parameters.validated.update( page_parameters )
        return page_resources

    def __serialize_all(self, resources, builder):
        '''
        Serializes each resource (within page) into json
        '''
        return [builder.to_json(i) for i in resources]

    def serialize_all(self, resources, fields):
        builder = JSONbuilder( self._api, fields )
        return self.__serialize_all( resources, builder )

    def __serialize(self, resource, builder):
        '''
        Creates json for given resource
        '''
        return builder.to_json(resource)

    def serialize(self, resource, fields):
        builder = JSONbuilder( self._api, fields )
        return self.__serialize( resource, builder )
         
    #
    # HTTP verbs
    #
    
    @method_required('index')
    def handle_index(self, request, parameters):
        parameters = self.__resource_parameters( request, parameters )
        response = self.index(request, parameters)
        builder, current_fields = self.__get_builder(self.index_fields, parameters)
        return self.__handle_response(request, response, current_fields, parameters, builder)
    
    @method_required('show')
    def handle_show(self, request, parameters):
        response = self.show(request, parameters.pop('pk'), **parameters)
        builder, fields = self.__get_builder(self.show_fields, parameters)
        return self.__handle_response(request, response, fields, parameters, builder)
    
    @method_required('create')
    def handle_create(self, request, parameters):
        response = self.create(request, **parameters)
        builder, fields = self.__get_builder(self.fields, parameters)
        return self.__handle_response(request, response, fields, parameters, builder)
    
    @method_required('update')    
    def handle_update(self):
        response = self.update(request, parameters.pop('pk'), **parameters)
        builder, fields = self.__get_builder(self.fields, parameters)
        return self.__handle_response(request, response, fields, parameters, builder)
    
    @method_required('destroy')
    def handle_destroy(self, request, parameters):
        response = self.destroy(request, parameters.pop('pk'), **parameters)
        builder, fields = self.__get_builder(self.fields, parameters)
        return self.__handle_response(request, response, fields, parameters, builder)
    
    @method_required('options')
    def handle_options(self, request, parameters):
        response = self.options(request, **parameters)
        builder, fields = self.__get_builder(self.fields, parameters)
        response = self.__handle_response(request, response, fields, parameters, builder)
        response['Allow'] = ','.join([k for k,v in self.__routes.items() if hasattr(self, v)])
        return response
        
    def options(self, request, **parameters):
        return 200
