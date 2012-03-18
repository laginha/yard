#!/usr/bin/env python
# encoding: utf-8

class RequiredParamMissing( Exception ):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Required parameter missing from request"
