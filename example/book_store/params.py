#!/usr/bin/env python
# encoding: utf-8

from yard.forms import *

class BookParameters(Form):
    year   = IntegerParam( alias='publication_date__year', min_value=1970, max_value=2012 )
    title  = CharParam()
    genre  = CharParam( alias='genres' )
    author = CharParam( alias='author__id' )
    house  = CharParam( alias='publishing_house__id' ) 
    
    logic = year, title, genre & (author|house)
