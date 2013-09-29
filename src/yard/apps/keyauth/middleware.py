#!/usr/bin/env python
# encoding: utf-8
from yard.apps.keyauth import key_required_wrapper, KEY_PARAMETER_NAME
from django.contrib.auth import authenticate


class ApiKeyRequiredMiddleware(object):
    """
    Middleware to check for Api Key in request and validate the Consumer
    """
    @key_required_wrapper
    def process_request(self, request):
        return


class ApiKeyAuthenticationMiddleware(object):
    """
    Middleware to authenticate user through given api key
    """
    def process_request(self, request):
        key = authenticate(token=request.REQUEST.get(KEY_PARAMETER_NAME))
        if key:
            request.key  = key
            request.user = key.user
