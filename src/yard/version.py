#!/usr/bin/env python
# encoding: utf-8
from yard.exceptions import VersionException
from yard.resources import Resource
import re

class ResourceVersions(object):

    def __init__(self, api, routes):
        for name,version in self.__class__.__dict__.iteritems():
            if callable(version) and issubclass(version, Resource):
                setattr(self, name, version(api, routes))

    def __call__(self, request, **kwargs):
        version = re.findall(r'.*version=(.*)', request.META.get('HTTP_ACCEPT', ''))
        requested_version = version[0] if version else request.GET.get('version')
        if version or hasattr(self, requested_version):
            return getattr(self, requested_version)(request, **kwargs)
        if hasattr(self, 'default'):
            return getattr(self, 'default')(request, **kwargs)
        if hasattr(self, 'latest'):
            return getattr(self, 'latest')(request, **kwargs)
        raise VersionException()
    
    @classmethod    
    def get_resource_attribute(self, attr):
        resource = getattr(self, 'latest', getattr(self, 'default'))
        return getattr(resource, attr, None) 
                