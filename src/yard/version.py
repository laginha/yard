#!/usr/bin/env python
# encoding: utf-8
from yard.exceptions import NoDefaultVersion
from yard.consts import RESOURCE_VERSION_RE
import re


class Metaclass(type):
    def __getattr__(self, attrname):
        return getattr(self.versions[self.default], attrname)


class VersionController(object):
    __metaclass__ = Metaclass
    re_version = re.compile( RESOURCE_VERSION_RE )

    def __init__(self, api, routes):
        self.api = api
        self.routes = routes
        if not hasattr(self, 'default'):
            raise NoDefaultVersion()

    @property
    def default_resource(self):
        return self.versions[ self.default ]

    def get_documentation(self):
        resource = self.default_resource(self.api, self.routes, self.default)
        return resource.get_documentation()

    def get_version(self, request):
        http_accept = request.META.get('HTTP_ACCEPT', '')
        match = self.re_version.match( http_accept )
        if match and match.group(1):
            return match.group(1)
        return request.GET.get('version', self.default)

    def handle_request(self, request, **kwargs):

        def dispatch(version_name):
            resource = self.versions[ version_name ]
            instance = resource(self.api, self.routes, version_name)
            return instance.handle_request(request, **kwargs)
        
        requested_version = self.get_version( request )
        if requested_version in self.versions:
            return dispatch( requested_version )
        elif hasattr(self, requested_version):
            alias_version = getattr(self, requested_version)
            if alias_version in self.versions:
                return dispatch( alias_version )
        return dispatch( self.default )

                