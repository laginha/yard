#!/usr/bin/env python
# encoding: utf-8

from django.forms.models import model_to_dict
from yard.utils          import is_tuple, is_str, is_list, is_dict
from yard.utils          import is_method, is_valuesset, is_queryset
import json


class JSONbuilder:
    
    def __init__(self, fields):
        self.subfields = filter( is_tuple, fields )
        self.fields    = filter( is_str, fields )
        self.methods   = lambda x: filter( is_method, [getattr(x, i, None) for i in self.fields] )
    
    
    def serializable(self, x):
        '''
        Convert to JSON-serializable object
        '''
        return x if is_list(x) or is_dict(x) else unicode(x)
       
        
    def __call__(self, x):
        '''
        Build JSON for resource according to fields attribute
        '''
        json_ = model_to_dict( x, self.fields )
        json_ = dict( [(a, self.serializable(b)) for a,b in json_.items()])
        
        # If subfields in fields
        for subfield in self.subfields:
            resource = getattr( x, subfield[0], None )
            # build sub-json
            build    = JSONbuilder(subfield[1])
            
            # don't include nullable in json
            if resource:
                json_[ subfield[0] ] = build( resource )
        
        # If instance methods in fields
        for method in self.methods(x):
            result = method()
            
            # don't include nullable in json
            if not result:
                continue
                
            # expect for a valuesQuerySet, querySet or json-serializable
            if is_queryset(result):
                json_[method.__name__] = [unicode(i) for i in result]
            elif is_valuesset(result):
                json_[method.__name__] = list( result )
            else:
                try:
                    json_[method.__name__] = json.dumps( result )
                except TypeError:
                    json_[method.__name__] = unicode( result )

        return json_
