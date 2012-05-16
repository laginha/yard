#!/usr/bin/env python
# encoding: utf-8

class ResourceMeta(object):
    __defaults = [
        ('no_meta',               False),
        ('parameters_considered', True),
        ('total_objects',         True),
    ]
    
    def __init__(self, meta):
        self.__new_meta = [
            (k,v) for k,v in meta.__class__.__dict__.iteritems() if callable(v)
        ]
        for k,v in self.__defaults:
            setattr(self, k, getattr(meta,k) if hasattr(meta, k) else v)
                      
    def fetch(self, resources, params):
        meta = {}
        self.__fetch_new_meta(meta, resources)
        self.__fetch_defaults(meta, resources, params)    
        return meta

    def __fetch_defaults(self, meta, resources, params):
        for k,v in self.__defaults:
            if getattr(self,k) == True:
                if k == 'no_meta':
                    return
                elif k == 'total_objects':
                    meta[k] = resources.count()
                elif k == 'parameters_considered':
                    meta[k] = params
            
    def __fetch_new_meta(self, meta, resources):
        print self.__new_meta
        for k,v in self.__new_meta:
            try:
                meta[k] = v(resources)
            except Exception as e:
                continue
    