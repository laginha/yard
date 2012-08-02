#!/usr/bin/env python
# encoding: utf-8

from django.core.exceptions    import ObjectDoesNotExist
from django.core.paginator     import Paginator, EmptyPage
from django.core               import serializers
from django.http               import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from yard.exceptions           import RequiredParamMissing, HttpMethodNotAllowed, InvalidStatusCode
from yard.forms                import Form
from yard.utils                import *
from yard.utils.http           import JsonResponse, FileResponse, HttpResponseUnauthorized
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
    parameters = Parameters = None
    fields = show_fields = index_fields = ()    
    
    class Meta(object):
        pass
    
    class Page(object):
        pass

    def __init__(self, routes):
        self.__routes     = routes # maps http methods with respective views
        self.__meta       = ResourceMeta( self.Meta ) 
        self.__page       = ResourcePage( self.Page )  
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
            else:
                self.__rparameters = parameters
            response = self.__view( method, self.__rparameters )
            fields   = self.index_fields if method=='index' else self.show_fields
            self.builder = JSONbuilder( fields or self.fields )
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
            content, exists = self.__resources_with_meta(response)
            return JsonResponse(content, status=status if exists else 204)
        elif is_modelinstance(response):
            return JsonResponse(self.__resource_to_json(response), status=status)
        elif response == None:
            return HttpResponse(status=status)
        elif is_int(response):
            return HttpResponse(status=response)
        elif is_str(response) or is_dict(response) or is_list(response):
            return JsonResponse(response, status=status) 
        elif is_file(response):
            return FileResponse(response, status=status)        
        elif is_valuesset(response):
            return JsonResponse(list(response), status=status)     
        else:
            return HttpResponse(str(response), status=status)          

    def __resources_with_meta(self, resources):
        '''
        Appends Meta data into the json response
        '''
        page    = self.__paginate( resources )
        objects = self.__resources_to_json( page )
        meta    = self.__meta.fetch(resources, page, self.__rparameters)
        if not meta:
            return objects, page.exists()
        else:
            return {'Objects': objects,'Meta': meta}, page.exists()
    
    def __paginate(self, resources):
        '''
        Return page of resources according to default or parameter values
        '''
        paginated_resources = self.__page.select( self.request, resources )
        self.__rparameters.validated.update( paginated_resources[1] )
        return paginated_resources[0]
    
    def __resources_to_json(self, resources):   
        '''
        Serializes each resource (within page) into json
        '''
        return [self.builder.to_json(i) for i in resources]       

    def __resource_to_json(self, resource):
        '''
        Creates json for given resource
        '''
        return self.builder.to_json(resource)
