#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.resources import Resource
from yard.api import Api
from books.tests.base import BaseTestCase
from books.models  import *
import simplejson

create_return_list          = lambda s, r, **p: range(10)
create_return_str           = lambda s, r, **p: 'foo'
create_return_int           = lambda s, r, **p: 200
create_return_dict          = lambda s, r, **p: {'foo': 'bar'}
create_return_none          = lambda s, r, **p: None
create_return_queryset      = lambda s, r, **p: Book.objects.all()
create_return_modelinstance = lambda s, r, **p: Book.objects.all()[0]
create_return_valuesset     = lambda s, r, **p: Book.objects.all().values('id')
create_return_tuple         = lambda s, r, **p: (500, 'ups')

index_return_list           = lambda s, r, p: range(10)
index_return_str            = lambda s, r, p: 'foo'
index_return_int            = lambda s, r, p: 200
index_return_dict           = lambda s, r, p: {'foo': 'bar'}
index_return_none           = lambda s, r, p: None
index_return_queryset       = lambda s, r, p: Book.objects.all()
index_return_modelinstance  = lambda s, r, p: Book.objects.all()[0]
index_return_valuesset      = lambda s, r, p: Book.objects.all().values('id')
index_return_tuple          = lambda s, r, p: (500, 'ups')

single_return_list          = lambda s, r, id, **p: range(10)
single_return_str           = lambda s, r, id, **p: 'foo'
single_return_int           = lambda s, r, id, **p: 200
single_return_dict          = lambda s, r, id, **p: {'foo': 'bar'}
single_return_none          = lambda s, r, id, **p: None
single_return_queryset      = lambda s, r, id, **p: Book.objects.all()
single_return_modelinstance = lambda s, r, id, **p: Book.objects.get(pk=id)
single_return_valuesset     = lambda s, r, id, **p: Book.objects.all().values('id')
single_return_tuple         = lambda s, r, id, **p: (500, 'ups')


class ResourceHttpMethodsTestCase( BaseTestCase ):
    
    def setUp(self):
        super(ResourceHttpMethodsTestCase, self).setUp()
        self.factory = RequestFactory()
        SomeResource = Resource
        #SomeResource.model = Book
        self.collection_resource = SomeResource.as_list_view(Api())['view']#.create_resource_instance()
        self.single_resource = SomeResource.as_detail_view(Api())['view']#.create_resource_instance()
    
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
        request = self.factory.post('/books/1')
        self.single_method_test( request, 'update' )
        request = self.factory.put('/books/1')
        self.single_method_test( request, 'update' )
        
    def test_destroy_method(self):
        request = self.factory.delete('/books/')
        self.single_method_test( request, 'destroy' )

    def single_method_test(self, request, method):
        resource_class = self.single_resource.get_resource_class()
        setattr(resource_class, method, single_return_list)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, list)
        setattr(resource_class, method, single_return_str)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, str)
        setattr(resource_class, method, single_return_int)
        content = self.get_response( request, self.single_resource, params={'pk':1}, content_type="text/html" )
        assert not content
        setattr(resource_class, method, single_return_dict)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        setattr(resource_class, method, single_return_none)
        content = self.get_response( request, self.single_resource, params={'pk':1}, content_type="text/html")
        assert not content
        setattr(resource_class, method, single_return_queryset)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, list)
        setattr(resource_class, method, single_return_modelinstance)
        content = self.get_response( request, self.single_resource , params={'pk':1})
        assert isinstance(content, dict)
        assert 'Objects' not in content
        assert 'Meta' not in content
        setattr(resource_class, method, single_return_valuesset)
        content = self.get_response( request, self.single_resource, params={'pk':1} )
        assert isinstance(content, list)
        setattr(resource_class, method, single_return_tuple)
        content = self.get_response( request, self.single_resource, params={'pk':1}, status=500 )
        assert isinstance(content, str)

    def test_index_method(self):
        def get_response_content(index_function, **kwargs):
            resource_class = self.collection_resource.get_resource_class()
            resource_class.index = index_function
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
        def get_response_content(create_function, **kwargs):
            resource_class = self.collection_resource.get_resource_class()
            resource_class.create = create_function
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

        
