#!/usr/bin/env python
# encoding: utf-8
from django.db.models.query              import QuerySet, ValuesQuerySet
from django.db                           import models
from django.http                         import HttpResponse
from types                               import GeneratorType, NoneType
import re, inspect

try:
    from django.contrib.gis.db.models.fields import GeometryField
    from django.contrib.gis.geos             import GEOSGeometry
    is_geodj_project = True
except ImportError:
    import sys
    sys.stdout.write("Warning: Could not find the GEOS library.\n")
    is_geodj_project = False

float_  = re.compile(r'^\-?[0-9]+\.[0-9]+$')

current_url      = lambda x: "%s/%s" %(x.get_host(), x.META.get('PATH_INFO', ''))
is_serializable  = lambda x: isinstance(x, (int,str,unicode,float,list,dict, NoneType))
is_float         = lambda x: isinstance(x, float)
is_int           = lambda x: isinstance(x, int)
is_str           = lambda x: isinstance(x, str)
is_unicode       = lambda x: isinstance(x, unicode)
is_tuple         = lambda x: isinstance(x, tuple)
is_dict          = lambda x: isinstance(x, dict)
is_list          = lambda x: isinstance(x, list)
is_file          = lambda x: isinstance(x, file)
is_iter          = lambda x: hasattr(x, '__iter__')
is_strfloat      = lambda x: bool( float_.match(x) ) if x else False
is_strint        = lambda x: x.isdigit() if isinstance(x, (unicode,str)) else False
is_method        = lambda x: inspect.ismethod(x)
is_geo_value     = lambda x: is_geodj_project and isinstance(x, GEOSGeometry)
is_geo           = lambda x: is_geodj_project and isinstance(x, GeometryField)
is_queryset      = lambda x: isinstance(x, QuerySet)
is_valuesset     = lambda x: isinstance(x, ValuesQuerySet)
is_modelinstance = lambda x: isinstance(x, models.Model)
is_httpresponse  = lambda x: isinstance(x, HttpResponse)
is_generator     = lambda x: isinstance(x, GeneratorType)
is_many_related_manager    = lambda x: "django.db.models.fields.related.ManyRelatedManager" in str(type(x))
is_related_manager         = lambda x: "django.db.models.fields.related.RelatedManager" in str(type(x))
is_generic_related_manager = lambda x: "django.contrib.contenttypes.generic.GenericRelatedObjectManager" in str(type(x))
is_related_manager         = lambda x: is_many_related_manager(x) and is_related_manager(x) and is_generic_related_manager(x)
