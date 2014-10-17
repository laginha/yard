#!/usr/bin/env python
# encoding: utf-8
from yard.forms.parameter import Parameter
from yard.utils           import is_serializable


class ResourceParameters(dict):
    '''
    Dictionary with given resource parameters values
    '''   
    def __init__(self, params={}):
        self.dict_of_errors = {}
        self.path = params
        self.validated = {}
        self.update( params )

    def update(self, params, hide=False):
        '''
        Updates parameters
        '''
        for key,value in params.iteritems():
            if isinstance(value, Exception):
                self.dict_of_errors[key] = unicode(value)
            elif isinstance(key, Parameter):
                self.validated[key.name] = value if is_serializable(value) else unicode(value)
                if key.aliases != None:
                    for each in key.aliases:
                        self[each] = value
                else:
                    self[key.alias] = value
            else:
                self[key] = value
                if not hide:
                    self.validated[key] = value if is_serializable(value) else unicode(value)
    
    def from_path(self):
        '''
        Returns parameters of type path
        '''
        return self.path
        
    def from_query(self):
        '''
        Returns parameters of type query
        '''
        return dict( [(k,v) for k,v in self.items() if k not in self.path] )
    
    def is_valid(self):
        '''
        Were there any errors while processing the parameters
        '''
        return not bool(self.dict_of_errors)

    def errors(self):
        '''
        Returns JSON with evaluated errors 
        '''
        return {'Errors': self.dict_of_errors if self.dict_of_errors else {}}

