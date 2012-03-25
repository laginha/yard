#!/usr/bin/env python
# encoding: utf-8
from django.contrib.gis.db.models.fields import GeometryField
from django.db.models.query import QuerySet, ValuesQuerySet
import re, inspect

float_  = re.compile(r'^\-?[0-9]+\.[0-9]+$')

current_url = lambda x: "%s/%s" %(x.get_host(), x.META.get('PATH_INFO', ''))

is_float = lambda x: isinstance(x, float)
is_int   = lambda x: isinstance(x, int)
is_str   = lambda x: isinstance(x, str)
is_tuple = lambda x: isinstance(x, tuple)
is_dict  = lambda x: isinstance(x, dict)
is_list  = lambda x: isinstance(x, list)

is_strfloat = lambda x: bool( float_.match(x) ) if x else False
is_strint   = lambda x: x.isdigit() if is_str(x) else False

is_method    = lambda x: inspect.ismethod(x)
is_geo       = lambda x: isinstance(x, GeometryField)
is_queryset  = lambda x: isinstance(x, QuerySet)
is_valuesset = lambda x: isinstance(x, ValuesQuerySet)
