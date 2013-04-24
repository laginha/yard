#!/usr/bin/env python
# encoding: utf-8
from yard.apps.keyauth.models import Consumer

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
