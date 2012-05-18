#!/usr/bin/env python
# encoding: utf-8

from django.db.models import Avg, Max, Min, Count
from yard.exceptions  import NoMeta


class MetaDict(dict):
    def __init__(self, resources, params):
        self.resources = resources
        self.params    = params
    
    def total_objects(self, name):
        self[name] = self.resources.count()
    
    def parameters_validated(self, name):
        self[name] = self.params
    
    def __aggregation(self, value, call):
        if not value: return
        for a,b in value:
            self[a] = self.resources.aggregate(_yard_=call(b))['_yard_']
        
    def minimum(self, value):
        self.__aggregation(value, Min)
        
    def maximum(self, value):
        self.__aggregation(value, Max)
        
    def average(self, value):
        self.__aggregation(value, Avg)
        
    def count(self, value):
        self.__aggregation(value, Count)
        
    def custom(self, name, call):
        try:
            self[name] = call(self.resources)
        except Exception as e:
            return


class ResourceMeta(object):
    __defaults = [
        ('no_meta',               False),
        ('parameters_validated',  True),
        ('total_objects',         True),
        ('average',               None),
        ('minimum',               None),
        ('maximum',               None),
        ('count',                 None)
    ]
    
    def __init__(self, meta):
        self.__new_meta = [
            (k,v) for k,v in meta.__class__.__dict__.iteritems() if callable(v)
        ]
        for k,v in self.__defaults:
            setattr(self, k, getattr(meta,k) if hasattr(meta, k) else v)
                      
    def fetch(self, resources, params):
        try:
            meta = MetaDict( resources, params )
            self.__fetch_defaults( meta ) 
            self.__fetch_new_meta( meta )
            return meta
        except NoMeta:
            return meta

    def __fetch_defaults(self, meta):
        for name,default in self.__defaults:
            value = getattr(self, name)
            if name=='no_meta' and value: 
                raise NoMeta()
            elif default==None:
                getattr(meta, name)( value )
            elif value:
                getattr(meta, name)( name )
        return meta
   
    def __fetch_new_meta(self, meta):
        for name,call in self.__new_meta:
            meta.custom( name, call )
    