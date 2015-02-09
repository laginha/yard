#!/usr/bin/env python
# encoding: utf-8
from yard.utils import is_generator


class ResourcePage(object):
    '''
    Class responsible for resource pagination
    ''' 
    DEFAULTS = {
        'offset_parameter': 'offset',
        'results_per_page': {
            'parameter': 'results',
            'default': 25,
            'limit': 50,
        },
        'no_pagination': False,
    }

    def __init__(self, page=type('Pagination', (), {})):
        for key,value in self.DEFAULTS.iteritems():
            set_value = getattr(page, key) if hasattr(page, key) else value
            setattr(self, key, set_value)
        self.pre_select()
        
    def pre_select(self):
        '''
        Optimize pagination process according to pagination attributes
        '''
        if self.no_pagination:
            self.select = lambda request,resources: (resources, {})
        else:
            if 'default' in self.results_per_page:
                self.default_number_of_objs = self.results_per_page['default']
            else:
                default = self.DEFAULTS['results_per_page']['default']
                self.default_number_of_objs = default
            if 'parameter' not in self.results_per_page:
                self.get_number = lambda r: (self.default_number_of_objs, [])
            if 'limit' not in self.results_per_page:
                self.get_limit = lambda number: number
    
    def select(self, request, resources):
        '''
        Paginate the resources according to Resource.Pagination attributes
        '''
        offset, param1 = self.get_offset( request.REQUEST )
        number, param2 = self.get_number( request.REQUEST )
        return self.paginate(resources, offset, number), dict(param1+param2)
    
    def get_limit(self, number):
        '''
        Define the number of resources to return considering the default limit
        '''
        number = min(number, self.results_per_page['limit'])
        return number if number > 0 else self.default_number_of_objs
    
    def get_number(self, request):
        '''
        Define the real number of resources to return in the pagination
        '''
        parameter = self.results_per_page['parameter']
        number    = request.get(parameter, '')  
        if number.isdigit():
            number = self.get_limit( int(number) )
            return number, [(parameter, number)]
        return self.default_number_of_objs, [
            (parameter, self.default_number_of_objs)
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
            
