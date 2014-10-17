#!/usr/bin/env python
# encoding: utf-8
from django.core.paginator import Paginator
from yard.utils            import is_generator


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
        for k,v in self.DEFAULTS.iteritems():
            setattr(self, k, getattr(page,k) if hasattr(page, k) else v)
        self.pre_select()
        
    def pre_select(self):
        '''
        Optimize pagination process according to pagination attributes
        '''
        if self.no_pagination:
            self.select = lambda request,resources: (resources, {})
        else:
            if 'default' in self.results_per_page:
                self.default_number_of_resources = self.results_per_page['default'] 
            else:
                self.default_number_of_resources = self.DEFAULTS['results_per_page']['default']
            if 'parameter' not in self.results_per_page:
                self.get_number_of_resources = lambda request: (self.default_number_of_resources, [])
            if 'limit' not in self.results_per_page:
                self.get_limit = lambda number: number
    
    def select(self, request, resources):
        '''
        Paginate the resources according to Resource.Pagination attributes
        '''
        offset, param1 = self.get_offset( request.REQUEST )
        number, param2 = self.get_number_of_resources( request.REQUEST )
        return self.paginate(resources, offset, number), dict(param1+param2)
    
    def get_limit(self, number):
        '''
        Define the number of resources to return considering the default limit
        '''
        number = min(number, self.results_per_page['limit'])
        return number if number > 0 else self.default_number_of_resources
    
    def get_number_of_resources(self, request):
        '''
        Define the real number of resources to return in the pagination
        '''
        parameter = self.results_per_page['parameter']
        number    = request.get(parameter, '')  
        if number.isdigit():
            number = self.get_limit( int(number) )
            return number, [(parameter, number)]
        return self.default_number_of_resources, [(parameter, self.default_number_of_resources)]
    
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
            
