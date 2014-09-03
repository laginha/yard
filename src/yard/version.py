#!/usr/bin/env python
# encoding: utf-8
from yard.exceptions import NoDefaultVersion
from yard.resources import Resource
import re

class Metaclass(type):
    def __getattr__(self, attrname):
        return getattr(self.versions[self.default], attrname)


class ResourceVersions(object):
    __metaclass__ = Metaclass

    def __init__(self, api, routes):
        self.version_to_resource = {}
        for name,version in self.versions.items():
            if callable(version) and issubclass(version, Resource):
                self.version_to_resource[ name ] = version(api, routes)
        if hasattr(self, 'default'):
            self.default_resource = self.version_to_resource[ self.default ]
            self.description = self.default_resource.description
        else:
            raise NoDefaultVersion()

    def __call__(self, request, **kwargs):
        version = re.findall(r'.*version=(.*)', request.META.get('HTTP_ACCEPT', ''))
        requested_version = version[0] if version else request.GET.get('version')
        if requested_version:
            if requested_version in self.version_to_resource:
                return self.version_to_resource[ requested_version ](request, **kwargs)
            elif hasattr(self, requested_version):
                alias_version = getattr(self, requested_version)
                if alias_version in self.version_to_resource:
                    return self.version_to_resource[ alias_version ](request, **kwargs)
        return self.default_resource(request, **kwargs)

                