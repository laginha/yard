#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import defaults

collection = {'get':'index', 'post':'create'}
single     = {'get':'show', 'put':'update', 'post':'update', 'delete':'destroy'}

def include(resource):
    urlpatterns = defaults.patterns('',
        defaults.url( r'^/(?P<id>[0-9]+)/$', resource(single) ),
        defaults.url( r'^/$',                resource(collection) ),
    )
    return defaults.include( urlpatterns )



