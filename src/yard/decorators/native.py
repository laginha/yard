#!/usr/bin/env python
# encoding: utf-8
from functools import wraps
import inspect


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

