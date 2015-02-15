#!/usr/bin/env python
# encoding: utf-8
from yard.utils import is_strfloat, is_strint
from yard.utils.swagger import build_swagger_parameter
from yard.exceptions import (
    RequiredParamMissing, InvalidParameterValue, 
    ConversionError, AndParameterException,)
import inspect


class Parameter(object):
    '''
    Parent class to all Form's parameter types
    '''    
    typename = 'string'
    
    def __init__(self, description='', help_text='', alias=None, aliases=None,
                 validate=None, default=None, required=False, 
                 ignore_invalids=False):
        self.alias           = alias
        self.aliases         = aliases
        if not hasattr(self, 'validate'):
            self.validate    = validate
        self.default         = default
        self.required        = required
        self.ignore_invalids = ignore_invalids
        self.name            = None
        self.description     = description
        self.help_text       = help_text
    
    def __str__(self):
        return self.name if self.name else self.typename
    
    def __or__(self, other):
        '''
        Called when parameter is joined with another parameter 
        through boolean 'or'
        '''
        return OR(other, self)

    def __and__(self, other):
        '''
        Called when parameter is joined with another parameter 
        through boolean 'and'
        '''
        return AND(self, other)
        
    def get_documentation(self):
        def get_default():
            if self.default:
                if callable(self.default):
                    if not inspect.getargspec(self.default).args:
                        return self.default()
                return self.default
            
        return build_swagger_parameter(
            location = 'query', name = self.name, typename = self.typename,
            description = self.description, required = self.required,
            default = get_default()
        )

    def convert(self, value):
        '''
        Converts value into float or int
        '''
        return float(value) if is_strfloat(value) else (
            int(value) if is_strint(value) else value )

    def get_value(self, request):
        '''
        Gets value from request
        '''
        value = request.GET.get( self.name )
        return None if value==None else self.convert(value)

    def get_default(self, value):
        '''
        Returns/transforms value according to default value/function
        '''
        is_default = True
        if self.default==None:
            if value==None and self.required:
                raise RequiredParamMissing(self)
            return value, not is_default
        elif callable(self.default):
            if inspect.getargspec(self.default).args:
                return self.default( value ), is_default
        elif value!=None:
            return value, not is_default
        if callable(self.default):
            return self.default(), is_default 
        return self.default, is_default

    def do_validate(self, value):
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
                self.alias = self.alias or k

    def get_value_and_info(self, request):
        '''
        Handles a normal/single param 
        (returns value and if it is default or not)
        '''
        is_default = False
        try:
            value = self.get_value( request )
            value, is_default = self.get_default( value )
            value = self.do_validate( value )
        except (ConversionError, InvalidParameterValue, 
                RequiredParamMissing) as e:
            return {self.name: e}, is_default
        if value!=None:
            return {self: value}, is_default 
        return {}, is_default
        
    def get(self, request):
        '''
        Handles a normal/single param (returns only value)
        '''
        value, is_default = self.get_value_and_info(request)
        return value


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
    def get_value_and_info(self, request):
        '''
        Handles params banded together with OR
        '''
        for param in self.__dict__.values():
            value, is_default = param.get_value_and_info( request )
            # returns the first valid value
            if value: return value, is_default
        return {}, False
        
    def get(self, request):
        value, is_default = self.get_value_and_info( request )
        return value

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
        
    def get_value_and_info(self, request):
        together, are_default = {}, []
        for param in self.__dict__.values():
            value, is_default = param.get_value_and_info( request )
            if value:
                together.update( value )
                are_default.append( is_default )
        all_defaults = all(are_default)
        if len(together)==self.size():
            # returns params's values if all valid
            return together, all_defaults
        if not together or all_defaults: 
            # ignore if all values are the default
            return {}, all_defaults
        # return exception otherwise
        params = []
        for k,v in together.iteritems():
            if isinstance(v, AndParameterException):
                params += v.params  
            else:
                params.append( k )
        exception = AndParameterException( params )
        return {self.__str__(): exception}, False
        
    def get(self, request):
        '''
        Handles params banded together with AND
        '''
        value, is_default = self.get_value_and_info( request )
        return value

    def __str__(self):
        return '( %s and %s )' %(self.x, self.y)
