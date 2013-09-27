#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.decorators import permission_required, login_required as django_login_required
from django.http import HttpResponseRedirect


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
                if not redirect and isinstance(HttpResponseRedirect, result):
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
    dec = django_login_required
    return django_to_yard_decorator( dec )(*args, **kwargs)


def perm_required(*args, **kwargs):
    dec = permission_required
    return django_to_yard_decorator( dec )(*args, **kwargs)


class validateForm(object):
    def __init__(self, form):
        self.form   = form
        
    def __call__(self, f):    
        def wrapper(klass, request, *args, **kwargs):
            
            def validate(*form_args):
                form = self.form(*form_args)
                if form.is_valid():
                    request.form = form
                    return f(klass, request, *args, **kwargs)
                return 400
                
            if not hasattr(request, "FILES"): 
                return validate( request.REQUEST )
            return validate( request.REQUEST, request.FILES )
        return wrapper
        
        
class exceptionHandling(object):
    def __init__(self, exception, return_value=400):
        self.exception    = exception
        self.return_value = return_value
        
    def __call__(self, f):
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except self.exception:
                return self.return_value
        return wrapper
        