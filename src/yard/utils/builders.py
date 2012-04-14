#!/usr/bin/env python
# encoding: utf-8

from django.forms.models import model_to_dict
from yard.utils          import is_tuple, is_str, is_list, is_dict

class JSONbuilder:
    def __init__(self, fields):
        self.subfields = filter( is_tuple, fields )
        self.fields    = filter( is_str, fields )
    
    def serializable(self, x):
        return x if is_list(x) or is_dict(x) else unicode(x)
        
    def __call__(self, x):
        json_ = model_to_dict( x, self.fields )
        json_ = dict( [(a, self.serializable(b)) for a,b in json_.items()])
        
        for subfield in self.subfields:
            resource = getattr( x, subfield[0], None )
            build    = JSONbuilder(subfield[1])
            if resource:
                json_[ subfield[0] ] = build( resource )
        
        return json_
