#!/usr/bin/env python
# encoding: utf-8
from yard.utils import is_tuple
from .params.base import Parameter


class Form(object):
    '''
    Form for acceptable Resource parameters
    '''
    def __init__(self, parameters):
        
        def set_names(params):
            #Sets name attribute for all parameters in __logic__
            for param in params:
                param.set_name( attrs )
        
        attrs = parameters.__dict__
        is_param = lambda x: isinstance(x, Parameter)
        self.params = [param for name,param in attrs.items() if is_param(param)]
        if '__logic__' in attrs:
            self.logic = attrs['__logic__']
            if is_tuple( self.logic ):
                set_names( self.logic )
            elif isinstance(self.logic, Parameter):
                self.logic = (self.logic,)
                set_names( self.logic )
        else:
            self.logic = self.params
            set_names( self.logic )
    
    def __str__(self):
        return ' + '.join( [str(param) for param in self.logic] )          

    def get(self, request):
        '''
        Gets and validates parameters values in request
        '''
        for param in self.logic:
            yield param.get(request)
