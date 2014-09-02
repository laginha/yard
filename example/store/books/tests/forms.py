#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase
from yard.forms import Form, Parameter
from yard.forms.parameter import Logic, AND, OR

A = Parameter()
B = Parameter()
C = Parameter()
D = Parameter()
E = Parameter()

class SomeForm:
    a, b, c, d, e = A, B, C, D, E
    __logic__ = a, b&c&d, e|a|b, c&(d|e)&a, b|(c&d)|e


class FormTestCase(TestCase):
    
    def test_logic(self):
        form = Form( SomeForm )
        assert len(form.logic) == 5
        assert not isinstance(form.logic[0], Logic)
        assert form.logic[0] == A
        assert str(form.logic[0]) == 'a'
        
        assert isinstance(form.logic[1], AND)
        assert not isinstance(form.logic[1].y, Logic)
        assert form.logic[1].y == D
        assert isinstance(form.logic[1].x, AND)
        assert not isinstance(form.logic[1].x.x, Logic)
        assert form.logic[1].x.x == B
        assert not isinstance(form.logic[1].x.y, Logic)
        assert form.logic[1].x.y == C
        assert str(form.logic[1]) == "( ( b and c ) and d )"
        assert len(form.logic[1]) == 3
        
        assert isinstance(form.logic[2], OR)
        assert not isinstance(form.logic[2].x, Logic)
        assert form.logic[2].x == B
        assert isinstance(form.logic[2].y, OR)
        assert not isinstance(form.logic[2].y.x, Logic)
        assert form.logic[2].y.x == A
        assert not isinstance(form.logic[2].y.y, Logic)
        assert form.logic[2].y.y == E
        assert str(form.logic[2]) == "( b or ( a or e ) )"
        assert len(form.logic[2]) == 3
        
        assert isinstance(form.logic[3], AND)
        assert not isinstance(form.logic[3].y, Logic)
        assert form.logic[3].y == A
        assert isinstance(form.logic[3].x, AND)
        assert not isinstance(form.logic[3].x.x, Logic)
        assert form.logic[3].x.x == C
        assert isinstance(form.logic[3].x.y, Logic)
        assert not isinstance(form.logic[3].x.y.x, Logic)
        assert form.logic[3].x.y.x == E
        assert not isinstance(form.logic[3].x.y.y, Logic)
        assert form.logic[3].x.y.y == D
        assert str(form.logic[3]) == "( ( c and ( e or d ) ) and a )"
        assert len(form.logic[3]) == 4
        
        assert isinstance(form.logic[4], OR)
        assert not isinstance(form.logic[4].x, Logic)
        assert form.logic[4].x == E
        assert isinstance(form.logic[4].y, OR)
        assert not isinstance(form.logic[4].y.y, Logic)
        assert form.logic[4].y.y == B
        assert isinstance(form.logic[4].y.x, Logic)
        assert not isinstance(form.logic[4].y.x.x, Logic)
        assert form.logic[4].y.x.x == C
        assert not isinstance(form.logic[4].y.x.y, Logic)
        assert form.logic[4].y.x.y == D
        assert str(form.logic[4]) == "( e or ( ( c and d ) or b ) )"
        assert len(form.logic[4]) == 4
