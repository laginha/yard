#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.resources import MobileDrivenResource
from yard.api import Api
from yard import fields
from books.tests.base import BaseTestCase
from books.models  import *
from books.resources import AuthorResource
import simplejson

class TestResource(MobileDrivenResource):
    model = Book
    fields = {
        'author': fields.Link
    }

    def index(self, request, params):
        return Book.objects.filter( **params )

    def show(self, request, book_id):
        return Book.objects.get( id=book_id )


class MobileDrivenResourceTestCase( BaseTestCase ):

    def setUp(self):
        super(MobileDrivenResourceTestCase, self).setUp()
        self.factory = RequestFactory()
        SomeResource = TestResource
        self.api = Api()
        self.api.include('test', TestResource)
        self.collection_resource = self.api.urlpatterns[1]._callback
        self.single_resource = self.api.urlpatterns[0]._callback
        
    def test_index_method(self):
        def get_content():
            request = self.factory.get('/test/')
            response = self.collection_resource(request, **{})
            assert response.status_code == 200
            assert "application/json" in response['Content-Type']
            content = simplejson.loads( response.content )
            assert "Objects" in content
            assert "Meta" in content
            assert "Links" in content
            return content
            
        assert len(get_content()['Links']) == 1
        self.api.include('author', AuthorResource)
        assert len(get_content()['Links']) == 2
        
    def test_show_method(self):
        def get_content():
            request = self.factory.get('/test/1')
            response = self.single_resource(request, **{'pk':1})
            assert response.status_code == 200
            assert "application/json" in response['Content-Type']
            content = simplejson.loads( response.content )
            assert "Meta" not in content
            return content
        
        content = get_content()
        assert "Links" not in content
        assert "Object" not in content
        self.api.include('author', AuthorResource)
        content = get_content()
        assert "Links" in content
        assert len(content['Links']) == 1
    