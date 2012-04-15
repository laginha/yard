#!/usr/bin/env python
# encoding: utf-8

class InvalidStatusCode( Exception ):
    def __init__(self, status):
        self.status = status
    def __str__(self):
        return "'%s' is not a valid http status code" %self.status

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
