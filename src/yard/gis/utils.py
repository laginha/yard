#!/usr/bin/env python
# encoding: utf-8
from yard.utils import (
    is_serializable, is_float, is_int, is_str, is_unicode, is_tuple, is_dict,
    is_list, is_file, is_iter, is_strfloat, is_strint, is_method, is_queryset,
    is_valuesset, is_modelinstance, is_httpresponse, is_generator, 
    is_many_related_manager, is_related_manager_object, 
    is_generic_related_manager, is_related_manager,)
from django.contrib.gis.db.models.fields import GeometryField
from django.contrib.gis.geos import GEOSGeometry

def is_geo_value(x):
    return isinstance(x, GEOSGeometry)

def is_geo(x):
    return isinstance(x, GeometryField)
