#!/usr/bin/env python
# encoding: utf-8
from yard.exceptions           import HttpMethodNotAllowed, InvalidStatusCode, MethodNotImplemented
from yard.utils                import *
from yard.resources.parameters import ResourceParameters
from yard.resources.builders   import JSONbuilder
from yard.resources.meta       import ResourceMeta
from yard.resources.page       import ResourcePage
from yard.resources            import fields as yardFields
from yard.forms                import Form


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
        return dict(
            [ (i.name, yardFields.get_field(i)) 
                for i in self.model._meta.fields if i.name not in ['mymodel_ptr']]
        )
    
    def __call__(self, request, **parameters):
        '''
        Called in every request made to Resource
        '''
        try:
            method = self.__method( request )
            return getattr(method)(request, parameters)
        except HttpMethodNotAllowed:
            # if http_method not allowed for this resource
            return HttpResponseNotFound()
        except RequiredParamMissing as e:
            # if required param missing from request
            return HttpResponseBadRequest()
        except MethodNotImplemented as e:
            # if view not implemented
            return HttpResponseNotFound()
        except ObjectDoesNotExist:
            # if return model instance does not exist
            return HttpResponseNotFound()
        except IOError:
            # if return file not found
            return HttpResponseNotFound()
            

    def __method(self, request):
        '''
        Checks if http_method within possible routes
        '''
        http_method = request.method.lower()
        if http_method not in self.__routes:
            raise HttpMethodNotAllowed( http_method )
        return self.__routes[http_method]

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

    def __response(self, request, response, current_fields, resource_parameters, builder):
        '''
        Proccess response into a JSON serializable object
        '''
        if is_queryset(response):
            response = self.select_related(response, current_fields)
            return self.__queryset_with_meta(request, response, resource_parameters, builder)
        elif is_modelinstance(response):
            return self.__serialize(response, builder)
        elif is_generator(response) or is_list(response):
            return self.__list_with_meta(request, response, resource_parameters, builder)
        elif is_valuesset(response):
            return self.__list_with_meta(request, list(response), resource_parameters)
        return response

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
    
    def __index(self, request, parameters):
        parameters = self.__resource_parameters( request, parameters )
        builder, current_fields = self.__get_builder(self.index_fields, parameters)
        response = self.index(request, parameters)
        return self.__response(request, response, current_fields, parameters, builder)
    
    def index(self, request, params):
        raise MethodNotImplemented()


    def __show(self, request, parameters):
        builder, fields = self.__get_builder(self.show_fields, parameters)
        response = self.show(request, parameters.pop('pk'), **parameters)
        return self.__response(request, response, fields, parameters, builder)
    
    def show(self, request, obj_id):
        raise MethodNotImplemented()
    
    
    def __create(self, request, parameters):
        builder, fields = self.__get_builder(self.fields, parameters)
        response = self.create(request, **parameters)
        return self.__response(request, response, fields, parameters, builder)
    
    def create(self, request, parameters):
        raise MethodNotImplemented()
      
        
    def __update(self):
        builder, fields = self.__get_builder(self.fields, parameters)
        response = self.update(request, parameters.pop('pk'), **parameters)
        return self.__response(request, response, fields, parameters, builder)
        
    def update(self, request, obj_id):
        raise MethodNotImplemented()
    
    
    def __destroy(self, request, parameters):
        builder, fields = self.__get_builder(self.fields, parameters)
        response = self.destroy(request, parameters.pop('pk'), **parameters)
        return self.__response(request, response, fields, parameters, builder)
        
    def destroy(self, request, obj_id):
        raise MethodNotImplemented()
    
    
    def __options(self, request, parameters):
        builder, fields = self.__get_builder(self.fields, parameters)
        response = self.options(request, **parameters)
        return self.__response(request, response, fields, parameters, builder)
    
    def options(self, request):
        raise MethodNotImplemented()
