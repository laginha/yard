#!/usr/bin/env python
# encoding: utf-8

from yard.utils      import is_strfloat, is_strint
from yard.exceptions import RequiredParamMissing, InvalidParameterValue, ConversionError, AndParameterException


class Parameter(object):
    '''
    Parent class to all Form's parameter types
    '''    
    def __init__(self, alias=None, validate=None, default=None, required=False, ignore_invalids=False):
        for k,v in locals().items():
            #set attributes dynamically
            setattr(self, k, v) if k != 'self' else None
        self.name     = None
    
    def __str__(self):
        return self.name if self.name else type(self)
    
    def __or__(self, other):
        '''
        Called when parameter is joined with another parameter through boolean 'or'
        '''
        return OR(other, self)

    def __and__(self, other):
        '''
        Called when parameter is joined with another parameter through boolean 'and'
        '''
        return AND(self, other)

    def convert(self, value):
        '''
        Converts value into float or int
        '''
        return float(value) if is_strfloat(value) else (
            int(value) if is_strint(value) else value )

    def _value(self, request):
        '''
        Gets value from request
        '''
        value = request.GET.get( self.name )
        return None if value==None else self.convert(value)

    def _default(self, value):
        '''
        Returns/transforms value according to default value/function
        '''
        if self.default==None:
            if value==None and self.required:
                raise RequiredParamMissing(self)
            return value
        return self.default(value) if callable(self.default) else (
            value if value!=None else self.default
        )    

    def _validate(self, value):
        '''
        Validates param value
        '''
        if not self.validate or value==None or self.validate(value):
            return value
        raise InvalidParameterValue(self, value)          

    def set_name(self, params):
        '''
        Sets name and alias attribute
        '''
        for k,v in params.items():
            if v==self:
                self.name  = k
                self.alias = self.alias if self.alias else k

    def get(self, request):
        '''
        Handles a normal/single param
        '''
        try:
            value = self._value( request )
            value = self._default( value )
            value = self._validate( value )
        except (ConversionError, InvalidParameterValue, RequiredParamMissing) as e:
            return {self.name: e}
        return {self: value} if value!=None else {}


class Logic(Parameter):
    '''
    Relates two parameters through boolean logic
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        '''
        Number of Parameters within
        '''
        length = 0
        for i in self.__dict__.values():
            length += len(i) if isinstance(i, Logic) else 1
        return length

    def set_name(self, params):
        '''
        Sets name attribute of Parameters within
        '''
        for i in self.__dict__.values():
            i.set_name( params )


class OR(Logic):
    '''
    Relates two parameters through boolean 'or'
    '''  
    def get(self, request):
        '''
        Handles params banded together with OR
        '''
        for param in self.__dict__.values():
            value = param.get( request )
            # returns the first valid value
            if value: return value
        return {}

    def __str__(self):
        return '( %s or %s )' %(self.x, self.y)


class AND(Logic):
    '''
    Relates two parameters through boolean 'and'
    '''
    
    def size(self):
        '''
        Number of AND Parameters within
        '''
        length = 0
        for i in self.__dict__.values():
            length += i.size() if isinstance(i, AND) else 1
        return length
       
    def get(self, request):
        '''
        Handles params banded together with AND
        '''
        together = {}
        for param in self.__dict__.values():
            value = param.get( request )
            together.update( value  )
        if not together:
            return {}
        if len(together)==self.size():
            # returns params's values if all valid
            return together
        # return exception otherwise
        exception = AndParameterException( together.keys() )
        result    = {exception.alias: exception}
        for k,v in together.iteritems():
            if isinstance(v, Exception): result.update( {k:v} )
        return result

    def __str__(self):
        return '( %s and %s )' %(self.x, self.y)


