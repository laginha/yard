#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client, RequestFactory
from yard.resources import Resource
from yard.resources.meta import model_to_fields
from yard.api import Api
from yard import fields as FIELDS
from yard.testcases.base import BaseTestCase
from books.models  import Book, Author


class TestResource(Resource):
    class Meta:
        model = Book
        

class JsonSerializerTestCase( BaseTestCase ):
    
    def setUp(self):
        super(JsonSerializerTestCase, self).setUp()
        self.api = Api()
        self.resource_class = TestResource
        self.resource = self.resource_class(self.api, {})
    
    def assert_json(self, objects, fields, json):
        assert len(json) == len(objects)
        for i in json:
            assert len(i) == len(fields)# + 1
            #assert 'resource_uri' in i
            for field in fields:
                assert field in i
    
    def build_json(self, objects, fields):
        return self.resource.serialize_all(objects, fields)
    
    def test_fields_with_list(self):
        objects = list(Book.objects.all())
        fields = model_to_fields(Book)
        json = self.build_json( objects, fields )
        self.assert_json( objects, fields, json )
        
    def test_default_fields_with_queryset(self):
        queryset = Book.objects.all()
        fields = model_to_fields(Book)
        json = self.build_json( queryset, fields )
        self.assert_json( queryset, fields, json )
    
    def test_one_to_one(self):    
        queryset = Book.objects.all()
        fields = {
            'id': FIELDS.Unicode,
            'author': {
                'id': FIELDS.Unicode,
                'name': FIELDS.Unicode,
            }
        }        
        json = self.build_json( queryset, fields )
        assert len(json) == queryset.count()
        for book in json:
            assert len(book) == len(fields)# + 1
            #assert 'resource_uri' in book
            assert 'id' in book
            assert 'author' in book
            assert 'id' in book['author']
            assert 'name' in book['author']
            #assert 'resource_uri' in book['author']

    def test_one_to_many(self):
        queryset = Author.objects.all()
        fields = {'id': FIELDS.Unicode,
            'book_set': {
                'id': FIELDS.Unicode,
                'name': FIELDS.Unicode,
            }
        }
        json = self.build_json( queryset, fields )
        assert len(json) == queryset.count()
        assert len(json[0]) == len(fields)# + 1
        for author in json:
            #assert 'resource_uri' in author
            assert 'id' in author
            assert 'book_set' in author
            assert isinstance(author['book_set'], list)
            assert len(author['book_set']) == Book.objects.filter(author__id=json[0]['id']).count()
            for book in author['book_set']:
                assert 'id' in book
                assert 'name' in book
                #assert 'resource_uri' in book
        