#!/usr/bin/env python
# encoding: utf-8

from yard.forms.form      import *
from yard.forms.parameter import Parameter
from yard.forms.params    import *


class QueryParameters(dict):
    def __init__(self, params={}):
        self.__errors   = {}
        self.update( params )

    def update(self, params):
        for key,value in params.items():
            if value:
                self[key] = value
            else:
                self.__errors[key] = str(value)

    def is_valid(self):
        return not bool(self.__errors)

    def errors(self):
        return {'ERRORS': self.__errors} if self.__errors else {}

