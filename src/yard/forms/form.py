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
            self.__logic__ = self.__attributes['__logic__']
            if is_tuple( self.__logic__ ):
                self.__set_names( self.__logic__ )
            elif isinstance(self.__logic__, Parameter):
                self.__logic__ = (self.__logic__,)
                self.__set_names( self.__logic__ )
        else:
            self.__logic__ = [p for n,p in self.__attributes.items() if n not in ('__module__', '__doc__')]
            self.__set_names( self.__logic__ )
    
    def __str__(self):
        return ' + '.join( [str(param) for param in self.__logic__] )

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
        for param in self.__logic__:
            yield param.get(request)

