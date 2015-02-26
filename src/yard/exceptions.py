#!/usr/bin/env python
# encoding: utf-8

class NoResourceMatch(Exception):
    '''
    For API has no resource for a given model
    '''
    def __init__(self, model):
        self.model = model
    
    def __str__(self):
        return "No resource found for model '%s'" %self.model


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


class NoDefaultVersion(Exception):
    '''
    For when no default version was defined
    '''
    def __str__(self):
        return "Default version unknown"

class NoModelError(Exception):
    def __str__(self):
        return "Resource related model unknown"
        