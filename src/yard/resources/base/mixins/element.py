from yard.utils.swagger import build_swagger_parameter


class ElementMixin(object):
    ELEMENT_ROUTES = {
        'GET':'detail', 
        'PUT':'update',
        'PATCH': 'update',
        'POST':'update', 
        'DELETE': 'destroy',
        'OPTIONS': 'options', 
    }
    
    @classmethod
    def as_detail_view(cls):
        return {
            'name': 'detail',
            'path': r'/(?P<pk>\d+)/?$',
            'routes': cls.ELEMENT_ROUTES,
        }
    
    def get_path_parameter(self):
        return build_swagger_parameter(preset='path')
    
    def get_detail_parameters(self):
        parameters = self.get_form_parameters(self.detail)
        parameters.extend( self.get_header_parameters() )
        parameters.append( self.get_path_parameter() )
        return parameters
    
    def get_detail_responses(self):
        def_name = "%sDetail"%self.tagname
        return {
            200: {
                'description': 'Successful operation',
                'schema': {"$ref": "#/definitions/%s"%def_name},
                'schema_definition': {
                    def_name: self.response_schema(self.detail_fields)
                }
            }
        }
        
    def get_detail_documentation(self):
        return self.operation_documentation('GET', 
            responses = self.get_detail_responses(),
            parameters = self.get_detail_parameters(),
        )
    
    def get_update_parameters(self):
        parameters = self.get_form_parameters(self.update)
        parameters.extend( self.get_header_parameters() )
        parameters.append( self.get_path_parameter() )
        return parameters

    def get_update_responses(self):
        return {}

    def get_update_documentation(self):
        return self.operation_documentation('PUT',
            responses = self.get_update_responses(),
            parameters = self.get_update_parameters(),
        )
    
    def get_destroy_parameters(self):
        parameters = self.get_form_parameters(self.destroy)
        parameters.extend( self.get_header_parameters() )
        parameters.append( self.get_path_parameter() )
        return parameters

    def get_destroy_responses(self):
        return {}

    def get_destroy_documentation(self):
        return self.operation_documentation('DELETE',
            responses = self.get_destroy_responses(),
            parameters = self.get_destroy_parameters(),
        )
        
    def handle_detail_method(self, method, request, fields=None, **kwargs):
        response = method(request, kwargs.pop('pk'), **kwargs)
        return self.handle_response(
            request, response, fields or self.fields, kwargs)
    
    def handle_detail(self, request, kwargs):
        return self.handle_detail_method(
            request = request, method = self.detail, 
            fields = self.detail_fields, **kwargs)
    
    def handle_update(self, request, kwargs):
        return self.handle_detail_method(
            request = request, method = self.update, 
            **kwargs)
    
    def handle_destroy(self, request, kwargs):
        return self.handle_detail_method(
            request = request, method = self.destroy, 
            **kwargs)
    
