#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.resources import Resource
from yard.api import Api
from books.tests.base import BaseTestCase
from books.models  import *
import simplejson

create_return_list = lambda request, **params: range(10)
create_return_str = lambda request, **params: 'foo'
create_return_int = lambda request, **params: 200
create_return_dict = lambda request, **params: {'foo': 'bar'}
create_return_none = lambda request, **params: None
create_return_queryset = lambda request, **params: Book.objects.all()
create_return_modelinstance = lambda request, **params: Book.objects.all()[0]
create_return_valuesset = lambda request, **params: Book.objects.all().values('id')
create_return_tuple = lambda request, **params: (500, 'ups')

index_return_list = lambda request, params: range(10)
index_return_str = lambda request, params: 'foo'
index_return_int = lambda request, params: 200
index_return_dict = lambda request, params: {'foo': 'bar'}
index_return_none = lambda request, params: None
index_return_queryset = lambda request, params: Book.objects.all()
index_return_modelinstance = lambda request, params: Book.objects.all()[0]
index_return_valuesset = lambda request, params: Book.objects.all().values('id')
index_return_tuple = lambda request, params: (500, 'ups')

single_return_list = lambda request, object_id, **params: range(10)
single_return_str = lambda request, object_id, **params: 'foo'
single_return_int = lambda request, object_id, **params: 200
single_return_dict = lambda request, object_id, **params: {'foo': 'bar'}
single_return_none = lambda request, object_id, **params: None
single_return_queryset = lambda request, object_id, **params: Book.objects.all()
single_return_modelinstance = lambda request, object_id, **params: Book.objects.get(pk=object_id)
single_return_valuesset = lambda request, object_id, **params: Book.objects.all().values('id')
single_return_tuple = lambda request, object_id, **params: (500, 'ups')


class ResourceHttpMethodsTestCase( BaseTestCase ):
    
    def setUp(self):
        super(ResourceHttpMethodsTestCase, self).setUp()
        self.factory = RequestFactory()
        self.collection_resource = Resource(Api(), {'get':'index', 'post':'create'})
        self.single_resource = Resource(Api(), {'get':'show', 'put':'update', 'post':'update', 'delete':'destroy'})
    
    def get_response(self, request, resource, params={}, content_type="application/json", status=200):
        response = resource(request, **params)
        assert response.status_code == status, response.status_code
        assert content_type in response['Content-Type']
        if content_type == "application/json":  
            return simplejson.loads( response.content )
        return response.content
    
    def test_show_method(self):
        request = self.factory.get('/books/')
        self.single_method_test( request, 'show' )
    
    def test_update_method(self):
        request = self.factory.post('/books/')
        self.single_method_test( request, 'update' )
        request = self.factory.put('/books/')
        self.single_method_test( request, 'update' )
        
    def test_destroy_method(self):
        request = self.factory.delete('/books/')
        self.single_method_test( request, 'destroy' )

    def single_method_test(self, request, method):
        setattr(self.single_resource, method, single_return_list)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, list)
        setattr(self.single_resource, method, single_return_str)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, str)
        setattr(self.single_resource, method, single_return_int)
        content = self.get_response( request, self.single_resource, params={'pk':1}, content_type="text/html" )
        assert not content
        setattr(self.single_resource, method, single_return_dict)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        setattr(self.single_resource, method, single_return_none)
        content = self.get_response( request, self.single_resource, params={'pk':1}, content_type="text/html")
        assert not content
        setattr(self.single_resource, method, single_return_queryset)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, list)
        setattr(self.single_resource, method, single_return_modelinstance)
        content = self.get_response( request, self.single_resource , params={'pk':1})
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        setattr(self.single_resource, method, single_return_valuesset)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, list)
        setattr(self.single_resource, method, single_return_tuple)
        content = self.get_response( request, self.single_resource, params={'pk':1}, status=500 )
        assert isinstance(content, str)

    def test_index_method(self):
        def get_response_content(index_function, **kwargs):
            self.collection_resource.index = index_function
            return self.get_response( request, self.collection_resource, **kwargs )
            
        request = self.factory.get('/books/')
        content = get_response_content( index_return_list )
        assert isinstance(content, dict)
        assert 'Objects' in content
        assert 'Meta' in content
        content = get_response_content( index_return_str )
        assert isinstance(content, str)
        content = get_response_content( index_return_int, content_type="text/html" )
        assert not content
        content = get_response_content( index_return_dict )
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        content = get_response_content( index_return_none, content_type="text/html" )
        assert not content
        content = get_response_content( index_return_queryset )
        assert isinstance(content, dict)
        assert 'Objects' in content
        assert 'Meta' in content
        content = get_response_content( index_return_modelinstance )
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        content = get_response_content( index_return_valuesset )
        assert isinstance(content, dict)
        assert 'Objects' in content
        content = get_response_content( index_return_tuple, status=500 )
        assert isinstance(content, str)
    
    def test_create_method(self):
        def get_response_content(index_function, **kwargs):
            self.collection_resource.create = index_function
            return self.get_response( request, self.collection_resource, **kwargs )
            
        request = self.factory.post('/books/')
        content = get_response_content( create_return_list )
        assert isinstance(content, list)
        content = get_response_content( create_return_str )
        assert isinstance(content, str)
        content = get_response_content( create_return_int, content_type="text/html" )
        assert not content
        content = get_response_content( create_return_dict )
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        content = get_response_content( create_return_none, content_type="text/html" )
        assert not content
        content = get_response_content( create_return_queryset )
        assert isinstance(content, list)
        content = get_response_content( create_return_modelinstance )
        assert isinstance(content, dict)
        content = get_response_content( create_return_valuesset )
        assert isinstance(content, list)
        content = get_response_content( create_return_tuple, status=500 )
        assert isinstance(content, str)

        
