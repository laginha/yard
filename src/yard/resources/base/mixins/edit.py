class EditMixin(object):
    EDIT_ROUTES = {
        'GET': 'edit', 
    }
    
    @classmethod
    def as_edit_view(cls):
        return {
            'name': 'edit',
            'path': r'/(?P<pk>[0-9]+)/edit/?$',
            'routes': cls.EDIT_ROUTES,
        }

    def get_edit_parameters(self):
        parameters = self.get_form_parameters(self.edit)
        parameters.extend( self.get_header_parameters() )
        parameters.append( self.get_path_parameter() )
        return parameters

    def get_edit_responses(self):
        return {}

    def get_edit_documentation(self):
        return self.operation_documentation('GET',
            responses = self.get_edit_responses(),
            parameters = self.get_edit_parameters(),
        )

    def get_edit_documentation(self):
        return self.operation_documentation('GET', 
            parameters = self.get_detail_parameters(),
        )
    
    def handle_edit(self, request, kwargs):
        response = self.edit(request, kwargs.pop('pk'), **kwargs)
        return self.handle_response(request, response, self.fields, kwargs)

