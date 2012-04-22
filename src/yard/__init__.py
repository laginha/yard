#!/usr/bin/env python
# encoding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator  import Paginator, EmptyPage
from django.core            import serializers
from django.http            import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from yard.http              import JsonResponse, FileResponse, HttpResponseUnauthorized
from yard.utils.builders    import JSONbuilder
from yard.exceptions        import RequiredParamMissing, HttpMethodNotAllowed, InvalidStatusCode
from yard.utils.templates   import ServerErrorTemplate
from yard.utils             import *
import json, mimetypes


class Resource(object):
    parameters  = ()
    fields      = ()    
    
    def __init__(self, routes):
        self.json   = JSONbuilder(self.fields)
        self.routes = routes # maps http methods with respective views
  
    def __call__(self, request, **parameters):
        try:
            method = self.__method( request )
            if method == 'index':
                self.__fetch( request, parameters )
            response = self.__view( request, method, parameters )
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

    def __method(self, request):
        '''
        Check if http_method within possible routes
        '''
        http_method = request.method.lower()
        if http_method not in self.routes:
            raise HttpMethodNotAllowed( http_method )
        return self.routes[http_method]
    
    def __fetch(self, request, parameters):
        '''
        Get paramters from request
        '''
        for i in self.parameters.get( request ):
            parameters.update( i )
    
    def __view(self, request, method, parameters):
        '''
        Run desired view according to method
        '''
        view = getattr( self, method )
        if method in ['show', 'update', 'destroy']:
            return view( request, parameters.pop('id'), **parameters ) 
        elif method == 'create':
            return view( request, **parameters )
        return view( request, parameters )
    
    
    def __response(self, response, status=200):
        '''
        Return a HttpResponse according to given response
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
            return JsonResponse(self.__resources_to_json(response), status=status)
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


    def __resources_to_json(self, resources):   
        '''
        Serialize each resource into json
        '''
        return [self.json(i) for i in resources]       


    def __resource_to_json(self, resource):
        '''
        Create json for given resource
        '''
        return self.json(resource)
