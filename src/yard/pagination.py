#!/usr/bin/env python
# encoding: utf-8
from yard.utils import is_generator


class Pagination(object):
    '''
    Class responsible for resource pagination
    ''' 
    
    PAGINATION_OPTIONS = {
        'offset_parameter': 'offset',
        'results_parameter': 'results',
        'results_per_page': 25,
        'limit_per_page': 50,
        'no_pagination': False,
    }
    
    def __init__(self):
        for key,value in self.PAGINATION_OPTIONS.iteritems():
            if not hasattr(self, key):
                setattr(self, key, value)
    
    def select(self, request, resources):
        '''
        Paginate the resources according to Resource.Pagination attributes
        '''
        if self.no_pagination:
            return resources, {}
        offset, param1 = self.get_offset( request.REQUEST )
        number, param2 = self.get_number( request.REQUEST )
        return self.paginate(resources, offset, number), dict(param1+param2)
    
    def get_limit(self, number):
        '''
        Define the number of resources to return considering the default limit
        '''
        number = min(number, self.limit_per_page)
        return number if number > 0 else self.results_per_page
    
    def get_number(self, request):
        '''
        Define the real number of resources to return in the pagination
        '''
        number = request.get(self.results_parameter, '')  
        if number.isdigit():
            number = self.get_limit( int(number) )
            return number, [(self.results_parameter, number)]
        return self.results_per_page, [
            (self.results_parameter, self.results_per_page)
        ]
    
    def get_offset(self, request):
        '''
        Define the starting point for pagination
        '''
        offset = request.get(self.offset_parameter, '')
        if offset.isdigit():
            offset = max(0, int(offset))
            return offset, [(self.offset_parameter, offset)]
        return 0, [(self.offset_parameter, 0)]
    
    def paginate(self, resources, offset, number):
        '''
        Paginate the resources
        '''
        if is_generator( resources ):
            return self.paginate_generator(resources, offset, number)
        return resources[offset:offset+number]
    
    def paginate_generator(self, resources, offset, number):
        '''
        Paginate a generator based resources
        '''
        objects = []
        try:
            for i in range(offset): 
                resources.next()
            for i in range(number):
                objects.append( resources.next() )
            return objects
        except StopIteration:
            return objects
            
