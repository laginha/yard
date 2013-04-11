#!/usr/bin/env python
# encoding: utf-8
from yard.http import to_http

class SimpleResponseMiddleware(object):
    
    def process_view(self, request, view, args, kwargs):
        status, response = view(request, *args, **kwargs)
        return to_http(request, response, status)
