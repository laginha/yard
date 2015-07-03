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
import simplejson


class JsonField(object):
    def __init__(self, typename, converter=None, is_link=False, is_uri=False):
        self.typename = typename
        if not converter:
            self.converter = lambda data: str(data)
        self.converter = converter
        self.is_link = is_link
        self.is_uri = is_uri
    
    def get_documentation(self):
        json = {'type': self.typename}
        if self.typename == 'array':
            json['items'] = {'type': 'string'}
        return json
    
    def __call__(self, data, api=None):
        if data:
            return self.converter(data, api) if api else self.converter(data)


def builtin_converter(builtin):
    def wrapper(data):
        if isinstance(data, builtin):
            return data
        return builtin(data)
    return wrapper

Integer = JsonField('integer', int)
Float = JsonField('number', float)
String = JsonField('string', str)
Boolean = JsonField('boolean', bool)
List = JsonField('array', list)
Dict = JsonField('json', dict)

File = JsonField('string', lambda data: data.url)
FilePath = JsonField('string', lambda data: data.path)
QuerySet = JsonField('array', lambda data: [unicode(i) for i in data])
ValuesSet = List = JsonField('array', lambda data: list(data))
RelatedManager = JsonField('array', lambda data: [unicode(i) for i in data.all()])
CommaSeparatedValue = JsonField('string', lambda data: [i for i in data.split(',')])


def json_converter(data):
    data = simplejson.dumps(data, default=lambda x: unicode(x))
    return simplejson.loads(data)

Json = JsonField('json', json_converter)


def unicode_converter(data):
    try:
        return unicode(data)
    except StopIteration:
        return repr(data)

Unicode = JsonField('string',  unicode_converter)
ForeignKey = GenericForeignKey = Unicode


def link_converter(data, api):
    return data.pk, api.get_link(data) 

Link = JsonField('string', link_converter, is_link=True)


def uri_converter(data, api):
    return api.get_uri(data)

URI = JsonField('string', uri_converter, is_uri=True)


OBJECT_TO_JSONFIELD = {
    int: Integer,
    float: Float,
    long: Integer,
    bool: Boolean,
    list: List,
    tuple: List,
    set: List,
    dict: Dict,
    models.query.QuerySet: QuerySet,
    models.query.ValuesQuerySet: ValuesSet,
}
   
def auto_converter(data):
    return OBJECT_TO_JSONFIELD.get( type(data), Unicode )(data)

Auto = JsonField('object', auto_converter)
Default = JsonField('object', lambda data: data)


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
}    

def get_field(obj): 
    return MODELFIELD_TO_JSONFIELD.get( type(obj), Unicode )


SELECT_RELATED_FIELDS = [URI, Link, ForeignKey]
PREFETCH_RELATED_FIELDS = [GenericForeignKey, RelatedManager]


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
    
