#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth import authenticate
from django.conf import settings
from django.http import HttpResponse
from yard.apps.keyauth import is_valid_consumer

KEY_PARAMETER_NAME = getattr(settings, 'KEY_PARAMETER_NAME', 'key')
KEY_AUTHENTICATION_FAIL = getattr(settings, 'KEY_AUTHENTICATION_FAIL', "")


def key_required(f):
    """
    Check for API Key in request and validate the Consumer
    """
    def wrapper(resource, request, *args, **kwargs):
        key = authenticate(token=request.REQUEST.get(KEY_PARAMETER_NAME))
        if key and is_valid_consumer(request, key):
            key.save()
            return f(resource, request, *args, **kwargs)
        return HttpResponse(content=KEY_AUTHENTICATION_FAIL, status=401)
    return wrapper
