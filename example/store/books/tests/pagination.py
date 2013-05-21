#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.resources.utils.page import ResourcePage
from books.tests.base import BaseTestCase
from books.models  import *


class PaginationTestCase( BaseTestCase ):
    
    def setUp(self):
        super(PaginationTestCase, self).setUp()
        objects = Book.objects.all()
        self.factory = RequestFactory()
    
    def assert_results_not_in_parameters(self, request, objects, pagination, offset=0):
        resources, parameters = pagination.select( request, objects )
        assert 'results' not in parameters
        assert 'offset' in parameters
        assert parameters['offset'] == offset
        assert len(resources) <= pagination.defaults[1][1]['default']

    def assert_page_params(self, request, objects, pagination, results_name='results', offset_name='offset', offset=0):
        resources, parameters = pagination.select( request, objects )
        assert results_name in parameters
        assert offset_name in parameters
        assert parameters[offset_name] == offset
        assert len(resources) <= parameters[results_name]
        return resources, parameters
        
    def basic_test(self, objects):
        request = self.factory.get('/books/')
        pagination = ResourcePage()
        resources, parameters = self.assert_page_params(request, objects, pagination)
        assert parameters['results'] == pagination.results_per_page['default']
        return resources
        
    def test_basic_with_queryset(self):
        objects = Book.objects.all()
        self.basic_test( objects )
        return objects
    
    def test_basic_with_list(self):
        objects = list(Book.objects.all())
        self.basic_test( objects )
        return objects

    def test_basic_with_valuesset(self):
        objects = Book.objects.all().values()
        self.basic_test( objects )
        return objects

    def offset_test(self, objects):
        pagination = ResourcePage()
        offset = 1
        request = self.factory.get('/books/', {'offset': offset})
        resources, parameters = self.assert_page_params(request, objects, pagination, offset=offset)
        assert parameters['results'] == pagination.results_per_page['default']
        return resources

    def test_offset_with_queryset(self):
        objects = Book.objects.all()
        assert self.offset_test( objects )[0] == self.test_basic_with_queryset()[1]
    
    def test_offset_with_list(self):
        objects = list(Book.objects.all())
        assert self.offset_test( objects )[0] == self.test_basic_with_list()[1]
    
    def test_offset_with_valuesset(self):
        objects = Book.objects.all().values()
        assert self.offset_test( objects )[0] == self.test_basic_with_valuesset()[1]

    def offset_parameter_test(self, objects):
        pagination = type("Pagination", (), {'offset_parameter': 'index'})
        pagination = ResourcePage(pagination)
        assert pagination.offset_parameter == 'index'
        offset = 1
        request = self.factory.get('/books/', {'index': offset})
        resources, parameters = self.assert_page_params(request, objects, pagination, offset_name='index', offset=offset)
        assert parameters['results'] == pagination.results_per_page['default']
        return resources

    def test_offset_parameter(self):
        objects = Book.objects.all()
        assert self.offset_parameter_test(objects)[0] == self.test_basic_with_queryset()[1]
    
    def test_offset_parameter(self):
        objects = list(Book.objects.all())
        assert self.offset_parameter_test(objects)[0] == self.test_basic_with_list()[1]
  
    def test_offset_parameter(self):
        objects = Book.objects.all().values()
        assert self.offset_parameter_test(objects)[0] == self.test_basic_with_valuesset()[1]

    def results_per_page_test(self, objects):
        pagination = type("Pagination", (), {'results_per_page': {
            'parameter': 'objects',
        }})
        pagination = ResourcePage(pagination)
        request = self.factory.get('/books/')
        resources, parameters = self.assert_page_params(request, objects, pagination, results_name='objects')
        assert parameters['objects'] == pagination.defaults[1][1]['default']
        assert 'results' not in parameters
        
        pagination = type("Pagination", (), {'results_per_page': {
            'parameter': 'objects',
        }})
        pagination = ResourcePage(pagination)
        request = self.factory.get('/books/', {'objects': 10})
        resources, parameters = self.assert_page_params(request, objects, pagination, results_name='objects')
        assert parameters['objects'] == 10
        
        pagination = type("Pagination", (), {'results_per_page': {
            'default': 100,
        }})
        pagination = ResourcePage(pagination)
        request = self.factory.get('/books/')
        self.assert_results_not_in_parameters( request, objects, pagination )
        request = self.factory.get('/books/', {'results': 10})
        self.assert_results_not_in_parameters( request, objects, pagination )
        
        pagination = type("Pagination", (), {'results_per_page': {
            'limit': 1,
        }})
        pagination = ResourcePage(pagination)
        request = self.factory.get('/books/')
        self.assert_results_not_in_parameters( request, objects, pagination )
        request = self.factory.get('/books/', {'results': 10})
        self.assert_results_not_in_parameters( request, objects, pagination )

        pagination = type("Pagination", (), {'results_per_page': {
            'parameter': 'objects',
            'default': 100,
        }})
        pagination = ResourcePage(pagination)
        request = self.factory.get('/books/')
        resources, parameters = self.assert_page_params( request, objects, pagination, results_name='objects')
        assert parameters['objects'] == pagination.results_per_page['default']
        assert 'results' not in parameters
        request = self.factory.get('/books/', {'objects': 10})
        resources, parameters = self.assert_page_params( request, objects, pagination, results_name='objects')
        assert 'results' not in parameters
        assert parameters['objects'] == 10
        
        pagination = type("Pagination", (), {'results_per_page': {
            'parameter': 'objects',
            'limit': 1,
        }})
        pagination = ResourcePage(pagination)
        request = self.factory.get('/books/')
        resources, parameters = self.assert_page_params( request, objects, pagination, results_name='objects')
        assert 'results' not in parameters
        assert parameters['objects'] == pagination.defaults[1][1]['default']
        request = self.factory.get('/books/', {'objects':10})
        resources, parameters = self.assert_page_params( request, objects, pagination, results_name='objects')
        assert 'results' not in parameters
        assert parameters['objects'] == pagination.results_per_page['limit']

    def test_results_per_page_with_queryset(self):
        objects = Book.objects.all()
        self.results_per_page_test( objects )

    def test_results_per_page_with_list(self):
        objects = list(Book.objects.all())
        self.results_per_page_test( objects )
   
    def test_results_per_page_with_valuesset(self):
        objects = Book.objects.all().values()
        self.results_per_page_test( objects )
    