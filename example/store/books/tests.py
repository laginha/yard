#!/usr/bin/env python
# encoding: utf-8
from django.test.client import Client
from yard.testcases.base import BaseTestCase
from books.models  import *
from datetime import date
import json

books   = Book.objects
authors = Author.objects
houses  = Publishing.objects
genres  = Genre.objects


class BookStoreTestCase( BaseTestCase ):
    
    def get(self, status=200, **params):
        response = self.client.get( '/books/', params )
        assert response.status_code == status, "%s-%s - %s" %(status, response.status_code, response.content)
        try:
            jdict = json.loads( response.content )
            return jdict['Objects'] if 'Objects' in jdict else jdict
        except (ValueError, KeyError) as e:
            assert False, "%s\n%s" %(e, response.content)
    
    def test_pagination(self):
        self.get()
        response = self.get( offset=0, results=1 )
        assert len(response) == 1, response
        response = self.get( offset=1, results=1 )
        assert len(response) == 1, response
        response = self.get( offset=2, results=1 )
        assert len(response) == 1, response
        response = self.get( offset=3, results=1 )
        assert len(response) == 0, response
        response = self.get( offset=0, results=2 )
        assert len(response) == 2, response
        response = self.get( offset=1, results=2 )
        assert len(response) == 2, response
        response = self.get( offset=2, results=2 )
        assert len(response) == 1, response
        response = self.get( offset=3, results=2 )
        assert len(response) == 0, response
    
    def test_year_param(self):
        self.get( 200, year=1996 )
        self.get( 200, year=2005 )        
        self.get( 200, year=2012 )
        
    def test_title_param(self):
        response = self.get( title='A Game of Thrones' )
        assert len(response) == 1, response
        assert int(response[0]['id']) == self.book1.id, (int(response[0]['id']), self.book1.id)
        response = self.get( title='A Feast for Crows' )
        assert len(response) == 1, response
        assert int(response[0]['id']) == self.book2.id, (int(response[0]['id']), self.book1.id)
        response = self.get( title='Some title' )
        assert len(response) == 0, response
      
    def test_year_and_title_params(self):
        response = self.get( title='A Game of Thrones', year=1996 )
        assert len(response) == 1, response
        assert int(response[0]['id']) == self.book1.id, (int(response[0]['id']), self.book1.id)
        response = self.get( title='A Game of Thrones', year=2005 )
        assert len(response) == 0, response
        response = self.get( title='A Feast for Crows', year=2005 )
        assert len(response) == 1, response
        assert int(response[0]['id']) == self.book2.id, (int(response[0]['id']), self.book1.id)
        response = self.get( title='A Feast for Crows', year=1996 )
        assert len(response) == 0, response
        response = self.get( title='Some title', year=2012 )
        assert len(response) == 0, response
        
    def test_AND_params(self):
        self.get( 400, genre=self.genre1.id )        
        self.get( genre=self.genre1.id, author=self.author.id )
        self.get( genre=self.genre1.id, house=self.house.id )
        self.get( author=self.author.id, genre=self.genre1.id, house=self.house.id )  
        self.get( 400, author=self.author.id, house=self.house.id )
    
    def test_show(self):
        response = self.client.get( '/books/%s/' %self.book1.id )
        assert response.status_code == 401, response.status_code 
        response = self.client.get( '/books/%s/' %self.book1.id, {'key':self.key.token} )
        assert response.status_code == 200, response.status_code
        response = json.loads( response.content )
        assert int(response['id']) == self.book1.id, (int(response['id']), self.book1.id)
        response = self.client.get( '/books/%s/' %self.book2.id )
        assert response.status_code == 401, response.status_code   
        response = self.client.get( '/books/%s/' %self.book2.id, {'key':self.key.token} )
        assert response.status_code == 200, response.status_code
        response = json.loads( response.content )
        assert int(response['id']) == self.book2.id, (int(response['id']), self.book2.id)
           
    def test_create(self):
        response = self.client.post( '/books/' )
        assert response.status_code == 401, response.status_code
    
    def test_update(self):
        response = self.client.post( '/books/%s/' %self.book1.id )
        assert response.status_code == 405, response.status_code
     
    def test_destroy(self):
        response = self.client.delete( '/books/%s/' %self.book1.id )
        assert response.status_code == 405, response.status_code
