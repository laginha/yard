#!/usr/bin/env python
# encoding: utf-8
from django.db import models
from functools import wraps


def verify(f):
    @wraps(f)
    def wrapper(data, *args):
        return f(data, *args) if data else None
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
    try:
        return unicode(data)
    except:
        return repr(data)
        
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


JSON = Dict
ForeignKey = GenericForeignKey = Unicode
ValuesSet = List

@verify  
def RelatedManager(data): 
    return [unicode(i) for i in data.all()]
    
@verify   
def QuerySet(data): 
    return [unicode(i) for i in data]


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
}    

def get_field(obj): 
    return MODELFIELD_TO_JSONFIELD.get( type(obj), Unicode )


SELECT_RELATED_FIELDS = [URI, Link, ForeignKey]
PREFETCH_RELATED_FIELDS = [GenericForeignKey, RelatedManager]
