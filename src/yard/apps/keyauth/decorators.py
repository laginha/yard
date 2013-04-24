#!/usr/bin/env python
# encoding: utf-8
from yard.apps.keyauth import key_required_wrapper

def key_required(f):
    """
    Check for API Key in request and validate the Consumer
    """
    @key_required_wrapper
    def wrapper(resource, request, *args, **kwargs):
        return f(resource, request, *args, **kwargs)
    return wrapper
