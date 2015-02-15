from yard.resources.base.parameters import ResourceParameters


class CollectionMixin(object):
    COLLECTION_ROUTES = {
        'GET':'list', 
        'POST':'create',
        'OPTIONS': 'options'
    }
    
    @classmethod
    def as_list_view(cls):
        return {
            'name': 'list',
            'path': r'/?$',
            'routes': cls.COLLECTION_ROUTES,
        }
    
    def get_list_parameters(self):
        parameters = self.get_form_parameters(self.list)
        parameters.extend( self.get_header_parameters() )
        if self.parameters:
            parameters.extend([
                each.get_documentation() for each in self.parameters.params
            ])
        return parameters

    def get_list_responses(self):
        def_name = "%sList"%self.tagname
        return {
            200: {
                'description': 'Successful operation',
                'schema': {
                    'type': 'array',
                    'items': {"$ref": "#/definitions/%s"%def_name},
                    'schema_definition': {
                        def_name: self.response_schema(self.list_fields)
                    }
                }
            }
        }
    
    def get_list_documentation(self):
        return self.operation_documentation('GET', 
            parameters = self.get_list_parameters(),
            responses  = self.get_list_responses(),
        )
    
    def get_create_parameters(self):
        parameters = self.get_form_parameters(self.create)
        parameters.extend( self.get_header_parameters() )
        return parameters
    
    def get_create_responses(self):  
        return {}  
    
    def get_create_documentation(self):
        return self.operation_documentation('POST',
            parameters = self.get_create_parameters(),
            responses = self.get_create_responses(),
        )
    
    def get_resource_parameters(self, request, **kwargs):
        '''
        Gets parameters from resource request
        '''
        resource_params = ResourceParameters( kwargs )
        if not self.parameters:
            return resource_params
        for each in self.parameters.get( request ):
            resource_params.update( each )
        return resource_params

    def handle_list(self, request, kwargs):
        parameters = self.get_resource_parameters( request, **kwargs )
        response = self.list(request, parameters)
        return self.handle_response(
            request, response, self.list_fields, parameters)
    
    def handle_create(self, request, kwargs):
        response = self.create(request, **kwargs)
        return self.handle_response(request, response, self.fields, kwargs)
    
