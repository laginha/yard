from yard.forms import QueryForm, QueryModelForm


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
        parameters = self.get_form_parameters(self.list, params_type='query')
        parameters.extend( self.get_header_parameters() )
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

    def handle_list(self, request, kwargs):
        response = self.list(request, **kwargs)
        Parameters = type('Parameters', (dict,), {})
        if hasattr(request, 'form'):
            form = request.form
            if isinstance(form, (QueryForm, QueryModelForm)):
                parameters = Parameters( form.parameters )
                parameters.validated = form.non_empty_data
            else:
                parameters = Parameters( form.cleaned_data )
                parameters.validated = dict([
                    each for each in form.cleaned_data.items() if each[1]
                ])
        else:
            parameters = Parameters()
            parameters.validated = {}
        return self.handle_response(
            request, response, self.list_fields, parameters)
        # return self.handle_response(request, response, self.list_fields)
    
    def handle_create(self, request, kwargs):
        response = self.create(request, **kwargs)
        return self.handle_response(request, response, self.fields)
    
