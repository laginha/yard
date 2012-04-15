#!/usr/bin/env python
# encoding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator  import Paginator, EmptyPage
from django.core            import serializers
from django.http            import HttpResponse, HttpResponseNotFound, HttpResponseServerError
from yard.utils             import *
from yard.utils.builders    import JSONbuilder
from yard.utils.exceptions  import RequiredParamMissing, HttpMethodNotAllowed, InvalidStatusCode
from yard.http              import JsonResponse, FileResponse, HttpResponseUnauthorized
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
                self.__update( request, parameters )
            response = self.__view( request, method, parameters )
            return self.__response( response )
        
        except HttpMethodNotAllowed:
            # if http_method not allowed for this resource
            return HttpResponseNotFound( str(e) )
        except RequiredParamMissing as e:
            # if required param missing from request
            return HttpResponseUnauthorized( str(e) )
        except AttributeError as e:
            # if view not implemented
            return HttpResponseNotFound()
        except ObjectDoesNotExist:
            # if return model instance does not exist
            return HttpResponseNotFound()
        except IOError:
            # if return file not found
            return HttpResponseNotFound()
        except InvalidStatusCode as e:
            return HttpResponseServerError(str(e))


    def __method(self, request):
        '''
        Check if http_method within possible routes
        '''
        http_method = request.method.lower()
        if http_method not in self.routes:
            raise HttpMethodNotAllowed( http_method )
        return self.routes[http_method]
    
    
    def __update(self, request, parameters):
        '''
        Get params from request according to the given parameters attribute
        '''
        params = self.__fetch_params( request )
        for param in params:
            parameters.update( param )
    
    
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


    def __fetch_params(self, request):
        '''
        Get values from request according to specified parameters attribute
        '''
        def limits_(param, request):
            '''validate param value through param limit key'''
            lambda_ = param.get( 'limit' )
            value   = request.GET.get( param['name'] )
            
            if not lambda_: return value
            if not value: return None
                
            try:
                # tries to convert value into float or int before passing it through limit
                return lambda_( float(value) ) if is_strfloat( value ) else (
                    lambda_( int(value) ) if is_strint( value ) else lambda_( value )
                )
            except ValueError:
                return
            except TypeError:
                return
        
        def next_(param, request):
            '''redirect param whether it is single or banded together with AND/OR'''
            return or_( param['or'], request ) if param.has_key('or') else (
                and_( param['and'], request ) if param.has_key('and') else solo_( param, request )
            )

        def solo_(param, request):
            '''handle a normal/single param'''
            value = limits_( param, request )
            key   = param.get('alias') or param['name']
            if not value and param.get('required', False):
                # raise exception if value not valid of required param
                raise RequiredParamMissing( key ) 
            return {key: value} if value else {}

        def and_(params, request):
            '''handle params banded together with AND'''
            together = {}
            if is_tuple( params ):   
                for param in params:
                    value = next_( param, request )
                    together.update( value  )
            # returns params's values if all valid
            return together if len(together)==len(params) else {}

        def or_(params, request): 
            '''handle params banded together with OR'''
            if is_tuple( params ):
                for param in params:
                    value = next_( param, request )
                    # returns the first valid value
                    if value: return value
            return {}
        
        # for each parameter
        for param in self.parameters:  
            if is_dict( param ):
                yield next_( param, request )


