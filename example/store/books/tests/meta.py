#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.resources.utils.page import ResourcePage
from yard.resources.utils.meta import ResourceMeta
from yard.resources.utils.parameters import ResourceParameters
from books.tests.base import BaseTestCase
from books.models  import *


class MetaTestCase( BaseTestCase ):
    
    def setUp(self):
        super(MetaTestCase, self).setUp()
        self.pagination = ResourcePage(type("Pagination", (), {'results_per_page': {
            'parameter': 'results',
            'default': 1,
        }}))
        self.params = ResourceParameters()
        self.factory = RequestFactory()
        
    def get_resource_meta(self, meta=None):
        return ResourceMeta(self.pagination) if not meta else ResourceMeta(self.pagination, meta)
    
    def get_metadata(self, request, meta, objects):
        paged, page_params = self.pagination.select(request, objects)
        self.params.validated.update( page_params )
        return meta.generate( request, objects, paged, self.params )
        
    def assert_defaults_in_meta(self, metadata, value=True):
        assert ('total_objects' in metadata) == value
        assert ('validated_parameters' in metadata) == value
        assert ('paginated_objects' in metadata) == value
        assert ('next_page' in metadata) == value
        assert ('previous_page' in metadata) == value
    
    def assert_defaults_not_in_meta(self, metadata):
        self.assert_defaults_in_meta(metadata, False)
    
    def assert_aggregates_in_meta(self, metadata, value=True):
        assert ('avg_pages' in metadata) == value
        assert ('min_pages' in metadata) == value
        assert ('max_pages' in metadata) == value
        assert ('count_pages' in metadata) == value
        
    def assert_aggregates_not_in_meta(self, metadata):
        self.assert_aggregates_in_meta(metadata, False)
    
    def assert_default_meta_values(self, metadata, objects, paged, page_params):
        assert metadata['total_objects'] == len(objects)
        assert metadata['validated_parameters'] == page_params
        assert metadata['paginated_objects'] == len(paged)
        assert metadata['next_page']
        
    def assert_default_meta(self, request, objects):
        meta = self.get_resource_meta()
        paged, page_params = self.pagination.select(request, objects)
        self.params.validated.update( page_params )
        metadata = meta.generate( request, objects, paged, self.params )
        self.assert_defaults_in_meta( metadata )
        self.assert_aggregates_not_in_meta( metadata )
        assert 'no_meta' not in metadata
        self.assert_default_meta_values(metadata, objects, paged, page_params)
        return metadata
        
    def assert_no_meta(self, request, objects):
        meta = self.get_resource_meta(type('Meta', (), {
            'no_meta': True,
        }))
        metadata = self.get_metadata(request, meta, objects)
        self.assert_defaults_not_in_meta( metadata )
        self.assert_aggregates_not_in_meta( metadata )
        assert 'no_meta' not in metadata
        assert 'Errors' not in metadata
        return metadata

    def assert_custom_meta(self, request, objects):
        meta = self.get_resource_meta(type('Meta', (), {
           'number_of_objects_is_even': lambda x: not bool( len(x)%2 )
        }))
        metadata = self.get_metadata(request, meta, objects)
        assert 'number_of_objects_is_even' in metadata

    def test_custom(self):        
        request = self.factory.get('/books/')
        objects = Book.objects.all()
        self.assert_custom_meta( request, objects )
        objects = list(Book.objects.all())
        self.assert_custom_meta( request, objects )
        objects = [1,'a',2]
        self.assert_custom_meta( request, objects )
        objects = Book.objects.all().values()
        self.assert_custom_meta( request, objects )
    
    def test_defaults_with_queryset(self):
        objects = Book.objects.all()
        request = self.factory.get('/books/')
        self.assert_default_meta( request, objects )
        request = self.factory.get('/books/', {'offset': 1})
        self.assert_default_meta( request, objects )
        meta = self.get_resource_meta(type('Meta', (), {
            'with_errors': True,
            'validated_parameters': False,
            'total_objects': False,
            'paginated_objects': False,
            'next_page': False,
            'previous_page': False,
            'average': (('avg_pages', 'number_of_pages'),),
            'minimum': (('min_pages', 'number_of_pages'),),
            'maximum': (('max_pages', 'number_of_pages'),),
            'count': (('count_pages', 'number_of_pages'),),
        }))
        request = self.factory.get('/books/')
        metadata = self.get_metadata(request, meta, objects)
        self.assert_defaults_not_in_meta( metadata )
        assert 'no_meta' not in metadata
        assert 'Errors' in metadata
        self.assert_aggregates_in_meta(metadata)
        self.assert_no_meta(request, objects)
    
    def test_defaults_with_list(self):
        objects = list(Book.objects.all())
        request = self.factory.get('/books/')
        metadata = self.assert_default_meta( request, objects )
        assert metadata['previous_page'] == None
        self.assert_no_meta(request, objects)
    
    def test_defaults_with_valuesset(self):  
        objects = Book.objects.all().values()
        request = self.factory.get('/books/')
        metadata = self.assert_default_meta( request, objects )
        assert metadata['previous_page'] == None 
        self.assert_no_meta(request, objects)
