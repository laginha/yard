#!/usr/bin/env python
# encoding: utf-8

BOOK_PARAMETERS = (
    { 'name':     'year',                           #query parameter name - required
      'alias':    'publication_date__year',         #actual name within server's logic - not required
      'required': False,                            #defaults to False - not required
      'limit':    lambda x: max(1970, min(2012, x)) #parameter's logic - not required
    },
    { 'name': 'title' },
    { 'and': (                                      # genre AND ( author OR house )
        { 'name': 'genre', 'alias': 'genres'},
        { 'or': (
            { 'name': 'author', 'alias': 'author__id' },                                      
            { 'name': 'house',  'alias': 'publishing_house__id' }, ) 
        }, )
    },
)

from yard.forms import Form, Parameter

class BookParameters(Form):
    name   = Parameter( alias='publication_date__year', limits=lambda x: max(1970, min(2012, x)) )
    title  = Parameter()
    genre  = Parameter( alias='genres' )
    author = Parameter( alias='author__id' )
    house  = Parameter( alias='publishing_house__id' ) 
    
    logic = name, title, genre & (author|house)

