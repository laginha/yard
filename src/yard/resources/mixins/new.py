class NewMixin(object):  
    NEW_ROUTES = {
        'GET': 'new', 
    }
    
    @classmethod
    def as_new_view(cls):
        return {
            'name': 'new',
            'path': r'/new/?$',
            'routes': cls.NEW_ROUTES,
        }
          
    def handle_new(self, request, kwargs):
        response = self.new(request, **kwargs)
        return self.handle_response(
            request, response, self._meta.fields, kwargs)
