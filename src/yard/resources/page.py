#!/usr/bin/env python
# encoding: utf-8

from django.core.paginator import Paginator

class ResourcePage(object):
    __defaults = [
        ('offset_parameter', None),
        ('results_per_page', None),
    ]

    def __init__(self, page):
        for k,v in self.__defaults:
            setattr(self, k, getattr(page,k) if hasattr(page, k) else v)
            
    def select(self, request, resources):
        if not self.results_per_page or not self.offset_parameter:
            return resources, {}
        return self.__paginate(request.REQUEST, resources)
    
    def __limit(self, number):
        if 'limit' in self.results_per_page:
            number = min(number, self.results_per_page['limit'])
            return number if number > 0 else self.results_per_page['default']
        return number
    
    def __number(self, request):
        default = self.results_per_page['default']
        if 'parameter' in self.results_per_page:
            parameter = self.results_per_page['parameter']
            number    = request.get(parameter, '')  
            if number.isdigit():
                number = self.__limit( int(number) )
                return number, [(parameter, number)]
            return default, [(parameter, default)]
        return default, []
    
    def __offset(self, request):
        offset = request.get(self.offset_parameter, '')
        if offset.isdigit():
            offset = max(0, int(offset))
            return offset, [(self.offset_parameter, offset)]
        return 0, [(self.offset_parameter, 0)]
    
    def __paginate(self, request, resources):
        offset, param1 = self.__offset( request )
        number, param2 = self.__number( request )
        objects = Paginator( resources[offset:], number ).page(1).object_list
        return objects, dict(param1+param2)
        
