from django.utils       import unittest
from django.test.client import Client
from book_store.models  import *

from datetime import date
import json


books   = Book.objects
authors = Author.objects
houses  = Publishing.objects
genres  = Genre.objects



class Book_TestCase( unittest.TestCase ):
    def setUp(self):
        self.client = Client()
        self.genre1 = genres.get_or_create( name='Dark Fantasy' )[0]
        self.genre2 = genres.get_or_create( name='Medieval Fantasy' )[0]
        self.genre3 = genres.get_or_create( name='High Fantasy' )[0]
        self.author = authors.get_or_create( name='George R.R. Martin', gender='M', birthday=date(1948,9,20) )[0]
        self.house  = houses.get_or_create( name='Bantam Books' )[0]
        self.book1  = books.get_or_create( title            = 'A Game of Thrones', 
                                           author           = self.author, 
                                           publishing_house = self.house,
                                           publication_date = date(1996,8,6) )[0]
        self.book1.genres = genres.all()
        self.book1.save()
        self.book2  = books.get_or_create( title            = 'A Feast for Crows', 
                                           author           = self.author, 
                                           publishing_house = self.house,
                                           publication_date = date(2005,10,17) )[0]
        self.book2.genres = genres.all()
        self.book2.save()
        self.book3  = books.get_or_create( title            = 'A Clash of Kings', 
                                           author           = self.author, 
                                           publishing_house = self.house,
                                           publication_date = date(1999,2,1) )[0]
        
        
    def get(self, status=200, **params):
        response = self.client.get( '/books/', params )
        assert response.status_code == status, "%s-%s - %s" %(status, response.status_code, response.content)
        try:
            jdict = json.loads( response.content )
            return jdict['Objects'] if 'Objects' in jdict else jdict
        except (ValueError, KeyError) as e:
            assert False, "%s\n%s" %(e, response.content)
    
    
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
        
    
    def test_show(self):
        response = self.client.get( '/books/%s/' %self.book1.id )
        assert response.status_code == 200, response.status_code 
        response = json.loads( response.content )
        assert int(response['id']) == self.book1.id, (int(response['id']), self.book1.id)
        
        response = self.client.get( '/books/%s/' %self.book2.id )
        assert response.status_code == 200, response.status_code   
        response = json.loads( response.content )
        assert int(response['id']) == self.book2.id, (int(response['id']), self.book2.id)
        
    
    def test_create(self):
        response = self.client.post( '/books/' )
        assert response.status_code == 405, response.status_code
    
    
    def test_update(self):
        response = self.client.post( '/books/%s/' %self.book1.id )
        assert response.status_code == 200, response.status_code
    
        
    def test_destroy(self):
        response = self.client.delete( '/books/%s/' %self.book1.id )
        assert response.status_code == 401, response.status_code
    
        
        