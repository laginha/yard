#!/usr/bin/env python
# encoding: utf-8
from django.db.models.query import QuerySet, ValuesQuerySet
from django.db import models
from django.http import HttpResponse
from types import GeneratorType, NoneType
import re
import inspect


float_  = re.compile(r'^\-?[0-9]+\.[0-9]+$')


def is_serializable(x):
    return isinstance(x, (int,str,unicode,float,list,dict, NoneType))
    
def is_float(x):
    return isinstance(x, float)
    
def is_int(x):
    return isinstance(x, int)
    
def is_str(x):
    return isinstance(x, str)
    
def is_unicode(x):
    return isinstance(x, unicode)
    
def is_tuple(x):
    return isinstance(x, tuple)
    
def is_dict(x):
    return isinstance(x, dict)
    
def is_list(x):
    return isinstance(x, list)
    
def is_file(x):
    return isinstance(x, file)
    
def is_iter(x):
    return hasattr(x, '__iter__')
    
def is_strfloat(x):
    return bool( float_.match(x) ) if x else False
    
def is_strint(x): 
    return x.isdigit() if isinstance(x, (unicode,str)) else False
    
def is_method(x):
    return inspect.ismethod(x)
    
def is_queryset(x):
    return isinstance(x, QuerySet)
    
def is_valuesset(x):
    return isinstance(x, ValuesQuerySet)
    
def is_modelinstance(x):
    return isinstance(x, models.Model)
    
def is_httpresponse(x):
    return isinstance(x, HttpResponse)
    
def is_generator(x):
    return isinstance(x, GeneratorType)
    
def is_many_related_manager(x): 
    name = "django.db.models.fields.related.ManyRelatedManager"
    return name in str(type(x))
    
def is_related_manager_object(x):
    name = "django.db.models.fields.related.RelatedManager"
    return name in str(type(x))
    
def is_generic_related_manager(x):
    name = "django.contrib.contenttypes.generic.GenericRelatedObjectManager"
    return name in str(type(x))
    
def is_related_manager(x): 
    functions = [
        is_many_related_manager, 
        is_related_manager_object, 
        is_generic_related_manager,
    ]
    for each in functions:
        if each(x):
            return True
    return False
