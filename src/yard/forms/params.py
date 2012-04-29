#!/usr/bin/env python
# encoding: utf-8

from django.contrib.gis.geos import Point
from yard.forms.parameter    import Parameter
from yard.exceptions         import InvalidParameterValue, ConversionError
from yard.utils              import is_iter, is_strint
from datetime                import datetime
import re


class IntegerParam(Parameter):
    '''
    Parameter for integer values
    '''
    def __init__(self, alias=None, required=False, default=None, min=None, max=None):
        if max!=None and min!=None:
            validate = lambda x: x>=min and x<= max
        elif max!=None:
            validate = lambda x: x<=max
        elif min!=None:
            validate = lambda x: x>=min
        else:
            validate = None
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
        
    def convert(self, value):
        '''
        Converts to int
        '''
        try:
            return int(value)
        except ValueError:
            raise ConversionError(self, value)


class PositiveIntegerParam(IntegerParam):
    '''
    Parameter for positive integer values
    '''
    def __init__(self, alias=None, required=False, default=None, max=None):
        IntegerParam.__init__(self, alias=alias, required=required, default=default, min=0, max=max)


class CharParam(Parameter):
    '''
    Parameter for string/char values
    '''
    def __init__(self, alias=None, required=False, default=None, max_length=None):
        validate = None if not max_length else (lambda x: len(x) <= max_length)
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
    
    def convert(self, value):
        return value


class RegexParam(Parameter):
    '''
    Parameter with regex validation
    '''
    def __init__(self, regex, alias=None, required=False, default=None):
        validate = lambda x: re.findall(r'^%s$'%regex, x)
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
    
    def convert(self, value):
        return value


class FloatParam(IntegerParam):
    '''
    Parameter for float values
    '''
    def __init__(self, alias=None, required=False, default=None, min=None, max=None):
        IntegerParam.__init__(self, alias=alias, required=required, default=default, min=min, max=max)
        
    def convert(self, value):
        '''
        Converts to float
        '''
        try:
            return float(value)
        except ValueError:
            raise ConversionError(self, value)


class PositiveFloatParam(FloatParam):
    '''
    Parameter for positive float values
    '''
    def __init__(self, alias=None, required=False, default=None, max=None):
        FloatParam.__init__(self, alias=alias, required=required, default=default, min=0, max=max)
        

class DateTimeParam(Parameter):
    '''
    Parameter for datetime values
    '''
    def __init__(self, alias=None, required=False, default=None, validate=None,
                 formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']):
        self.formats = formats if is_iter(formats) else [formats,]
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
    
    def convert(self, value, to_time=False, to_date=False):
        '''
        Converts to Datetime
        '''
        for format in self.formats:
            try:
                dt = datetime.strptime( value, format )
                return dt.time() if to_time else(
                    dt.date() if to_date else dt ) 
            except ValueError as e:
                continue 
        raise ConversionError(self, value)
        

class DateParam(DateTimeParam):
    '''
    Parameter for date values
    '''
    def __init__(self, alias=None, required=False, default=None, validate=None, formats=['%Y-%m-%d']):
        DateTimeParam.__init__(self, alias=alias, required=required, default=default, validate=validate, formats=formats)

    def convert(self, value):
        '''
        Converts to Date
        '''
        return DateTimeParam.convert(self, value, to_date=True)


class TimeParam(DateTimeParam):
    '''
    Parameter for time values
    '''
    def __init__(self, alias=None, required=False, default=None, validate=None, formats=['%H:%M:%S', '%H:%M']):
        DateTimeParam.__init__(self, alias=alias, required=required, default=default, validate=validate, formats=formats)

    def convert(self, value):
        '''
        Converts to Time
        '''
        return DateTimeParam.convert(self, value, to_time=True)
        

class BooleanParam(Parameter):
    '''
    Parameter for boolean values
    '''
    def __init__(self, alias=None, required=False, default=True):
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=None)
        
    def convert(self, value):
        '''
        Converts to Boolean True or False
        '''
        return False if value.lower() in ['false', 'none'] else (
            bool(int(value)) if is_strint(value) else True
        )

        
class ChoiceParam(Parameter):
    '''
    Parameter for single value with pre-defined choices
    '''
    def __init__(self, choices, alias=None, required=False, default=None):
        validate = lambda x: x in choices
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)


class MultipleChoiceParam(Parameter):
    '''
    Parameter for multiple values with pre-defined choices
    '''
    def __init__(self, choices, alias=None, required=False, default=None, sep=','):
        self.sep = sep
        validate = lambda x: all([i in choices for i in x])
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
        
    def convert(self, value):
        '''
        Converts to list
        '''
        return [ Parameter.convert(self,i) for i in value.split(self.sep)]


class PointParam(Parameter):
    '''
    Parameter for point values
    '''
    def __init__(self, alias=None, required=False, default=None, validate=None):
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)        

    def convert(self, value):
        '''
        Converts to Point
        '''
        try:
            lng, lat = value.split(',')
            return Point(float(lng), float(lat))
        except ValueError:
            raise ConversionError(self, value)
