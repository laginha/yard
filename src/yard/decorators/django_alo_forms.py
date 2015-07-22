from alo.decorators import validate as original_validate
from .utils import to_yard_decorator

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
