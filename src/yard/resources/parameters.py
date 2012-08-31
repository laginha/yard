#!/usr/bin/env python
# encoding: utf-8
from yard.forms.parameter import Parameter


class ResourceParameters(dict):
    '''
    Dictionary with given resource parameters values
    '''   
    def __init__(self, params={}):
        self.__errors  = {}
        self.__path    = params
        self.validated = {}
        self.update( params )

    def update(self, params, hide=False):
        '''
        Updates parameters
        '''
        for key,value in params.iteritems():
            if isinstance(value, Exception):
                self.__errors[key] = unicode(value)
            elif isinstance(key, Parameter):
                self[key.alias] = value
                self.validated[key.name] = unicode(value)
            else:
                self[key] = value
                if not hide:
                    self.validated[key] = unicode(value)
    
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
        return {'Errors': self.__errors if self.__errors else {}}

