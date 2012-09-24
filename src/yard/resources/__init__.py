#!/usr/bin/env python
# encoding: utf-8

from django.conf               import settings
from django.core.exceptions    import ObjectDoesNotExist
from django.core.paginator     import Paginator, EmptyPage
from django.core               import serializers
from django.http               import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from yard.exceptions           import RequiredParamMissing, HttpMethodNotAllowed, InvalidStatusCode
from yard.forms                import Form
from yard.utils                import *
from yard.utils.http           import ProperJsonResponse, JsonResponse, FileResponse, HttpResponseUnauthorized, JsonDebugResponse
from yard.resources.parameters import ResourceParameters
from yard.resources.builders   import JSONbuilder
from yard.resources.templates  import ServerErrorTemplate
from yard.resources.meta       import ResourceMeta
from yard.resources.page       import ResourcePage
import json, mimetypes



class Resource(object):
    '''
    API Resource object
    '''
    parameters = None
    Parameters = None
    fields       = ()
    show_fields  = ()
    index_fields = ()    
    
    class Meta(object):
        pass
    
    class Page(object):
        pass

    def __init__(self, routes):
        if not hasattr(settings, 'YARD_DEBUG'):
            yard_debug = 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG==True
            self.JsonClassResponse = JsonDebugResponse if yard_debug else ProperJsonResponse
        else:
            self.JsonClassResponse = JsonDebugResponse if settings.YARD_DEBUG else ProperJsonResponse
        self.__routes     = routes # maps http methods with respective views
        self.__meta       = ResourceMeta( self.Meta )
        self.__page       = ResourcePage( self.page if hasattr(self, 'page') else self.Page )  
        self.index_fields = self.index_fields if self.index_fields else self.fields
        self.show_fields  = self.show_fields  if self.show_fields else self.fields
        self.parameters   = self.parameters() if self.parameters else (
                            self.Parameters() if self.Parameters else None )
  
    def __call__(self, request, **parameters):
        '''
        Called in every request made to Resource
        '''
        try:
            self.request = request
            method = self.__method()
            if method == 'index':
                self.__rparameters = self.__resource_parameters( parameters )
                self.builder = self.__get_builder(self.index_fields, self.__rparameters)
            elif method == 'show':
                self.__rparameters = parameters
                self.builder = self.__get_builder(self.show_fields, self.__rparameters)
            else:
                self.__rparameters = parameters
                self.builder = self.__get_builder(self.fields, self.__rparameters)
            response = self.__view( method, self.__rparameters )
            self.JsonResponse = self.JsonClassResponse( request )
            return self.__response( response )    
        except HttpMethodNotAllowed:
            # if http_method not allowed for this resource
            return HttpResponseNotFound()
        except RequiredParamMissing as e:
            # if required param missing from request
            return HttpResponseBadRequest()
        except AttributeError as e:
            # if view not implemented
            return HttpResponseNotFound(str(e))
        except ObjectDoesNotExist:
            # if return model instance does not exist
            return HttpResponseNotFound()
        except IOError:
            # if return file not found
            return HttpResponseNotFound()
        except InvalidStatusCode as e:
            # status code given is not int
            return ServerErrorTemplate(e)

    def __method(self):
        '''
        Checks if http_method within possible routes
        '''
        http_method = self.request.method.lower()
        if http_method not in self.__routes:
            raise HttpMethodNotAllowed( http_method )
        return self.__routes[http_method]
    
    def __resource_parameters(self, parameters):
        '''
        Gets parameters from resource request
        '''
        resource_params = ResourceParameters( parameters )
        if self.parameters:
            for i in self.parameters.get( self.request ):
                resource_params.update( i )
        return resource_params
    
    def __get_builder(self, fields, parameters):
        if callable(fields):
            self.current_fields = fields(self.__rparameters)
            return JSONbuilder( self.current_fields )
        self.current_fields = fields
        return JSONbuilder( self.current_fields )
    
    def __view(self, method, parameters):
        '''
        Runs desired view according to method
        '''
        view = getattr( self, method )
        if method in ['show', 'update', 'destroy']:
            return view( parameters.pop('id'), **parameters ) 
        elif method == 'create':
            return view( **parameters )
        return view( parameters )
    
    def __response(self, response, status=200):
        '''
        Returns a HttpResponse according to given response
        '''
        if is_tuple(response) and len(response)>1:
            if is_int(response[0]):
                status = response[0]
            else:
                raise InvalidStatusCode(response[0])
            response = response[1]
        elif is_httpresponse(response):
            return response
            
        if is_queryset(response):
            response = self.select_related(response)
            content  = self.__queryset_with_meta(response)
            return self.JsonResponse(content, status=status)
        elif is_modelinstance(response):
            content = self.serialize(response)
            return self.JsonResponse(content, status=status)
        elif is_generator(response) or is_list(response):
            content = self.__list_with_meta(response)
            return self.JsonResponse(content, status=status)             
        elif response == None:
            return HttpResponse(status=status)
        elif is_int(response):
            return HttpResponse(status=response)
        elif is_str(response) or is_dict(response):
            return self.JsonResponse(response, status=status) 
        elif is_file(response):
            return FileResponse(response, status=status)        
        elif is_valuesset(response):
            content = self.__list_with_meta(list(response))
            return self.JsonResponse(content, status=status)
        else:
            return HttpResponse(str(response), status=status)

    def select_related(self, resources):
        '''
        Optimize queryset according to current response fields
        '''
        related_models = [i[0] for i in self.current_fields if isinstance(i, tuple)]
        return resources.select_related( *related_models )

    def __queryset_with_meta(self, resources):
        '''
        Appends Meta data into the json response
        '''
        page    = self.__paginate( resources )
        objects = self.serialize_all( page )
        meta    = self.__meta.fetch(resources, page, self.__rparameters)
        return objects if not meta else {'Objects': objects,'Meta': meta}
    
    def __list_with_meta(self, resources):
        '''
        Appends Meta data into list based response
        '''
        page = self.__paginate( resources )
        meta = self.__meta.fetch(resources, page, self.__rparameters)
        return page if not meta else {'Objects': page,'Meta': meta}
    
    def __paginate(self, resources):
        '''
        Return page of resources according to default or parameter values
        '''
        paginated_resources = self.__page.select( self.request, resources )
        self.__rparameters.validated.update( paginated_resources[1] )
        return paginated_resources[0]
    
    def serialize_all(self, resources):   
        '''
        Serializes each resource (within page) into json
        '''
        return [self.builder.to_json(i) for i in resources]       

    def serialize(self, resource):
        '''
        Creates json for given resource
        '''
        return self.builder.to_json(resource)
        
        