from yard.forms.params import (
    IntegerParam, PositiveIntegerParam, CharParam, RegexParam, FloatParam,
    PositiveFloatParam, DateTimeParam, DateParam, TimeParam, BooleanParam,
    ChoiceParam, MultipleChoiceParam, IpAddressParam, EmailParam,
    InstanceParam, TimestampParam, CommaSeparatedValueParam, 
    CommaSeparatedIntegerParam,)
from .params.base import Parameter
from django.contrib.gis.geos import Point


class PointParam(Parameter):
    '''
    Parameter for point values
    '''
    def __init__(self, description=None, alias=None, aliases=None, 
                required=False, default=None, validate=None, 
                latitude_first=False):
        self.latitude_first = latitude_first
        super(PointParam, self).__init__(
            description=description, alias=alias, aliases=aliases, 
            required=required, default=default, validate=validate)        

    def convert(self, value):
        '''
        Converts to Point
        '''
        try:
            in_range = lambda lon,lat: (-90 < lat < 90) and (-180 < lon < 180)
            x, y = [float(i) for i in value.split(',')]
            if math.isnan( x ) or math.isnan( y ):
                raise ConversionError(self, value)
            if self.latitude_first:
                if in_range(y, x):
                    return Point(y, x)
            else:
                if in_range(x, y):
                    return Point(x, y)
            raise ConversionError(self, value)
        except ValueError:
            raise ConversionError(self, value)
