#!/usr/bin/env python
# encoding: utf-8
from django.contrib.gis.db import models
import simplejson

Integer = int
Float = float
List = Tuple = Iter = list
Dict = JSON = dict
Unicode = String = unicode
Boolean = bool
CommaSeparatedValue = lambda resource: [i for i in resource.split(',')],
File = lambda resource: resource.url,
FilePath = lambda resource: resource.path,
GEOJSON = lambda resource: simplejson.loads(resource.geojson)
RelatedManager = lambda resource: [unicode(i) for i in resource.all()]
QuerySet = lambda resource: [unicode(i) for i in resource]
ValuesSet = lambda resource: list( resource )
URI = lambda resource, api: api.get_uri(resource)

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
