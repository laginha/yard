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
        assert len( api.urlpatterns ) == 2*2
        
        api = Api()
        api.include('a', BookResource, single_name='single_name', collection_name='collection_name')
        assert len( api.urlpatterns ) == 2*1
        assert api.urlpatterns[0].name == 'single_name'
        assert api.urlpatterns[1].name == 'collection_name'
        
        api = Api()
        api.include('b', BookResourceVersions, single_name='single_name', collection_name='collection_name')
        assert len( api.urlpatterns ) == 2*1
        assert api.urlpatterns[0].name == 'single_name'
        assert api.urlpatterns[1].name == 'collection_name'
        
        api = Api(discover=True)
        api.include('a', BookResource)
        api.include('b', BookResourceVersions)
        # ToDo
        
        api = Api('path/')
        api.include('a', BookResource)
        api.include('b', BookResourceVersions)
        assert len( api.urlpatterns ) == 2*2
        for path in api.urlpatterns:
            assert path._regex.startswith('path/')
