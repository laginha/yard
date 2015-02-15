#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.decorators import (
    permission_required as original_permission_required,
    login_required as original_login_required,)
from keyauth.decorators import key_required as original_key_required
from functools import wraps


class DjangoToYardDecorator(object):
    '''
    Adapt django's decorators to yard resources
    '''
    def __init__(self, func):
        self.original_decorator = func
    
    def __call__(self, *args, **kwargs):
        def decorator(func):
            @wraps(func)
            def wrapper(klass, request, *rargs, **rkwargs):
                def func_wrapper(request, *a, **k):
                    return func(klass, request, *rargs, **rkwargs)
                original_decorator = self.original_decorator(*args, **kwargs)
                return original_decorator(func_wrapper)(
                    request, *rargs, **rkwargs)
            return wrapper
        return decorator


def login_required(*args, **kwargs): 
    '''
    Check if user is authenticated
    '''   
    return DjangoToYardDecorator( original_login_required )(*args, **kwargs)


def permission_required(*args, **kwargs):
    '''
    Check if user has permissions
    '''
    return DjangoToYardDecorator(original_permission_required)(*args, **kwargs)


def key_required(*args, **kwargs):
    '''
    Check key for access
    '''
    return DjangoToYardDecorator( original_key_required )(*args, **kwargs)
