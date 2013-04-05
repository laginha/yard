#!/usr/bin/env python
# encoding: utf-8
from django.contrib.gis.db import models
import simplejson

Integer = int
Float = float
List = Tuple = Iter = list
Dict = JSON = dict
String = str
Unicode = unicode
Boolean = bool
CommaSeparatedValue = lambda data: [i for i in data.split(',')],
File = lambda data: data.url,
FilePath = lambda data: data.path,
GEOJSON = lambda data: simplejson.loads(data.geojson)
RelatedManager = lambda data: [unicode(i) for i in data.all()]
QuerySet = lambda data: [unicode(i) for i in data]
ValuesSet = lambda data: list( data )
URI = lambda data, api: api.get_uri(data)

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
    models.GeometryField: GEOJSON,
    models.PointField: GEOJSON,
    models.LineStringField: GEOJSON,
    models.PolygonField: GEOJSON,
    models.MultiPointField: GEOJSON,
    models.MultiLineStringField: GEOJSON,
    models.MultiPolygonField: GEOJSON,
}

get_field = lambda obj: MAPPING.get( type(obj), Unicode )
