#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.resources import Resource
from yard.api import Api
from yard.serializers import MobileSerializer
from yard import fields
from yard.testcases.base import BaseTestCase
from books.models  import *
from books.resources import AuthorResource
import ujson


class TestResource(Resource):
    class Meta:
        serializer = MobileSerializer
        model = Book
        fields = {
            'author': fields.Link
        }

    def list(self, request):
        return Book.objects.all()

    def detail(self, request, book_id):
        return Book.objects.get( id=book_id )


class MobileDrivenResourceTestCase( BaseTestCase ):

    def setUp(self):
        super(MobileDrivenResourceTestCase, self).setUp()
        self.factory = RequestFactory()
        self.api = Api()
        self.api.include('test', TestResource)
        self.collection_resource = [
            i._callback for i in self.api.urlpatterns if '.list' in i.name][0]
        self.single_resource = [
            i._callback for i in self.api.urlpatterns if '.detail' in i.name][0]
        
    def test_list_method(self):
        def get_content():
            request = self.factory.get('/test/')
            response = self.collection_resource(request, **{})
            assert response.status_code == 200, response.status_code
            assert "application/json" in response['Content-Type']
            content = ujson.loads( response.content )
            assert "Objects" in content
            assert "Meta" in content
            assert "Links" in content
            return content
        
        assert len(get_content()['Links']) == 1
        self.api.include('author', AuthorResource)
        assert len(get_content()['Links']) == 2
        
    def test_detail_method(self):
        def get_content():
            request = self.factory.get('/test/1')
            response = self.single_resource(request, **{'pk':1})
            assert response.status_code == 200
            assert "application/json" in response['Content-Type']
            content = ujson.loads( response.content )
            assert "Meta" not in content
            return content
        
        content = get_content()
        assert "Links" not in content
        assert "Object" not in content
        self.api.include('author', AuthorResource)
        content = get_content()
        assert "Links" in content
        assert len(content['Links']) == 1
    