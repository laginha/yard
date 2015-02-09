#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import get_object_or_404
import inspect


def validate(func):
    '''
    Check if resource parameters is valid
    '''
    def wrapper(klass, request, params):
        if not params.is_valid():
            return 400, params.errors()
        return func(klass, request, params)
    return wrapper


def validate_form(form_class, include_instance=True, 
                    instance_name='instance', extra=None):
    '''
    Validate request according to given form
    '''
    def decorator(func):
        def wrapper(klass, request, *args, **kwargs):
            
            def do_validation(form_kwargs):
                if extra != None:
                    form_kwargs.update( extra(klass, request) )
                form = form_class(**form_kwargs)
                if form.is_valid():
                    request.form = form
                    return func(klass, request, *args, **kwargs)
                return 400
            
            form_kwargs = {'data': request.REQUEST}
            if not hasattr(request, "FILES"): 
                form_kwargs['files'] = request.FILES
            if include_instance:
                argspec = inspect.getargspec(form_class.__init__).args
                if instance_name in argspec:
                    if kwargs.get('pk', None) and hasattr(klass, model):
                        model = klass.model
                        obj = get_object_or_404(model, pk=kwargs['pk'])
                        form_kwargs[instance_name] = obj
            return do_validation(form_kwargs)

        return wrapper
    return decorator


def exception_handling(exception, response):
    '''
    Handle a specific exception
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception:
                return return_value
        return wrapper
    return decorator


def resource_decorator(decorator):
    '''
    Apply one decorator to all HTTP response methods
    Based on: 
    stackoverflow.com/questions/2237624/applying-python-decorators-to-methods-in-a-class
    '''
    def wrapper(cls):
        methods = [
            'index', 'show', 'create', 'update', 'destroy', 'new', 'edit'
        ]
        for name, method in inspect.getmembers(cls, inspect.ismethod):
            if name in methods:
                setattr(cls, name, decorator(method))
        return cls
    return wrapper

