#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.api import Api
from yard.resources import Resource
from yard.testcases.base import BaseTestCase
from books.models  import *
from books.resources import BookResource, BookResourceVersions


class ApiTestCase( BaseTestCase ):
 
    def get_number_of_urls(self, resource):
        count = 0
        methods = [
            ['create', 'list'],
            ['update', 'destroy', 'detail'],
            ['new'], ['edit'],
        ]
        for each in methods:
            if any( hasattr(resource, i) for i in each ):
                count += 1
        return count
 
    def test_api_include(self):
        num_urls = self.get_number_of_urls(BookResource)
        api = Api()
        api.include('a', BookResource)
        api.include('b', BookResourceVersions)
        assert len( api.urlpatterns ) == 2*num_urls
        
        api = Api()
        api.include('a', BookResource, name='books')
        assert len( api.urlpatterns ) == num_urls
        viewnames = [each.name for each in api.urlpatterns]
        assert 'books.detail' in viewnames
        assert 'books.list' in viewnames
        assert 'books.edit' in viewnames
        assert 'books.new' in viewnames
        
        api = Api()
        api.include('b', BookResourceVersions)
        assert len( api.urlpatterns ) == num_urls
        viewnames = [each.name for each in api.urlpatterns]
        assert 'BookResourceVersions.detail' in viewnames
        assert 'BookResourceVersions.list' in viewnames
        assert 'BookResourceVersions.edit' in viewnames
        assert 'BookResourceVersions.new' in viewnames
        
        api = Api(discover=True)
        api.include('a', BookResource)
        api.include('b', BookResourceVersions)
        assert len( api.urlpatterns ) == 2*num_urls + 1
        viewnames = [each.name for each in api.urlpatterns]
        assert 'api_documentation' in viewnames

        api = Api('path/')
        api.include('a', BookResource)
        api.include('b', BookResourceVersions)
        assert len( api.urlpatterns ) == 2*num_urls
        for path in api.urlpatterns:
            assert path._regex.startswith('path/')
