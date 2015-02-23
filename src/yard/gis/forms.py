from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from yard.forms import *
import math


class PointField(CharField):
    default_error_messages = {
        'invalid': _('Enter valid coordinate numbers.'),
        'no_pair': _('Enter a pair of numbers, separated by a comma.'),
        'out_of_range': _('Enter coordinates within range'),
    }
        
    def __init__(self, latitude_first=False, **kwargs):
        self.latitude_first = latitude_first
        super(PointField, self).__init__(**kwargs)
        
    def to_python(self, value):
        in_range = lambda lon,lat: (-90 < lat < 90) and (-180 < lon < 180)
        coords = value.split(',')
        if len(coords) != 2:
            raise ValidationError(self.default_error_messages['no_pair'])
        try:
            x,y = [float(each) for each in coords]
        except ValueError:
            raise ValidationError(self.default_error_messages['invalid'])
        else:
            if math.isnan( x ) or math.isnan( y ):
                raise ValidationError(self.default_error_messages['invalid'])
            elif self.latitude_first:
                if in_range(y, x):
                    return Point(y, x)
            elif in_range(x, y):
                return Point(x, y)
            raise ValidationError(self.default_error_messages['out_of_range'])
