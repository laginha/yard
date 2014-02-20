#!/usr/bin/env python
# encoding: utf-8
from yard.exceptions import NoDefaultVersion
from yard.resources import Resource
import re

class Metaclass(type):
    def __getattr__(self, name):
        return getattr(self.default, name)


class ResourceVersions(object):
    __metaclass__ = Metaclass

    def __init__(self, api, routes):
        for name,version in self.__class__.__dict__.iteritems():
            if callable(version) and issubclass(version, Resource):
                setattr(self, name, version(api, routes))
        self.description = self.__description()

    def __call__(self, request, **kwargs):
        version = re.findall(r'.*version=(.*)', request.META.get('HTTP_ACCEPT', ''))
        requested_version = version[0] if version else request.GET.get('version')
        if hasattr(self, requested_version):
            return getattr(self, requested_version)(request, **kwargs)
        return self.default(request, **kwargs)
        
    def __description(self):
        if hasattr(self, 'default'):
            return self.default.description
        raise NoDefaultVersion()
                