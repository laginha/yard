#!/usr/bin/env python
# encoding: utf-8

from yard.utils      import is_strfloat, is_strint, is_tuple, is_list, is_str, is_int, is_float
from yard.exceptions import RequiredParamMissing
import re


class Form(object):
    def __init__(self):
        self.__attributes = self.__class__.__dict__ 
        if hasattr(self, 'logic'):
            if is_tuple( self.logic ):
                self.__set_names( self.logic )
                print self
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
            x = param.get( request ) 
            print x
            yield x
    
    

class Parameter(object):
    def __init__(self, alias=None, validate=None, default=None, required=False):
        self.alias    = alias
        self.validate = validate
        self.default  = default
        self.required = required
        self.name     = None

    def __or__(self, other):
        return OR(other, self)

    def __and__(self, other):
        return AND(self, other)
        
    def __str__(self):
        return self.name or 'None'
        
    def convert(self, value):
        '''
        tries to convert value into float or int
        '''
        return float(value) if is_strfloat(value) else (
            int(value) if is_strint(value) else value )
    
    def __value(self, request):
        value = request.GET.get( self.name )  
        if not value: 
            return  
        return self.convert(value)
        
    def __default(self, value):
        '''
        validate param value through param limit key
        '''
        if not self.default:
            return value
        return self.default(value) if value and callable(self.default) else (
            value if value else self.default
        )    
    
    def __validate(self, value):
        '''
        validate param value through param limit key
        '''
        if not self.validate: 
            return value          
        return value if value and self.validate( value ) else None
    
    def set_name(self, params):
        for k,v in params.items():
            if v==self:
                self.name  = k
                self.alias = self.alias if self.alias else k

    def get(self, request):
        '''
        handle a normal/single param
        '''
        value = self.__value( request )
        value = self.__validate( self.__default(value) )
        if not value and self.required:
            # raise exception if value of required param is not valid
            raise RequiredParamMissing( self.alias ) 
        return {self.alias: value} if value else {}
        
        
class Logic(Parameter):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        length = 0
        for i in self.__dict__.values():
            length += len(i) if isinstance(i, Logic) else 1
        return length

    def set_name(self, params):
        for i in self.__dict__.values():
            i.set_name( params )


class OR(Logic):
    def get(self, request):
        '''
        handle params banded together with OR
        '''
        for param in self.__dict__.values():
            value = param.get( request )
            # returns the first valid value
            if value: return value
        return {}

    def __str__(self):
        return '( %s or %s )' %(self.x, self.y)


class AND(Logic):
    def get(self, request):
        '''
        handle params banded together with AND
        '''
        together = {}
        for param in self.__dict__.values():
            value = param.get( request )
            together.update( value  )
        # returns params's values if all valid
        return together if len(together)==len(self) else {}

    def __str__(self):
        return '( %s and %s )' %(self.x, self.y)

