#!/usr/bin/env python
# encoding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator  import Paginator, EmptyPage
from django.core            import serializers
from utils                  import *
from utils.exceptions       import RequiredParamMissing
from utils.http_responses   import JsonResponse, HttpResponse, HttpResponseUnauthorized, HttpResponseNotFound
import json


class Resource(object):
    parameters  = ()
    fields      = ()
    
    
    def __init__(self, routes):
        def build_json_tree(field, resource=None):
            '''
            pre-build a json according to the given fields
            '''
            if is_tuple( field ):     
                
                # if it is a resource-field with sub-fields (x,(y,z))
                if len( field ) == 2 and is_str( field[0] ) and is_tuple( field[1] ): #known issue here
                    resource = lambda x: getattr( x, field[0], None )
                    # recursive: go into sub-fields
                    value    = build_json_tree( field[1], resource )
                    return ( field[0], value ) 
                    
                # if sub-fields (y,z)
                else:
                    # recursive: go into fields
                    results  = [ build_json_tree(f, resource) for f in field ]
                    # filter non-existing fields
                    filtered = filter(lambda x: x and is_tuple( x ), results)
                    return dict( filtered )  
            
            elif is_str( field ):
                
                # if field is sub-field
                if resource:
                    lambda_ = lambda x: getattr( resource(x), field, '' )
                # if first-level field
                else:
                    lambda_ = lambda x: getattr( x, field, '' )
                return ( field, lambda_ )
        
        json_tree   = build_json_tree( self.fields )
        # make sure json_tree is a dictinary
        self.tree   = json_tree if is_dict( json_tree ) else dict(json_tree if is_list(json_tree) else [json_tree])
        self.routes = routes # maps http methods with respective views

    
    def __call__(self, request, **parameters):
        http_method = request.method.lower()
        # check if http_method within possible routes
        if http_method not in self.routes:
            return HttpResponseNotFound()
        
        method = self.routes[http_method]
        if method == 'index':
               
            try:
                # get params from request according to the given parameters attribute
                params = self.fetch_params( request )
                for param in params:
                    parameters.update( param )
            except RequiredParamMissing as e:
                # if required param missing from request
                return HttpResponseUnauthorized( str(e) )
        
        try:
            view     = getattr( self, method )
            # Run desired view
            response = view( request, parameters['id'] ) if method in ['show', 'update', 'destroy'] else (
                view( request ) if method == 'create' else view( request, parameters )
            )
        except AttributeError:
            # if view not implemented
            return HttpResponseNotFound()
        
        # return a http compliant response
        return self.respond( response )


    def respond(self, response, status=200):
        '''
        Return a HttpResponse according to given response
        '''
        if is_tuple(response) and len(response)>1:
            if is_int(response[0]):
                status = response[0]
            response = response[1]
              
        if is_httpresponse(response): return response                     
        elif is_queryset(response): return JsonResponse(self.resources_to_json(response), status=status)
        elif is_modelinstance(response): return JsonResponse(self.resource_to_json(response), status=status)
        elif response == None: return HttpResponse(status=status)
        elif is_int(response): return HttpResponse(status=response)
        elif is_str(response): return HttpResponse(response, status=status)                
        elif is_valuesset(response): return JsonResponse(list(response), status=status)          
        elif is_dict(response) or is_list(response): return JsonResponse(response, status=status)      
        else: return response          


    def resources_to_json(self, resources):   
        '''
        Serialize each resource into json
        '''       
        return [ self.resource_to_json(i) for i in resources ]


    def resource_to_json(self, resource, tree=None):
        '''
        Use pre-calculated json_tree to create json for given resource
        '''
        if not tree:
            tree = self.tree
        dict_ = {}
        for k,v in tree.items():        
            value = self.resource_to_json( resource, v ) if is_dict( v ) else v( resource )
            if not value: 
                continue
            # if field is a model instance method
            elif is_method(value):
                result = value()
                # expect for a valuesQuerySet, querySet, dict, list or unicoded value
                dict_[ k ] = list( result ) if is_valuesset(result) else (
                    [unicode(i) for i in result] if is_queryset(result) else (
                        result if is_dict(result) or is_list(result) else unicode(result)
                    )
                )
            else:
                dict_[ k ] = value if is_dict(value) else unicode(value)
        return dict_


    def fetch_params(self, request):
        '''
        Get values from request according to specified parameters attribute
        '''
        def limits_(param, request):
            '''validate param value through param limit key'''
            lambda_ = param.get( 'limit', lambda x: x)
            value   = request.GET.get( param['name'] )
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


