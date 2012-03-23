#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import defaults

# allowed http-methods mapped with respective resource-method
collection = {'get':'index', 'post':'create'}
single     = {'get':'show', 'put':'update', 'post':'update', 'delete':'destroy'}

def include(resource):
    '''
    include resource urls for single and collection access
    '''
    urlpatterns = defaults.patterns('',
        # url for resource collection access
        defaults.url( r'^/(?P<id>[0-9]+)/$', resource(single) ),
        # url for single resource access
        defaults.url( r'^/$',                resource(collection) ),
    )
    return defaults.include( urlpatterns )



