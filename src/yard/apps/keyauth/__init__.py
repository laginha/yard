#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from yard.apps.keyauth.models import Consumer

KEY_PARAMETER_NAME = getattr(settings, 'KEY_PARAMETER_NAME', 'key')
KEY_AUTH_401_TEMPLATE = getattr(settings, 'KEY_AUTH_401_TEMPLATE', None)

if KEY_AUTH_401_TEMPLATE:
    HttpResponse401 = lambda r: render(r, **KEY_AUTH_401_TEMPLATE)
else:
    KEY_AUTH_401_CONTENT = getattr(settings, 'KEY_AUTH_401_CONTENT', "")
    HttpResponse401 = lambda r: HttpResponse(KEY_AUTH_401_CONTENT, status=401)


def key_required_wrapper(f):
    '''
    Auxiliar decorator for keyauth decorator and middleware
    '''
    def wrapper(klass, request, *args, **kwargs):
        key = authenticate(token=request.REQUEST.get(KEY_PARAMETER_NAME))
        if key and is_valid_consumer(request, key):
            key.save()
            return f(klass, request, *args, **kwargs)
        return HttpResponse401( request )
    return wrapper


def is_valid_consumer(request, key):
    '''
    Validate the client for API access with the given key
    '''
    try:
        ip = request.META.get('REMOTE_ADDR', None)
        return Consumer.objects.get(key=key, ip=ip).allowed
    except Consumer.DoesNotExist:
        consumers = Consumer.objects.filter(key=key, allowed=True)
        return not consumers.exists()


