#!/usr/bin/env python
# encoding: utf-8

from yard.forms import Form, Parameter

class BookParameters(Form):
    year   = Parameter( alias='publication_date__year', limits=lambda x: max(1970, min(2012, x)) )
    title  = Parameter()
    genre  = Parameter( alias='genres' )
    author = Parameter( alias='author__id' )
    house  = Parameter( alias='publishing_house__id' ) 
    
    logic = year | title | genre #, house & (author|house), author
