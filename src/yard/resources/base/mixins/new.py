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
    
    def get_new_parameters(self):
        parameters = self.get_form_parameters(self.new)
        parameters.extend( self.get_header_parameters() )
        return parameters

    def get_new_responses(self):
        return {}

    def get_new_documentation(self):
        return self.operation_documentation('GET',
            responses = self.get_new_responses(),
            parameters = self.get_new_parameters(),
        )
          
    def handle_new(self, request, kwargs):
        response = self.new(request, **kwargs)
        return self.handle_response(request, response, self.fields, kwargs)

