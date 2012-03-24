#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls.defaults import patterns, url, include

# allowed http-methods mapped with respective resource-method
collection = {'get':'index', 'post':'create'}
single     = {'get':'show', 'put':'update', 'post':'update', 'delete':'destroy'}

def include_resource(resource):
    '''
    include resource urls for single and collection access
    '''
    urlpatterns = patterns('',
        # url for resource collection access
        url( r'^/(?P<id>[0-9]+)/$', resource(single) ),
        # url for single resource access
        url( r'^/$',                resource(collection) ),
    )
    return include( urlpatterns )



