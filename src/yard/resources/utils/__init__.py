#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from yard.exceptions import MethodNotImplemented
from yard.resources.utils.parameters import ResourceParameters
from yard.resources.utils.builders import JSONbuilder
from yard.resources.utils.meta import ResourceMeta
from yard.resources.utils.page import ResourcePage
from yard import fields

class method_required(object):
    def __init__(self, method):
        self.method = method
        
    def __call__(self, f):
        def wrapper(klass, *args, **kwargs):
            if not hasattr(klass, self.method):
                raise MethodNotImplemented(self.method)
            return f(klass, *args, **kwargs)
        return wrapper

def model_to_fields(model):
    return dict(
        [ (i.name, fields.get_field(i)) 
            for i in model._meta.fields if i.name not in ['mymodel_ptr']]
    )
