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
from yard.meta              import ResourceMeta
from yard.forms             import Form
import json, mimetypes


class ResourceParameters(dict):
    '''
    Dictionary with given resource parameters values
    '''   
    def __init__(self, params={}):
        self.__errors   = {}
        self.__path     = params
        self.with_names = {}
        self.update( params )

    def update(self, params):
        '''
        Updates parameters
        '''
        for key,value in params.iteritems():
            if value:
                self[key.alias] = value
                self.with_names[key.name] = value
            else:
                self.__errors[key] = str(value)
    
    def from_path(self):
        '''
        Returns parameters of type path
        '''
        return self.__path
        
    def from_query(self):
        '''
        Returns parameters of type query
        '''
        return dict( [(k,v) for k,v in self.items() if k not in self.__path] )
    
    def is_valid(self):
        '''
        Were there any errors while processing the parameters
        '''
        return not bool(self.__errors)

    def errors(self):
        '''
        Returns JSON with evaluated errors 
        '''
        return {'ERRORS': self.__errors} if self.__errors else {}


class Resource(object):
    '''
    API Resource object
    '''
    parameters  = None
    fields      = ()    
    
    class Meta(object):
        pass

    def __init__(self, routes):
        self.json   = JSONbuilder(self.fields)
        self.routes = routes # maps http methods with respective views
        self._meta  = ResourceMeta( self.Meta() )   
  
    def __call__(self, request, **parameters):
        '''
        Called in every request made to Resource
        '''
        try:
            method = self.__method( request )
            if method == 'index':
                self.rparameters = self.__resource_parameters( request, parameters )
            else:
                self.rparameters = parameters
            response = self.__view( request, method, self.rparameters )
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
        Checks if http_method within possible routes
        '''
        http_method = request.method.lower()
        if http_method not in self.routes:
            raise HttpMethodNotAllowed( http_method )
        return self.routes[http_method]
    
    def __resource_parameters(self, request, parameters):
        '''
        Gets parameters from resource request
        '''
        resource_params = ResourceParameters( parameters )
        if self.parameters:
            for i in self.parameters.get( request ):
                resource_params.update( i )
        return resource_params
    
    def __view(self, request, method, parameters):
        '''
        Runs desired view according to method
        '''
        view = getattr( self, method )
        if method in ['show', 'update', 'destroy']:
            return view( request, parameters.pop('id'), **parameters ) 
        elif method == 'create':
            return view( request, **parameters )
        return view( request, parameters )
       
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
            return JsonResponse(self.__resources_with_meta(response), status=status)
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
        meta    = self._meta.fetch(resources, self.rparameters)
        objects = self.__resources_to_json(resources)
        return objects if not meta else {
            'Objects': objects,
            'Meta':    meta,
        }

    def __resources_to_json(self, resources):   
        '''
        Serializes each resource into json
        '''
        return [self.json(i) for i in resources]       

    def __resource_to_json(self, resource):
        '''
        Creates json for given resource
        '''
        return self.json(resource)
