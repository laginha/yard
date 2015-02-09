#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from keyauth.models import Key
from books.models  import *
from datetime import date
import json

books   = Book.objects
authors = Author.objects
houses  = Publishing.objects
genres  = Genre.objects


class BaseTestCase( TestCase ):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get_or_create( username='username' )[0]
        self.key = Key.objects.get_or_create( user=self.user )[0]
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
