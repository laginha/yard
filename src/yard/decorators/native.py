#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from functools import wraps
import inspect


def validate(form_class, extra=None):
    '''
    Validate request according to given form
    ''' 
    def decorator(func):        
        func.form_class = form_class
        
        @wraps(func)
        def wrapper(resource, request, *args, **kwargs):
            
            def do_validation(form_kwargs):
                if extra != None:
                    form_kwargs.update( extra(resource, request) )
                form = form_class(**form_kwargs)
                if form.is_valid():
                    request.form = form
                    return func(resource, request, *args, **kwargs)
                return 400, form.errors
            
            form_kwargs = {'data': request.REQUEST}
            if not hasattr(request, "FILES"): 
                form_kwargs['files'] = request.FILES
            if issubclass(form_class, ModelForm) and args:
                if isinstance(args[0], int):
                    instance = get_object_or_404(model, pk=args[0])
                    form_kwargs['instance'] = instance
            return do_validation(form_kwargs)

        return wrapper
    return decorator


def exception_handling(exception, response):
    '''
    Handle a specific exception
    '''
    def decorator(func):
        @wraps(func)
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

