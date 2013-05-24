#!/usr/bin/env python
# encoding: utf-8
from django.contrib.gis.db import models
import simplejson

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
    
JSON = Dict

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
def GeoJSON(data):
    return simplejson.loads(data.geojson)
    
@verify  
def RelatedManager(data): 
    return [unicode(i) for i in data.all()]
    
@verify   
def QuerySet(data): 
    return [unicode(i) for i in data]

@verify   
def ValuesSet(data): 
    return list(data)

@verify   
def URI(data, api): 
    return api.get_uri(data)


MAPPING = {
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

get_field = lambda obj: MAPPING.get( type(obj), Unicode )
