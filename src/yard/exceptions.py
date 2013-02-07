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


class MethodNotImplemented(Exception):
    '''
    For when a Http method is not implemented in a resource
    '''
    def __init__(self, method):
        self.method = method

    def __str__(self):
        return "Method '%s' not implemented" %self.method


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


class AndParameterException(Exception):
    '''
    For when not all parameters within an AND are not met/validated
    '''
    alias = 'ApiException'
    
    def __init__(self, params):
        self.params = params
    
    def __nonzero__(self):
        return False
    
    def __str__(self):
        if len(self.params) == 1:
            text = "'%s'" %self.params[0]
        else:
            _lambda = lambda a,b: "%s, '%s'"%(a,b)
            text = reduce(_lambda, self.params[1:-1], "'%s'" %self.params[0])
            text += " and '%s'" %self.params[-1]
        return "Parameters %s cannot be used aloned" %text
            

class NoMeta(Exception):
    '''
    For when no meta is desired for the QuerySet based json-response
    '''
    pass


class VersionException(Exception):
    '''
    For when no default nor latest resource version is given
    '''
    def __str__(self):
        return "No default nor latest version known"
