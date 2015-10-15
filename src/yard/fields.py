#!/usr/bin/env python
# encoding: utf-8
try:
    from django.contrib.gis.db import models
    GIS_ENABLED = True
except ImportError:
    from django.db import models
    import sys
    sys.stdout.write("Warning: Could not find the GEOS library.\n")
    GIS_ENABLED = False

from django.db.models.query import QuerySet
from django.db.models.query import ValuesQuerySet
import json
import uuid


class JsonField(object):
    '''
    Base json response field
    '''
    def __init__(self, typename, converter, is_link=False, is_uri=False, 
                 use_in_select_related=False, use_in_prefetch_related=False):
        self.typename = typename
        self.converter = converter
        self.is_link = is_link
        self.is_uri = is_uri
        self.use_in_select_related = use_in_select_related
        self.use_in_prefetch_related = use_in_prefetch_related
    
    def get_documentation(self):
        json = {'type': self.typename}
        if self.typename == 'array':
            json['items'] = {'type': 'string'}
        return json
    
    def __call__(self, data, api=None):
        if data:
            return self.converter(data, api) if api else self.converter(data)

#
# Converters
#

def json_converter(data):
    data = json.dumps(data, default=lambda x: unicode(x))
    return json.loads(data)
    
def unicode_converter(data):
    try:
        return unicode(data)
    except StopIteration:
        return repr(data)
        
def link_converter(data, api):
    return data.pk, api.get_link(data) 
    
def uri_converter(data, api):
    return api.get_uri(data)
    
def auto_converter(data):
    return OBJECT_TO_JSONFIELD.get( type(data), Unicode )(data)

def related_converter(data):
    return [unicode(each) for each in data.all()]

#
# Fields
#
Auto = JsonField('object', auto_converter)
Boolean = JsonField('boolean', bool)
CommaSeparatedValue = JsonField('string', lambda data: [i for i in data.split(',')])
Default = JsonField('object', lambda data: data)
Dict = JsonField('json', dict)
File = JsonField('string', lambda data: data.url)
FilePath = JsonField('string', lambda data: data.path)
Float = JsonField('number', float)
Integer = JsonField('integer', int)
UUID = JsonField('string', lambda data: data.hex)
Json = JsonField('json', json_converter)
QuerySet = JsonField('array', lambda data: [unicode(i) for i in data])
String = JsonField('string', str)
Unicode = JsonField('string',  unicode_converter)
ValuesSet = List = JsonField('array', list)
# Fields used in prefetch_related
GenericForeignKey = JsonField('string',  unicode_converter, use_in_prefetch_related=True)
RelatedManager = JsonField('array', related_converter, use_in_prefetch_related=True)
# Fields used in select_related
ForeignKey = JsonField('string', unicode_converter, use_in_select_related=True)
Link = JsonField('string', link_converter, is_link=True, use_in_select_related=True)
URI = JsonField('string', uri_converter, is_uri=True, use_in_select_related=True)

#
# Utils
#

OBJECT_TO_JSONFIELD = {
    int: Integer,
    float: Float,
    long: Integer,
    bool: Boolean,
    list: List,
    tuple: List,
    set: List,
    dict: Dict,
    uuid.UUID: UUID,
    QuerySet: QuerySet,
    ValuesQuerySet: ValuesSet,
}

MODELFIELD_TO_JSONFIELD = {
    models.AutoField: Integer,
    models.BigIntegerField: Integer,
    models.IntegerField: Integer,
    models.PositiveIntegerField: Integer,
    models.PositiveSmallIntegerField: Integer,
    models.SmallIntegerField: Integer,
    models.BooleanField: Boolean,
    models.NullBooleanField: Boolean,
    models.CommaSeparatedIntegerField: CommaSeparatedValue,
    models.DecimalField: Float,
    models.FloatField: Float,
    models.FileField: File,
    models.ImageField: File,
    models.FilePathField: FilePath,
    models.ManyToManyField: RelatedManager,
    models.UUIDField: UUID,
}    

if GIS_ENABLED:
    import gpolyencode
    import ujson
    
    def encoded_polyline_converter(data):
        encoder = gpolyencode.GPolyEncoder()
        return encoder.encode(data.coords)

    GeoJson = JsonField('string', lambda data: ujson.loads(data.geojson))
    Distance = JsonField('number', lambda data: data.km)
    EncodedPolyline = JsonField('string', encoded_polyline_converter)


    OBJECT_TO_JSONFIELD.update({
        models.fields.LineStringField: GeoJson,
        models.fields.MultiLineStringField: GeoJson,
        models.fields.PointField: GeoJson,
        models.fields.MultiPointField: GeoJson,
        models.fields.PolygonField: GeoJson,
        models.fields.MultiPolygonField: GeoJson,
        models.fields.GeometryField: GeoJson,
        models.fields.GeometryCollectionField: GeoJson,
    })

    MODELFIELD_TO_JSONFIELD.update({
        models.GeometryField: GeoJson,
        models.PointField: GeoJson,
        models.LineStringField: GeoJson,
        models.PolygonField: GeoJson,
        models.MultiPointField: GeoJson,
        models.MultiLineStringField: GeoJson,
        models.MultiPolygonField: GeoJson,
    })   

def get_field(obj): 
    return MODELFIELD_TO_JSONFIELD.get( type(obj), Unicode )
