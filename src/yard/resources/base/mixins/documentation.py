from yard.utils.swagger import (
    build_swagger_operation, build_swagger_schema, build_swagger_parameter)


class DocumentationMixin(object):
    
    def get_allowed_methods(self):
        allowed_methods = []
        for http_method, resource_method in self.routes.items():
             if http_method != "OPTIONS" and hasattr(self, resource_method):
                 allowed_methods.append( http_method )
        
    def handle_options(self, request, kwargs):
        response = self.options(request, **kwargs)
        response = self.handle_response(request, response, self.fields, kwargs)
        response['Allow'] = ','.join( self.get_allowed_methods() )
        return response
    
    def options(self, request, **kwargs):
        return 200, self.get_documentation()
    
    def get_header_parameters(self):
        if self.version_name:
            return [build_swagger_parameter(
                preset  = "http_accept", 
                default = self.version_name,
            )]
        return []
    
    def get_form_parameters(self, method):
        def get_typename(widget): 
            if getattr(widget, 'input_type', '') == 'number':
                return 'number', None
            elif getattr(widget, 'allow_multiple_selected', False):
                return 'array', {'type': 'string'}
            return 'string', None
            
        parameters = []
        if hasattr(method, 'form_class'):
            for each in method.form_class():
                maximum = minimum = pattern = None
                for validator in each.field.validators:
                    if validator.code.startswith('max_'):
                        maximum = validator.limit_value
                    elif validator.code.startswith('min_'):
                        minimum = validator.limit_value
                    if hasattr(validator, 'regex'):
                        pattern = validator.regex
                typename, items = get_typename(each.field.widget)
                parameters.append( 
                    build_swagger_parameter(
                        location    = 'form', 
                        name        = each.name, 
                        typename    = typename,
                        description = each.field.help_text, 
                        required    = each.field.required,
                        items       = items,
                        maximum     = maximum,
                        minimum     = minimum,
                        pattern     = pattern,
                    )
                )
        return parameters
    
    def get_documentation(self):
        result = {}
        for method_name in set(self.routes.values()):
            if method_name=='options' or not hasattr(self, method_name):
                continue
            doc_method_name = "get_%s_documentation" %method_name
            json_doc = getattr(self, doc_method_name)()
            if json_doc:
                result.update( json_doc )
        return result
        
    def operation_documentation(self, http_method, parameters=None, 
                                responses=None, **kwargs):
        return build_swagger_operation(
            http_method = http_method,
            verb        = self.routes[http_method],
            tagname     = self.tagname,
            parameters  = parameters, 
            responses   = responses,
            **kwargs
        )
        
    def response_schema(self, fields=None):
        return build_swagger_schema(fields or self.fields)
