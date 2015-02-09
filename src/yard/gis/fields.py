#!/usr/bin/env python
# encoding: utf-8
from yard.fields import (
    Integer, Float, List, Dict, String, Unicode, Boolean, CommaSeparatedValue,
    File, FilePath, URI, Link, JSON, ForeignKey, GenericForeignKey, ValuesSet,
    RelatedManager, QuerySet, OBJECT_TO_JSONFIELD, Auto, 
    MODELFIELD_TO_JSONFIELD, get_field,)
from django.contrib.gis.db import models
import simplejson
import gpolyencode


@verify     
def GeoJSON(data):
    return simplejson.loads(data.geojson)
    
@verify
def EncodedPolyline(data):
    encoder = gpolyencode.GPolyEncoder()
    return encoder.encode(data.coords)

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
