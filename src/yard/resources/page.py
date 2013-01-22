#!/usr/bin/env python
# encoding: utf-8

from django.core.paginator import Paginator
from yard.utils            import is_generator


class ResourcePage(object):
    __defaults = [
        ('offset_parameter', None),
        ('results_per_page', None),
    ]

    def __init__(self, page):
        for k,v in self.__defaults:
            setattr(self, k, getattr(page,k) if hasattr(page, k) else v)
        self.__pre_select()
            
    def select(self, request, resources):
        offset, param1 = self.__offset( request.REQUEST )
        number, param2 = self.__number( request.REQUEST )
        return self.__paginate(resources, offset, number), dict(param1+param2)
        
    def __pre_select(self):
        if not self.results_per_page or not self.offset_parameter:
            self.select = lambda request,resources: (resources, {})
        else:
            self.__default = self.results_per_page['default']
            if 'parameter' not in self.results_per_page:
                self.__number = lambda request: (self.__default, [])
            if 'limit' not in self.results_per_page:
                self.__limit = lambda number: number
    
    def __limit(self, number):
        number = min(number, self.results_per_page['limit'])
        return number if number > 0 else self.__default
    
    def __number(self, request):
        parameter = self.results_per_page['parameter']
        number    = request.get(parameter, '')  
        if number.isdigit():
            number = self.__limit( int(number) )
            return number, [(parameter, number)]
        return self.__default, [(parameter, self.__default)]
    
    def __offset(self, request):
        offset = request.get(self.offset_parameter, '')
        if offset.isdigit():
            offset = max(0, int(offset))
            return offset, [(self.offset_parameter, offset)]
        return 0, [(self.offset_parameter, 0)]
    
    def __paginate(self, resources, offset, number):
        if is_generator( resources ):
            return self.__paginate_generator(resources, offset, number)
        return resources[offset:offset+number]
    
    def __paginate_generator(self, resources, offset, number):
        objects = []
        try:
            for i in range(offset): 
                resources.next()
            for i in range(number):
                objects.append( resources.next() )
            return objects
        except StopIteration:
            return objects
            
