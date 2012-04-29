#!/usr/bin/env python
# encoding: utf-8

from yard.utils           import is_tuple
from yard.forms.parameter import Parameter


class Form(object):
    def __init__(self):
        self.__attributes = self.__class__.__dict__ 
        if hasattr(self, 'logic'):
            if is_tuple( self.logic ):
                self.__set_names( self.logic )
            elif isinstance(self.logic, Parameter):
                self.logic = (self.logic,)
                self.__set_names( self.logic )
        else:
            self.logic = [p for n,p in self.__attributes.items() if n not in ('__module__', '__doc__')]
            self.__set_names( self.logic )
        
    def __str__(self):
        return ' + '.join( [str(param) for param in self.logic] )

    def __set_names(self, params):
        for param in params:
            param.set_name( self.__attributes )        

    def get(self, request):
        for param in self.logic:
            yield param.get(request)

