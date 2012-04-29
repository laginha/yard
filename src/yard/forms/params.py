#!/usr/bin/env python
# encoding: utf-8

from django.contrib.gis.geos import Point
from yard.forms.parameter    import Parameter
from yard.exceptions         import InvalidParameterValue, ConversionError
from yard.utils              import is_iter, is_strint
from datetime                import datetime
import re


class IntegerParam(Parameter):
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
        try:
            return int(value)
        except ValueError:
            raise ConversionError(self, value)


class PositiveIntegerParam(IntegerParam):
    def __init__(self, alias=None, required=False, default=None, max=None):
        IntegerParam.__init__(self, alias=alias, required=required, default=default, min=0, max=max)


class CharParam(Parameter):
    def __init__(self, alias=None, required=False, default=None, max_length=None):
        validate = None if not max_length else (lambda x: len(x) <= max_length)
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
    
    def convert(self, value):
        return value


class RegexParam(Parameter):
    def __init__(self, regex, alias=None, required=False, default=None):
        validate = lambda x: re.findall(r'^%s$'%regex, x)
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
    
    def convert(self, value):
        return value


class FloatParam(IntegerParam):
    def __init__(self, alias=None, required=False, default=None, min=None, max=None):
        IntegerParam.__init__(self, alias=alias, required=required, default=default, min=min, max=max)
        
    def convert(self, value):
        try:
            return float(value)
        except ValueError:
            raise ConversionError(self, value)


class PositiveFloatParam(FloatParam):
    def __init__(self, alias=None, required=False, default=None, max=None):
        FloatParam.__init__(self, alias=alias, required=required, default=default, min=0, max=max)
        

class DateTimeParam(Parameter):
    def __init__(self, alias=None, required=False, default=None, validate=None,
                 formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']):
        self.formats = formats if is_iter(formats) else [formats,]
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
    
    def convert(self, value, to_time=False, to_date=False):
        for format in self.formats:
            try:
                dt = datetime.strptime( value, format )
                return dt.time() if to_time else(
                    dt.date() if to_date else dt ) 
            except ValueError as e:
                continue 
        raise ConversionError(self, value)
        

class DateParam(DateTimeParam):
    def __init__(self, alias=None, required=False, default=None, validate=None, formats=['%Y-%m-%d']):
        DateTimeParam.__init__(self, alias=alias, required=required, default=default, validate=validate, formats=formats)

    def convert(self, value):
        return DateTimeParam.convert(self, value, to_date=True)


class TimeParam(DateTimeParam):
    def __init__(self, alias=None, required=False, default=None, validate=None, formats=['%H:%M:%S', '%H:%M']):
        DateTimeParam.__init__(self, alias=alias, required=required, default=default, validate=validate, formats=formats)

    def convert(self, value):
        return DateTimeParam.convert(self, value, to_time=True)
        

class BooleanParam(Parameter):
    def __init__(self, alias=None, required=False, default=True):
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=None)
        
    def convert(self, value):
        return False if value.lower() in ['false', 'none'] else (
            bool(int(value)) if is_strint(value) else True
        )

        
class ChoiceParam(Parameter):
    def __init__(self, choices, alias=None, required=False, default=None):
        validate = lambda x: x in choices
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)


class MultipleChoiceParam(Parameter):
    def __init__(self, choices, alias=None, required=False, default=None, sep=','):
        self.sep = sep
        validate = lambda x: all([i in choices for i in x])
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
        
    def convert(self, value):
        return [ Parameter.convert(self,i) for i in value.split(self.sep)]


class PointParam(Parameter):
    def __init__(self, alias=None, required=False, default=None, validate=None):
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)        

    def convert(self, value):
        try:
            lng, lat = value.split(',')
            return Point(float(lng), float(lat))
        except ValueError:
            raise ConversionError(self, value)
