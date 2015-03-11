#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.resources import Resource
from yard.api import Api
from yard.testcases.base import BaseTestCase
from books.models  import *
import ujson

create_return_list          = lambda r, **p: range(10)
create_return_str           = lambda r, **p: 'foo'
create_return_int           = lambda r, **p: 200
create_return_dict          = lambda r, **p: {'foo': 'bar'}
create_return_none          = lambda r, **p: None
create_return_queryset      = lambda r, **p: Book.objects.all()
create_return_modelinstance = lambda r, **p: Book.objects.all()[0]
create_return_valuesset     = lambda r, **p: Book.objects.all().values('id')
create_return_tuple         = lambda r, **p: (500, 'ups')

list_return_list           = lambda r, **p: range(10)
list_return_str            = lambda r, **p: 'foo'
list_return_int            = lambda r, **p: 200
list_return_dict           = lambda r, **p: {'foo': 'bar'}
list_return_none           = lambda r, **p: None
list_return_queryset       = lambda r, **p: Book.objects.all()
list_return_modelinstance  = lambda r, **p: Book.objects.all()[0]
list_return_valuesset      = lambda r, **p: Book.objects.all().values('id')
list_return_tuple          = lambda r, **p: (500, 'ups')

element_return_list          = lambda r, id, **p: range(10)
element_return_str           = lambda r, id, **p: 'foo'
element_return_int           = lambda r, id, **p: 200
element_return_dict          = lambda r, id, **p: {'foo': 'bar'}
element_return_none          = lambda r, id, **p: None
element_return_queryset      = lambda r, id, **p: Book.objects.all()
element_return_modelinstance = lambda r, id, **p: Book.objects.get(pk=id)
element_return_valuesset     = lambda r, id, **p: Book.objects.all().values('id')
element_return_tuple         = lambda r, id, **p: (500, 'ups')


class TestResource(Resource):
    class Meta:
        model = Book
        

class ResourceHttpMethodsTestCase( BaseTestCase ):
    
    def setUp(self):
        super(ResourceHttpMethodsTestCase, self).setUp()
        self.factory = RequestFactory()
        self.collection_resource = TestResource(
            Api(), TestResource.as_list_view()['routes']
        )
        self.element_resource = TestResource(
            Api(), TestResource.as_detail_view()['routes']
        )
    
    def get_response(self, request, resource, params={}, 
            content_type="application/json", status=200):
        response = resource.handle_request(request, **params)
        assert response.status_code == status, response.status_code
        assert content_type in response['Content-Type'], response
        if content_type == "application/json":  
            return ujson.loads( response.content )
        return response.content
    
    def test_show_method(self):
        request = self.factory.get('/books/')
        self.element_method_test( request, 'detail' )
    
    def test_update_method(self):
        request = self.factory.post('/books/1')
        self.element_method_test( request, 'update' )
        request = self.factory.put('/books/1')
        self.element_method_test( request, 'update' )
        
    def test_destroy_method(self):
        request = self.factory.delete('/books/')
        self.element_method_test( request, 'destroy' )

    def element_method_test(self, request, method):
        setattr(self.element_resource, method, element_return_list)
        content = self.get_response( request, self.element_resource, 
            params={'pk':1} )
        assert isinstance(content, list)
        setattr(self.element_resource, method, element_return_str)
        content = self.get_response( request, self.element_resource, 
            params={'pk':1}, content_type="text/html" )
        assert isinstance(content, str)
        setattr(self.element_resource, method, element_return_int)
        content = self.get_response( request, self.element_resource, 
            params={'pk':1}, content_type="text/html" )
        assert not content
        setattr(self.element_resource, method, element_return_dict)
        content = self.get_response( request, self.element_resource, 
            params={'pk':1} )
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        setattr(self.element_resource, method, element_return_none)
        content = self.get_response( request, self.element_resource, 
            params={'pk':1}, content_type="text/html" )
        assert not content
        setattr(self.element_resource, method, element_return_queryset)
        content = self.get_response( request, self.element_resource, 
            params={'pk':1} )
        assert isinstance(content, list)
        setattr(self.element_resource, method, element_return_modelinstance)
        content = self.get_response( request, self.element_resource, 
            params={'pk':1})
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        setattr(self.element_resource, method, element_return_valuesset)
        content = self.get_response( request, self.element_resource, 
            params={'pk':1} )
        assert isinstance(content, list)
        setattr(self.element_resource, method, element_return_tuple)
        content = self.get_response( request, self.element_resource, 
            params={'pk':1}, status=500, content_type="text/html" )
        assert isinstance(content, str)

    def test_list_method(self):
        def get_response_content(list_function, **kwargs):
            self.collection_resource.list = list_function
            return self.get_response( request, self.collection_resource, **kwargs )
            
        request = self.factory.get('/books/')
        content = get_response_content( list_return_list )
        assert isinstance(content, dict)
        assert 'Objects' in content
        assert 'Meta' in content
        content = get_response_content( list_return_str, 
            content_type="text/html" )
        assert isinstance(content, str)
        content = get_response_content( list_return_int, 
            content_type="text/html" )
        assert not content
        content = get_response_content( list_return_dict )
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        content = get_response_content( list_return_none, 
            content_type="text/html" )
        assert not content
        content = get_response_content( list_return_queryset )
        assert isinstance(content, dict)
        assert 'Objects' in content
        assert 'Meta' in content
        content = get_response_content( list_return_modelinstance )
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        content = get_response_content( list_return_valuesset )
        assert isinstance(content, dict)
        assert 'Objects' in content
        content = get_response_content( list_return_tuple, 
            status=500, content_type="text/html" )
        assert isinstance(content, str)
    
    def test_create_method(self):
        def get_response_content(create_function, **kwargs):
            self.collection_resource.create = create_function
            return self.get_response( request, 
                self.collection_resource, **kwargs )
            
        request = self.factory.post('/books/')
        content = get_response_content( create_return_list )
        assert isinstance(content, list)
        content = get_response_content( create_return_str, 
            content_type="text/html" )
        assert isinstance(content, str)
        content = get_response_content( create_return_int, 
            content_type="text/html" )
        assert not content
        content = get_response_content( create_return_dict )
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        content = get_response_content( create_return_none, 
            content_type="text/html" )
        assert not content
        content = get_response_content( create_return_queryset )
        assert isinstance(content, list)
        content = get_response_content( create_return_modelinstance )
        assert isinstance(content, dict)
        content = get_response_content( create_return_valuesset )
        assert isinstance(content, list)
        content = get_response_content( create_return_tuple, 
            status=500, content_type="text/html" )
        assert isinstance(content, str)
