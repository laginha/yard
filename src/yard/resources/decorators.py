#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.decorators import permission_required as django_permission_required
from django.contrib.auth.decorators import login_required as django_login_required
from django.http import HttpResponseRedirect
import inspect


def django_to_yard_decorator(django_decorator):
    '''
    Adapt django's decorators in yard resources
    '''
    def django_to_yard_wrapper(*args, **kwargs):
        redirect = kwargs.pop('redirect', False)
        
        def actual_decorator(f):    
            def decorator_wrapper(klass, request, *rargs, **rkwargs):
                def aux(request, *a, **k):
                    return f(klass, request, *rargs, **rkwargs)
                user_test_decorator = django_decorator(*args, **kwargs)
                result =  user_test_decorator( aux )(request, *rargs, **rkwargs)
                if not redirect and isinstance(result, HttpResponseRedirect):
                    return 401
                return result
            return decorator_wrapper
            
        return actual_decorator
    return django_to_yard_wrapper


def validate(f):
    '''
    Check if resource parameters is valid
    '''
    def wrapper(klass, request, params):
        if not params.is_valid():
            return 400, params.errors()
        return f(klass, request, params)
    return wrapper


def login_required(*args, **kwargs): 
    '''
    Check if user is authenticated
    '''   
    dec = django_login_required
    return django_to_yard_decorator( dec )(*args, **kwargs)


def permission_required(*args, **kwargs):
    '''
    Check if user has permissions
    '''
    dec = permission_required
    return django_to_yard_decorator( dec )(*args, **kwargs)


def validateForm(form_class):
    '''
    Validate request according to given form
    '''
    def decorator(f):
        def wrapper(klass, request, *args, **kwargs):
            
            def validate(*form_args):
                form = form_class(*form_args)
                if form.is_valid():
                    request.form = form
                    return f(klass, request, *args, **kwargs)
                return 400
                
            if not hasattr(request, "FILES"): 
                return validate( request.REQUEST )
            return validate( request.REQUEST, request.FILES )

        return wrapper
    return decorator


def exceptionHandling(exception, return_value):
    '''
    Handle a specific exception
    '''
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except exception:
                return return_value
        return wrapper
    return decorator


def resource_decorator(decorator):
    '''
    Apply one decorator to all HTTP response methods
    Based on: stackoverflow.com/questions/2237624/applying-python-decorators-to-methods-in-a-class
    '''
    def wrapper(cls):
        for name, method in inspect.getmembers(cls, inspect.ismethod):
            if name in ['index', 'show', 'create', 'update', 'destroy']:
                setattr(cls, name, decorator(method))
        return cls
    return wrapper

