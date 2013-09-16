#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from yard.exceptions import MethodNotImplemented
from yard.resources.utils.parameters import ResourceParameters
from yard.resources.utils.builders import JSONbuilder, JSONbuilderForMobile
from yard.resources.utils.meta import ResourceMeta
from yard.resources.utils.page import ResourcePage
from yard import fields

def with_pagination_and_meta(f):
    '''
    Paginates and appends Meta data into the json response if in index view
    '''
    def wrapper(self, request, resources, parameters, fields):
        if hasattr(parameters, 'validated'):
            page = self._paginate( request, resources, parameters )
            objects, links = f(self, request, page, parameters, fields)
            meta = self._meta.generate(request, resources, page, parameters)
            if meta and not links:
                return {'Objects': objects, 'Meta': meta}
            if meta and links:
                return {'Objects': objects, 'Meta': meta, 'Links':links}
            if not meta and links:
                return {'Objects': objects, 'Links': links}
            return objects
        return f(self, request, resources, parameters, fields)[0]
    return wrapper

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