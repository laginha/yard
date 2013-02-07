#!/usr/bin/env python
# encoding: utf-8
from yard.exceptions import VersionException

class ResourceVersions(object):

    def __init__(self, routes):
        for name,version in self.__class__.__dict__.iteritems():
            if name not in ['__module__', '__main__', '__doc__']:
                setattr(self, name, version(routes))

    def __call__(self, request, **kwargs):
        if 'version' in request.META or 'version' in request.GET:
            requested_version = request.META.get('version', request.GET['version'])
            if hasattr(self, requested_version):
                return getattr(self, requested_version)(request, **kwargs)
        if hasattr(self, 'default'):
            return getattr(self, 'default')(request, **kwargs)
        if hasattr(self, 'latest'):
            return getattr(self, 'latest')(request, **kwargs)
        raise VersionException()     
                