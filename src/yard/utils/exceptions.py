#!/usr/bin/env python
# encoding: utf-8

class HttpMethodNotAllowed( Exception ):
    def __init__(self, method):
        self.method = method
    def __str__(self):
        return "Http method %s not allowed" %self.method

class RequiredParamMissing( Exception ):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Required parameter missing from request"
