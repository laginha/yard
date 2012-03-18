#!/usr/bin/env python
# encoding: utf-8

# Inspired byhttp://djangosnippets.org/snippets/1071/

from django.core.paginator  import Paginator, EmptyPage
from django.core            import serializers
from utils                  import *
from utils.exceptions       import RequiredParamMissing
from utils.http_responses   import JsonResponse, HttpResponse, HttpResponseUnauthorized, HttpResponseNotFound
import json


class Resource(object):
    parameters  = ()
    fields = ()
    
    def __init__(self, routes):
        def build_json_tree(field, resource=None):
            if is_tuple( field ):     
                if len( field ) == 2 and is_str( field[0] ) and is_tuple( field[1] ): #known issue here
                    resource = lambda x: getattr( x, field[0], None )
                    value    = build_json_tree( field[1], resource )
                    return ( field[0], value ) 
                else:
                    results  = [ build_json_tree(f, resource) for f in field ]
                    filtered = filter(lambda x: x and is_tuple( x ), results)
                    return dict( filtered )       
            elif is_str( field ):
                if resource:
                    lambda_ = lambda x: unicode( getattr( resource(x), field, '' ) ) 
                else:
                    lambda_ = lambda x: unicode( getattr( x, field, '' ) )
                return ( field, lambda_ )
        
        json_tree   = build_json_tree( self.fields )
        if is_dict( json_tree ):
            self.tree = json_tree
        else:
            self.tree   = dict(  json_tree if is_list(json_tree) else [json_tree]  )
        self.routes = routes

    
    def __call__(self, request, **parameters):
        http_method = request.method.lower()
        if http_method not in self.routes:
            return HttpResponseNotFound()
        
        method = self.routes[http_method]
        if method == 'index':   
            try:
                params = self.fetch_params( request )
                for param in params:
                    parameters.update( param )
            except RequiredParamMissing as e:
                return HttpResponseUnauthorized( str(e) )
        
        try:
            view     = getattr( self, method )
            response = view( request, parameters['id'] ) if method in ['show', 'update', 'destroy'] else (
                view( request ) if method == 'create' else view( request, parameters )
            )
        except AttributeError:
            return HttpResponseNotFound()
        
        return self.respond( response )


    def respond(self, response):
        return HttpResponse() if not response else (
            JsonResponse( self.serialize(response) ) if is_queryset(response) else response
        )


    def serialize(self, resources):   
        def build_json_response( tree, resource ):
            dict_ = {}
            for k,v in tree.items():        
                value = build_json_response( v, resource ) if is_dict( v ) else v( resource )
                if value:
                    dict_[ k ] = value
            return dict_
        
        return [ build_json_response(self.tree, i) for i in resources ]
        
    
    def fetch_params(self, request):
        def limits_(param, request):
            lambda_ = param.get( 'limit', lambda x: x)
            value   = request.GET.get( param['name'] )
            try:
                return lambda_( float(value) ) if is_float( value ) else (
                    lambda_( int(value) ) if is_int( value ) else lambda_( value )
                )
            except ValueError:
                return
            except TypeError:
                return
        
        def next_(param, request):
            return or_( param['or'], request ) if param.has_key('or') else (
                and_( param['and'], request ) if param.has_key('and') else solo_( param, request )
            )

        def solo_(param, request):
            value = limits_( param, request )
            key   = param.get('alias') or param['name']
            if not value and param.get('required', False):
                raise RequiredParamMissing( key ) 
            return {key: value} if value else {}

        def and_(params, request):
            together = {}
            if is_tuple( params ):   
                for param in params:
                    value = next_( param, request )
                    together.update( value  ) 
            return together if len(together)==len(params) else {}

        def or_(params, request): 
            if is_tuple( params ):
                for param in params:
                    value = next_( param, request )
                    if value: return value
            return {}
        
        for param in self.parameters:  
            if isinstance( param, dict ):
                yield next_( param, request )


