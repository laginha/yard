#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.metadata import Metadata
from yard.pagination import Pagination
from yard.forms import Parameters
from yard.testcases.base import BaseTestCase
from books.models  import *


class TestPagination(Pagination):
    results_per_page = 1
    results_parameter = 'results'


class MetadataTestCase( BaseTestCase ):
    
    def setUp(self):
        super(MetadataTestCase, self).setUp()
        self.pagination = TestPagination()
        self.params = Parameters.create()
        self.factory = RequestFactory()

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
        meta = Metadata(self.pagination)
        paged, page_params = self.pagination.select(request, objects)
        self.params.validated.update( page_params )
        metadata = meta.generate( request, objects, paged, self.params )
        self.assert_defaults_in_meta( metadata )
        self.assert_aggregates_not_in_meta( metadata )
        assert 'no_meta' not in metadata
        self.assert_default_meta_values(metadata, objects, paged, page_params)
        return metadata
        
    def assert_no_meta(self, request, objects):
        
        class TestMetadata(Metadata):
            no_meta = True
        
        metadata = self.get_metadata(
            request, TestMetadata(self.pagination), objects)
        self.assert_defaults_not_in_meta( metadata )
        self.assert_aggregates_not_in_meta( metadata )
        assert 'no_meta' not in metadata
        return metadata

    def assert_custom_meta(self, request, objects):
        
        class TestMetadata(Metadata):
            custom = {
                'number_of_objects_is_even': (lambda x: not bool( len(x)%2 ))
            }
        
        meta = TestMetadata(self.pagination)
        metadata = self.get_metadata(
            request, meta, objects)
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
        
        class TestMetadata(Metadata):
            validated_parameters = False
            total_objects = False
            paginated_objects = False
            next_page = False
            previous_page = False
            average = (('avg_pages', 'number_of_pages'),)
            minimum = (('min_pages', 'number_of_pages'),)
            maximum = (('max_pages', 'number_of_pages'),)
            count   = (('count_pages', 'number_of_pages'),)
        
        request = self.factory.get('/books/')
        metadata = self.get_metadata(
            request, TestMetadata(self.pagination), objects)
        self.assert_defaults_not_in_meta( metadata )
        assert 'no_meta' not in metadata
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
