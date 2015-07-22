from functools import wraps

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
