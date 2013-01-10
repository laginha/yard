#!/usr/bin/env python
# encoding: utf-8

from django.forms            import EmailField
from yard.forms.parameter    import Parameter
from yard.exceptions         import InvalidParameterValue, ConversionError
from yard.utils              import is_iter, is_strint
from datetime                import datetime, time as Time
import re, socket, math

try:
    from django.contrib.gis.geos import Point
except ImportError:
    import sys
    sys.stdout.write("Warning: Could not find the GEOS library.\n")


class IntegerParam(Parameter):
    '''
    Parameter for integer values
    '''
    def __init__(self, alias=None, required=False, default=None, min_value=None, max_value=None):
        if max_value!=None and min_value!=None:
            validate = lambda x: x>=min_value and x<= max_value
        elif max_value!=None:
            validate = lambda x: x<=max_value
        elif min_value!=None:
            validate = lambda x: x>=min_value
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
    def __init__(self, alias=None, required=False, default=None, min_value=0, max_value=None):
        if max_value!=None:
            validate = lambda x: x<=max_value and x>=max(min_value, 0)
        else:
            validate = lambda x: x>=max(min_value, 0)
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)


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
    def __init__(self, alias=None, required=False, default=None, min_value=None, max_value=None):
        IntegerParam.__init__(self, alias=alias, required=required, default=default, min_value=min_value, max_value=max_value)
        
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
    def __init__(self, alias=None, required=False, default=None, max_value=None):
        FloatParam.__init__(self, alias=alias, required=required, default=default, min_value=0, max_value=max_value)
        

class DateTimeParam(Parameter):
    '''
    Parameter for datetime values
    '''
    def __init__(self, alias=None, required=False, default=None, default_date=None, validate=None,
                 formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d'], time_formats=['%H:%M:%S', '%H:%M'] ):        
        iter_        = lambda x: x if is_iter(x) else [x,]
        self.formats = {'datetime': iter_( formats )}
        if default_date!=None:
            self.default_date    = default_date
            self.formats['time'] = iter_( time_formats )
            if default == None:
                default = self.__default_date_only
            else:       
                default = self.__default_with_default_date( default )
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
    
    def __default_date_only(self, value):
        if isinstance(value, Time):
            if callable(self.default_date):
                return datetime.combine( self.default_date(), value )
            return datetime.combine( self.default_date, value )
        return value
        
    def __default_with_default_date(self, default_value):
        def default(value):
            if value==None:
                return default_value() if callable(default_value) else default_value
            elif isinstance(value, Time):
                if callable(self.default_date):
                    return datetime.combine( self.default_date(), value )
                return datetime.combine( self.default_date, value )
            return value
        return default
           
    def convert(self, value, to_time=False, to_date=False):
        '''
        Converts to Datetime
        '''
        for key,formats in self.formats.iteritems():
            for format in formats:
                try:
                    dt = datetime.strptime( value, format )
                    if key=='time': return dt.time()
                    return dt.time() if to_time else ( dt.date() if to_date else dt )
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
    def __init__(self, alias=None, required=False, default=False):
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
    def __init__(self, alias=None, required=False, default=None, validate=None, latitude_first=False):
        self.latitude_first = latitude_first
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)        

    def convert(self, value):
        '''
        Converts to Point
        '''
        try:
            x, y = [float(i) for i in value.split(',')]
            if math.isnan( x ) or math.isnan( y ):
                raise ConversionError(self, value)
            return Point(y, x) if self.latitude_first else Point(x, y)
        except ValueError:
            raise ConversionError(self, value)


class IpAddressParam(Parameter):
    '''
    Parameter for IP values
    '''
    def __init__(self, alias=None, required=False, default=None):
        def validate(x):
            try: 
                return socket.inet_aton( x )
            except socket.error:
                return False 
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)

    def convert(self, value):
        return value


class EmailParam(Parameter):
    '''
    Parameter for E-mail values
    '''
    def __init__(self, alias=None, required=False, default=None):
        def validate(x):
            try:
                return EmailField().clean(x)
            except:
                return False
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)    

    def convert(self, value):
        return value
        
        
class InstanceParam(Parameter):
    '''
    Parameter for model instances
    '''
    def __init__(self, model, model_attribute='pk', alias=None, required=False, default=None):
        self.model = model.objects
        self.model_attribute = model_attribute
        Parameter.__init__(self, alias=alias, required=required, default=default)#, validate=validate)
        
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
    def __init__(self, alias=None, required=False, default=None, validate=None):     
        Parameter.__init__(self, alias=alias, required=required, default=default, validate=validate)
    
    def convert(self, value):
        try:
            converted = float(value)
            if math.isnan( converted ):
                 raise ConversionError(self, value)
            return datetime.fromtimestamp( converted )
        except ValueError:
            raise ConversionError(self, value)
        