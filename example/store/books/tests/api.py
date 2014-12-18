#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.resources.utils.builders import JSONbuilder
from yard.api import Api
from books.tests.base import BaseTestCase
from books.models  import *
from books.resources import BookResource, BookResourceVersions


class ApiTestCase( BaseTestCase ):
 
    def test_api_include(self):
        api = Api()
        api.include('a', BookResource)
        api.include('b', BookResourceVersions)
        assert len( api.urlpatterns ) == 2*4
        
        api = Api()
        api.include('a', BookResource, name='books')
        assert len( api.urlpatterns ) == 4
        viewnames = [each.name for each in api.urlpatterns]
        assert 'books.detail' in viewnames
        assert 'books.list' in viewnames
        assert 'books.edit' in viewnames
        assert 'books.new' in viewnames
        
        api = Api()
        api.include('b', BookResourceVersions)
        assert len( api.urlpatterns ) == 4
        viewnames = [each.name for each in api.urlpatterns]
        assert 'BookResourceVersions.detail' in viewnames
        assert 'BookResourceVersions.list' in viewnames
        assert 'BookResourceVersions.edit' in viewnames
        assert 'BookResourceVersions.new' in viewnames
        
        api = Api(discover=True)
        api.include('a', BookResource)
        api.include('b', BookResourceVersions)
        # ToDo
        
        api = Api('path/')
        api.include('a', BookResource)
        api.include('b', BookResourceVersions)
        assert len( api.urlpatterns ) == 2*4
        for path in api.urlpatterns:
            assert path._regex.startswith('path/')
