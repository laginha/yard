#!/usr/bin/env python
# encoding: utf-8
import random, math
MAX = 10
MIN = 1

class Randomizer:
    '''
    Interface built over python module random
        https://gist.github.com/1254359
    '''

    def __init__(self):
        self.choice 		 = random.choice
        self.list   		 = lambda f,m: [ f() for i in range(0,m) ]
        self.comma_separated = lambda f,a: ','.join( f( a ) )			


    def number(self, mi=MIN, ma=MAX):
        return random.randint( mi, ma )
        
    def float(self, mi=MIN, ma=MAX):
        return self.number(mi,ma)/1.0

    def char(self):
        c = [ self.number(65, 90), self.number(97, 122) ]
        return chr( self.choice( c ) )
        
    def char_number(self):
        return chr( self.number(48,57) )

    def string(self, ma=MAX):
        return ''.join( self.list_of_chars( ma ) )

    def boolean(self):
        return self.number(0,1) == 1

    
    def comma_separated_number(self, ma=MAX):
        return self.comma_separated( self.list_of_char_numbers, ma )

    def comma_separated_char(self, ma=MAX):
        return self.comma_separated( self.list_of_chars, ma )

    def comma_separated_string(self, ma=MAX):
        return self.comma_separated( self.list_of_strings, ma )


    def list_of_char_numbers(self, ma=MAX):
        return self.list( self.char_number, ma )

    def list_of_numbers(self, ma=MAX):
        return self.list( self.number, ma )

    def list_of_chars(self, ma=MAX):
        return self.list( self.char, ma )

    def list_of_strings(self, ma=MAX):
        return self.list( self.string, ma )

