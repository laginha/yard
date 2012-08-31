#!/usr/bin/env python
# encoding: utf-8

from yard.utils      import is_strfloat, is_strint
from yard.exceptions import RequiredParamMissing, InvalidParameterValue, ConversionError, AndParameterException
import inspect


class Parameter(object):
    '''
    Parent class to all Form's parameter types
    '''    
    def __init__(self, alias=None, validate=None, default=None, required=False, ignore_invalids=False):
        self.alias           = alias
        self.validate        = validate
        self.default         = default
        self.required        = required
        self.ignore_invalids = ignore_invalids
        self.name            = None
    
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
        self.is_default = False
        if self.default==None:
            if value==None and self.required:
                raise RequiredParamMissing(self)
            return value
        elif callable(self.default) and inspect.getargspec(self.default).args:
            self.is_default = True
            return self.default( value )
        elif value!=None:
            return value
        else:
            self.is_default = True
            if callable(self.default):
                return self.default()
            return self.default

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
            together.update( value )
        if len(together)==self.size():
            # returns params's values if all valid
            return together
        if all([i.is_default if isinstance(i, Parameter) else False for i in together]):
            # ignore if all values are the default
            return {}
        # return exception otherwise
        exception = AndParameterException( together.keys() )
        result    = {exception.alias: exception}
        for k,v in together.iteritems():
            if isinstance(v, Exception): 
                result.update( {k:v} )
        return result

    def __str__(self):
        return '( %s and %s )' %(self.x, self.y)
