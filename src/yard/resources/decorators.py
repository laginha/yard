#!/usr/bin/env python
# encoding: utf-8

def validate(f):
    '''
    Check if resource parameters is valid
    '''
    def wrapper(self, request, params):
        if not params.is_valid():
            return params.errors()
        return f(self, request, params)
    return wrapper


def login_required(f):
    def wrapper(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(self, request, *args, **kwargs)
        else:
            return 401
    return wrapper


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
        