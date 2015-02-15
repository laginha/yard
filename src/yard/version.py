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
    
    @classmethod
    def preprocess(cls, api):
        cls.api = api
        if hasattr(cls, 'default'):
            cls.default_resource = cls.versions[ cls.default ]
            cls.description = cls.default_resource.description
        else:
            raise NoDefaultVersion()
        for version_name, resource in cls.versions.items():
            resource.preprocess(cls.api, version_name=version_name)

    def __init__(self, routes):
        self.routes = routes

    def get_documentation(self):
        resource = self.versions[self.default](self.routes)
        return resource.get_documentation()

    def get_version(self, request):
        http_accept = request.META.get('HTTP_ACCEPT', '')
        match = self.re_version.match( http_accept )
        if match and match.group(1):
            return match.group(1)
        return request.GET.get('version', self.default)

    def handle_request(self, request, **kwargs):

        def dispatch(resource):
            return resource(self.routes).handle_request(request, **kwargs)
        
        requested_version = self.get_version( request )
        if requested_version in self.versions:
            return dispatch( self.versions[requested_version] )
        elif hasattr(self, requested_version):
            alias_version = getattr(self, requested_version)
            if alias_version in self.versions:
                return dispatch( self.versions[alias_version] )
        return dispatch( self.default_resource )

                