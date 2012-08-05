#!/usr/bin/env python
# encoding: utf-8

def validate(f):
    '''
    Check if resource parameters is valid
    '''
    def wrapper(self, params):
        if not params.is_valid():
            return params.errors()
        return f(self, params)
    return wrapper
