#!/usr/bin/env python
# encoding: utf-8

from yard.utils      import is_strfloat, is_strint
from yard.exceptions import RequiredParamMissing, InvalidParameterValue, ConversionError



class Parameter(object):
    def __init__(self, alias=None, validate=None, default=None, required=False, ignore_invalids=False):
        for k,v in locals().items():
            #set attributes dynamically
            setattr(self, k, v) if k != 'self' else None
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
            if not value and self.required:
                raise RequiredParamMissing(self)
            return value
        return self.default(value) if value and callable(self.default) else (
            value if value else self.default
        )    

    def __validate(self, value):
        '''
        validate param value through param limit key
        '''
        if not self.validate or value and self.validate(value):
            return value
        raise InvalidParameterValue(self, value)          

    def set_name(self, params):
        for k,v in params.items():
            if v==self:
                self.name  = k
                self.alias = self.alias if self.alias else k

    def get(self, request):
        '''
        handle a normal/single param
        '''
        try:
            value = self.__value( request )
            value = self.__default( value )
            value = self.__validate( value )
        except (ConversionError, InvalidParameterValue, RequiredParamMissing) as e:
            return {self.name: e}
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


