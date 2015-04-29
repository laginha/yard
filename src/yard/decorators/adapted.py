#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.decorators import (
    permission_required as original_permission_required,
    login_required as original_login_required,)
from keyauth.decorators import key_required as original_key_required
from throttling.decorators import throttle as original_throttle
from alo.decorators import validate as original_validate
from functools import wraps


def validate(form_class):
    '''
    Validate request according to given form
    ''' 
    original_decorator = original_validate(form_class)
    def decorator(func):
        if hasattr(func, '__func__'):
            func.__func__.form_class = form_class
        else:
            func.form_class = form_class
        return original_decorator(func)
    return decorator


class to_yard_decorator(object):
    '''
    Adapt django's decorators to yard resources
    '''
    def __init__(self, func):
        self.original_decorator = func()
    
    def __call__(self, *args, **kwargs):
        
        def decorator(func):
            @wraps(func)
            def wrapper(klass, request, *args, **kwargs):
                def func_wrapper(request, *a, **k):
                    return func(klass, request, *args, **kwargs)
                return original_wrapper(func_wrapper)(request, *args, **kwargs)
            return wrapper
            
        original_wrapper = self.original_decorator(*args, **kwargs)
        return decorator


@to_yard_decorator
def login_required(): 
    return original_login_required

@to_yard_decorator
def permission_required():
    return original_permission_required

@to_yard_decorator
def key_required():
    return original_key_required

@to_yard_decorator
def throttle():
    return original_throttle
