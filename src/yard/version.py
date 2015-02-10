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
        cls.version_to_resource = {}
        for version_name, resource in cls.versions.items():
            resource.preprocess(cls.api)
            cls.version_to_resource[ version_name ] = resource
        if hasattr(cls, 'default'):
            cls.default_resource = cls.version_to_resource[ cls.default ]
            cls.description = cls.default_resource.description
        else:
            raise NoDefaultVersion()

    def __init__(self, routes):
        self.routes = routes

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
        if requested_version in self.version_to_resource:
            return dispatch( self.version_to_resource[requested_version] )
        elif hasattr(self, requested_version):
            alias_version = getattr(self, requested_version)
            if alias_version in self.version_to_resource:
                return dispatch( self.version_to_resource[alias_version] )
        return dispatch( self.default_resource )

                