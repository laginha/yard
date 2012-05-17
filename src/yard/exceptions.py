#!/usr/bin/env python
# encoding: utf-8


class InvalidStatusCode(Exception):
    '''
    For when view returns an invalid status code
    '''
    def __init__(self, status):
        self.status = status
    
    def __str__(self):
        return "Http status code '%s' is not valid. Only int allowed." %self.status


class HttpMethodNotAllowed(Exception):
    '''
    For when http method is not allowed for given url or resource
    ''' 
    def __init__(self, method):
        self.method = method
    
    def __str__(self):
        return "Http method %s not allowed." %self.method


class RequiredParamMissing(Exception):
    '''
    For when a required resource parameter is not in request
    '''   
    def __init__(self, param):
        self.param = param
        
    def __nonzero__(self):
        return False

    def __str__(self):
        return "Required parameter missing from request."
 
      
class InvalidParameterValue(Exception):
    '''
    For when a parameter value fails the validate test
    '''
    def __init__(self, param, value):
        self.value = value
        self.param = param
    
    def __nonzero__(self):
        return False
    
    def __str__(self):
        return "Query value '%s' failed %s validation." %(self.value, self.param.__class__.__name__)


class ConversionError(Exception):
    '''
    For when a parameter value could not be properly converted
    '''
    def __init__(self, param, value):
        self.value = value
        self.param = param
    
    def __nonzero__(self):
        return False

    def __str__(self):
        return "Query value '%s' for %s could not be converted properly." %(self.value, self.param.__class__.__name__)


class NoMeta(Exception):
    '''
    For when no meta is desired for the QuerySet based json-response
    '''
    pass
