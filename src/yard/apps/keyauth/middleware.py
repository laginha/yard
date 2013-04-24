#!/usr/bin/env python
# encoding: utf-8
from yard.apps.keyauth import key_required_wrapper

class ApiKeyRequiredMiddleware(object):
    """
    Middleware to check for Api Key in request and validate the Consumer
    """
    @key_required_wrapper
    def process_view(self, request, view, *args, **kwargs):
        return view(request, *args, **kwargs)
