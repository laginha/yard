#!/usr/bin/env python
# encoding: utf-8

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

