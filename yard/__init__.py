#!/usr/bin/env python
# encoding: utf-8

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
                    lambda_ = lambda x: unicode( getattr( resource(x), field, '' ) ) 
                # if first-level field
                else:
                    lambda_ = lambda x: unicode( getattr( x, field, '' ) )
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


    def respond(self, response):
        '''
        Return a HttpResponse according to given response
        '''
        return HttpResponse() if not response else (
            JsonResponse( self.serialize(response) ) if is_queryset(response) else response
        )


    def serialize(self, resources):   
        '''
        Serialize resources into json
        '''
        def build_json_response( tree, resource ):
            '''Use pre-calculated json_tree to create json for given resource'''
            dict_ = {}
            for k,v in tree.items():        
                value = build_json_response( v, resource ) if is_dict( v ) else v( resource )
                if value:
                    dict_[ k ] = value
            return dict_
        
        # build json for each resource
        return [ build_json_response(self.tree, i) for i in resources ]
        
    
    def fetch_params(self, request):
        '''
        Get values from request according to specified parameters attribute
        '''
        def limits_(param, request):
            '''validate param value through param limit key'''
            lambda_ = param.get( 'limit', lambda x: x)
            value   = request.GET.get( param['name'] )
            try:
                # tries to convert value into float or int before passing it through limit
                return lambda_( float(value) ) if is_float( value ) else (
                    lambda_( int(value) ) if is_int( value ) else lambda_( value )
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


