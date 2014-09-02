#!/usr/bin/env python
# encoding: utf-8
from yard.utils           import is_tuple
from yard.forms.parameter import Parameter


class Form(object):
    '''
    Form for acceptable Resource parameters
    '''
    
    def __init__(self, parameters):
        self.__attributes = parameters.__dict__
        if '__logic__' in self.__attributes:
            self.logic = self.__attributes['__logic__']
            if is_tuple( self.logic ):
                self.__set_names( self.logic )
            elif isinstance(self.logic, Parameter):
                self.logic = (self.logic,)
                self.__set_names( self.logic )
        else:
            self.logic = self.params
            self.__set_names( self.logic )
    
    def __str__(self):
        return ' + '.join( [str(param) for param in self.logic] )        

    @property
    def params(self):
        return [p for n,p in self.__attributes.items() if isinstance(p, Parameter)]

    def __set_names(self, params):
        '''
        Sets name attribute for all parameters in __logic__
        '''
        for param in params:
            param.set_name( self.__attributes )        

    def get(self, request):
        '''
        Gets and validates parameters values in request
        '''
        for param in self.logic:
            yield param.get(request)
