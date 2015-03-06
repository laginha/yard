#!/usr/bin/env python
# encoding: utf-8
from yard.fields import (
    JsonField, Integer, Float, List, Dict, String, Unicode, Boolean, 
    CommaSeparatedValue, File, FilePath, URI, Link, JSON, ForeignKey, 
    GenericForeignKey, ValuesSet, RelatedManager, QuerySet, OBJECT_TO_JSONFIELD, 
    Auto, MODELFIELD_TO_JSONFIELD, get_field,)
from django.contrib.gis.db import models
import ujson
import gpolyencode


def encoded_polyline_converter(data):
    encoder = gpolyencode.GPolyEncoder()
    return encoder.encode(data.coords)

GeoJson = JsonField('string', lambda data: ujson.loads(data.geojson))
EncodedPolyline = JsonField('string', encoded_polyline_converter)


OBJECT_TO_JSONFIELD.update({
    models.fields.LineStringField: GeoJSON,
    models.fields.MultiLineStringField: GeoJSON,
    models.fields.PointField: GeoJSON,
    models.fields.MultiPointField: GeoJSON,
    models.fields.PolygonField: GeoJSON,
    models.fields.MultiPolygonField: GeoJSON,
    models.fields.GeometryField: GeoJSON,
    models.fields.GeometryCollectionField: GeoJSON,
})

MODELFIELD_TO_JSONFIELD.update({
    models.GeometryField: GeoJSON,
    models.PointField: GeoJSON,
    models.LineStringField: GeoJSON,
    models.PolygonField: GeoJSON,
    models.MultiPointField: GeoJSON,
    models.MultiLineStringField: GeoJSON,
    models.MultiPolygonField: GeoJSON,
})   
