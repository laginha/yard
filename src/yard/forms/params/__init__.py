#!/usr/bin/env python
# encoding: utf-8
from django.forms import EmailField
from django.core.exceptions import ValidationError
from yard.exceptions import ConversionError
from yard.utils import is_iter, is_strint
from .base import Parameter
from datetime import datetime, time as Time
import re
import socket
import math


class IntegerParam(Parameter):
    '''
    Parameter for integer values
    '''
    typename = 'integer'
    
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, min_value=None, max_value=None):
        self.max_value = max_value
        self.min_value = min_value
        super(IntegerParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default)
        
    def convert(self, value):
        '''
        Converts to int
        '''
        try:
            return int(value)
        except ValueError:
            raise ConversionError(self, value)

    def validate(self, value):
        if self.max_value != None and self.min_value != None:
            return value >= self.min_value and value <= self.max_value
        elif self.max_value != None:
            return value <= self.max_value
        elif self.min_value != None:
            return value >= self.min_value
        return True

    def get_documentation(self):
        result = super(IntegerParam, self).get_documentation()
        result['maximum'] = self.max_value
        result['minimum'] = self.min_value
        return result      


class PositiveIntegerParam(IntegerParam):
    '''
    Parameter for positive integer values
    '''
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, max_value=None):
        super(PositiveIntegerParam, self).__init__( 
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default, min_value=0, 
            max_value=max_value)
            
    def validate(self, value):
        if self.max_value != None:
            return value <= self.max_value and value >= self.min_value
        return value >= self.min_value


class CharParam(Parameter):
    '''
    Parameter for string/char values
    '''
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, max_length=None, 
                min_length=None):
        self.max_length = max_length
        self.min_length = min_length
        super(CharParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default,)
    
    def convert(self, value):
        return value
    
    def validate(self, value):
        if self.max_length:
            return len(value) <= self.max_length
        return True
        
    def get_documentation(self):
        result = super(CharParam, self).get_documentation()
        if self.max_length:
            result['maxLength'] = self.max_length
        if self.min_length:
            result['minLength'] = self.min_length
        return result


class RegexParam(Parameter):
    '''
    Parameter with regex validation
    '''
    def __init__(self, regex, description=None, alias=None, aliases=None, 
                required=False, default=None):
        # self.regex = r'^%s$'%regex
        self.regex = regex
        self.compiled = re.compile(self.regex)
        super(RegexParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default)
            
    def validate(self, value):
        return self.compiled.match( value )
            
    def convert(self, value):
        return value
        
    def get_documentation(self):
        result = super(RegexParam, self).get_documentation()
        result['pattern'] = self.regex
        return result


class FloatParam(IntegerParam):
    '''
    Parameter for float values
    '''
    typename = 'number'
    
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, min_value=None, max_value=None):
        super(FloatParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default, min_value=min_value,
            max_value=max_value)
        
    def convert(self, value):
        '''
        Converts to float
        '''
        try:
            converted = float(value)
            if math.isnan( converted ):
                raise ConversionError(self, value)
            return converted
        except ValueError:
            raise ConversionError(self, value)


class PositiveFloatParam(FloatParam):
    '''
    Parameter for positive float values
    '''
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, max_value=None):
        super(PositiveFloatParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default, min_value=0, 
            max_value=max_value)
        

class DateTimeParam(Parameter):
    '''
    Parameter for datetime values
    '''
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, default_date=None, 
                validate=None, time_formats=['%H:%M:%S', '%H:%M'],
                formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']):        
        to_iter = lambda x: x if is_iter(x) else [x,]
        self.formats = {'datetime': to_iter( formats )}
        if default_date != None:
            self.default_date = default_date
            self.formats['time'] = to_iter( time_formats )
            if default == None:
                default = self.get_default_date_only
            else:       
                default = self.get_default_with_default_date( default )
        super(DateTimeParam, self).__init__( 
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default, validate=validate)
    
    def get_all_formats(self):
        return [each for value in self.formats.values() for each in value]
    
    def get_default_date_only(self, value):
        if isinstance(value, Time):
            if callable(self.default_date):
                return datetime.combine( self.default_date(), value )
            return datetime.combine( self.default_date, value )
        return value
        
    def get_default_with_default_date(self, default_value):
        def default(value):
            if value == None:
                if callable(default_value):
                    return default_value()
                return default_value
            return self.get_default_date_only(value)
        return default
    
    def get_documentation(self):
        result = super(DateTimeParam, self).get_documentation()
        regex_formats = []
        for each in self.get_all_formats():
            each = re.sub(r'%y|W|U|S|M|m|j|I|H|d', r'\d{2}', each)
            each = re.sub('%Y', r'\d{4}', each)
            each = re.sub('%w', r'\d{1}', each)
            each = re.sub('%p', r'pm|am', each)
            regex_formats.append( r'^' + each + r'$' )
        result['pattern'] = r'|'.join( regex_formats )
        return result
           
    def convert(self, value, to_time=False, to_date=False):
        '''
        Converts to Datetime
        '''
        for key,formats in self.formats.iteritems():
            for each in formats:
                try:
                    dt = datetime.strptime( value, each )
                    if key=='time' or to_time: 
                        return dt.time()
                    elif to_date:
                        return dt.date()
                    else:
                        return dt
                except ValueError as e:
                    continue
        raise ConversionError(self, value)
        

class DateParam(DateTimeParam):
    '''
    Parameter for date values
    '''
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, validate=None, 
                formats=['%Y-%m-%d']):
        super(DateParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default, validate=validate, 
            formats=formats, time_formats=[])

    def convert(self, value):
        '''
        Converts to Date
        '''
        return super(DateParam, self).convert(value, to_date=True)


class TimeParam(DateTimeParam):
    '''
    Parameter for time values
    '''
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, validate=None, 
                formats=['%H:%M:%S', '%H:%M']):
        super(TimeParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default, validate=validate, 
            formats=formats, time_formats=[])

    def convert(self, value):
        '''
        Converts to Time
        '''
        return super(TimeParam, self).convert(value, to_time=True)
        

class BooleanParam(Parameter):
    '''
    Parameter for boolean values
    '''
    typename = 'boolean'
    
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=False):
        super(BooleanParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default, validate=None)
        
    def convert(self, value):
        '''
        Converts to Boolean True or False
        '''
        return False if value.lower() in ['false', 'none'] else (
            bool(int(value)) if is_strint(value) else True
        )

    def get_documentation(self):
        result = super(BooleanParam, self).get_documentation()
        result['enum'] = ['false', 'true']
        return result

        
class ChoiceParam(Parameter):
    '''
    Parameter for single value with pre-defined choices
    '''
    def __init__(self, choices, description=None, alias=None, aliases=None, 
                required=False, default=None):
        self.choices = choices
        super(ChoiceParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default)
            
    def validate(self, value):
        return value in self.choices


class MultipleChoiceParam(Parameter):
    '''
    Parameter for multiple values with pre-defined choices
    '''
    typename = 'array'
    
    def __init__(self, choices, description=None, alias=None, aliases=None, 
                required=False, default=None, sep=','):
        self.sep = sep
        self.choices = choices
        super(MultipleChoiceParam, self).__init__(
             description=description, alias=alias, 
            aliases=aliases, required=required, default=default)
    
    def get_documentation(self):
        result = super(MultipleChoiceParam, self).get_documentation()
        result['pattern'] = r'(.*%s.*)+' %self.seq
        result['items'] = {'type': 'string'}
        return result
    
    def validate(self, value):
        return all(each in self.choices for each in value)
        
    def convert(self, value):
        '''
        Converts to list
        '''
        return [ Parameter.convert(self,i) for i in value.split(self.sep)]


class IpAddressParam(Parameter):
    '''
    Parameter for IP values
    '''
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None):
        super(IpAddressParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default)

    def get_documentation(self):
        result = super(IpAddressParam, self).get_documentation()
        result['pattern'] = r'\d+\.\d+\.\d+\.\d+'
        return result

    def validate(self, value):
        try: 
            return socket.inet_aton( value )
        except socket.error:
            return False

    def convert(self, value):
        return value


class EmailParam(Parameter):
    '''
    Parameter for E-mail values
    '''
    def __init__(self, description=None, alias=None, 
                aliases=None, required=False, default=None):
        super(EmailParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default)    

    def get_documentation(self):
        result = super(IpAddressParam, self).get_documentation()
        result['pattern'] = r'.+@.+'
        return result

    def validate(self, value):
        try:
            return EmailField().clean(value)
        except ValidationError:
            return False

    def convert(self, value):
        return value
        
        
class InstanceParam(Parameter):
    '''
    Parameter for model instances
    '''
    typename = 'integer'
    
    def __init__(self, model, model_attribute='pk', description=None, 
                alias=None, aliases=None, required=False, default=None):
        self.model = model.objects
        self.model_attribute = model_attribute
        super(InstanceParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default)
        
    def convert(self, value):
        try:
            instance = self.model.filter( **{self.model_attribute: value} )
            if instance.exists():
                return instance[0]
            raise ConversionError(self, value)
        except ValueError:
            raise ConversionError(self, value)


class TimestampParam(Parameter):
    '''
    Parameter for timestamp values
    '''
    typename = 'integer'
          
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, validate=None):     
        super(TimestampParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default, validate=validate)
    
    def convert(self, value):
        try:
            converted = float(value)
            if math.isnan( converted ):
                 raise ConversionError(self, value)
            return datetime.fromtimestamp( converted )
        except ValueError:
            raise ConversionError(self, value)


class CommaSeparatedValueParam(RegexParam):
    '''
    Parameter for comma seperated values
    '''
    REGEX = r'^.+$|^.+,.+$'
    
    def __init__(self, description=None, alias=None, 
                aliases=None, required=False, default=None):
        super(CommaSeparatedValueParam, self).__init__(
            regex=self.REGEX, description=description, alias=alias, 
            aliases=aliases, required=required, default=default)
 
    def convert(self, value):
        return [each for each in value.split(',')]
 

class CommaSeparatedIntegerParam(CommaSeparatedValueParam):
    '''
    Parameter for comma seperated integers
    '''
    REGEX = r'^[0-9]+$|^[0-9]+,[0-9]+$'
    
    def convert(self, value):
        try:
            return [int(each) for each in value.split(',')]
        except ValueError:
            raise ConversionError(self, value)
    