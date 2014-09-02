#!/usr/bin/env python
# encoding: utf-8
from django.contrib.gis.db import models
import simplejson#, gpolyencode


def verify(f):
    def wrapper(data, *args):
        return f(data, *args) if data != None else None
    return wrapper


@verify
def Integer(data):
    return int(data)
    
@verify
def Float(data):
    return float(data)

@verify
def List(data):
    return list(data)
    
@verify
def Dict(data):
    return dict(data)
    
@verify
def String(data):
    return str(data)
    
@verify
def Unicode(data):
    return unicode(data)
        
@verify
def Boolean(data):
    return bool(data)
            
@verify
def CommaSeparatedValue(data):
    return lambda data: [i for i in data.split(',')]

@verify
def File(data): 
    return data.url
    
@verify    
def FilePath(data): 
    return data.path
    
@verify   
def URI(data, api): 
    return api.get_uri(data)

@verify   
def Link(data, api): 
    return data.pk, api.get_link(data)

@verify     
def GeoJSON(data):
    return simplejson.loads(data.geojson)

JSON = Dict
ForeignKey = GenericForeignKey = Unicode
ValuesSet = List

@verify  
def RelatedManager(data): 
    return [unicode(i) for i in data.all()]
    
@verify   
def QuerySet(data): 
    return [unicode(i) for i in data]

@verify
def EncodedPolyline(data):
    encoder = gpolyencode.GPolyEncoder()
    return encoder.encode(data.coords)


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
    models.fields.LineStringField: GeoJSON,
    models.fields.MultiLineStringField: GeoJSON,
    models.fields.PointField: GeoJSON,
    models.fields.MultiPointField: GeoJSON,
    models.fields.PolygonField: GeoJSON,
    models.fields.MultiPolygonField: GeoJSON,
    models.fields.GeometryField: GeoJSON,
    models.fields.GeometryCollectionField: GeoJSON,
}

@verify   
def Auto(data):
    return OBJECT_TO_JSONFIELD.get( type(data), Unicode )(data)


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
    models.GeometryField: GeoJSON,
    models.PointField: GeoJSON,
    models.LineStringField: GeoJSON,
    models.PolygonField: GeoJSON,
    models.MultiPointField: GeoJSON,
    models.MultiLineStringField: GeoJSON,
    models.MultiPolygonField: GeoJSON,
}    

get_field = lambda obj: MODELFIELD_TO_JSONFIELD.get( type(obj), Unicode )
