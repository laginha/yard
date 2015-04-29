from .functions import (
    build_swagger_parameter, build_swagger_object, 
    build_swagger_schema, build_swagger_operation,)


class Documentation(object):
    
    def __init__(self, resource):
        self.resource = resource
    
    def get_documentation(self):
        result = {}
        for method_name in set(self.resource.routes.values()):
            if method_name == 'options':
                continue
            if not hasattr(self.resource, method_name):
                continue
            doc_method_name = "get_%s_documentation" %method_name
            json_doc = getattr(self, doc_method_name)()
            if json_doc: 
                result.update(json_doc)
        return result
    
    #
    # Auxiliar methods
    #
    
    def get_operation_documentation(self, http_method, parameters=None,
                                    responses=None, **kwargs):
        return build_swagger_operation(
            http_method = http_method, 
            verb = self.resource.routes[http_method],
            tagname = self.resource.tagname, 
            parameters = parameters, 
            responses = responses, 
            **kwargs )
    
    def get_response_schema(self, fields=None):
        fields = fields or self.resource._meta.fields
        if callable(fields):
            from django.test import TestCase, RequestFactory
            fields = fields(self.resource.Meta(), RequestFactory().get(''))
        return build_swagger_schema(fields or self.resource._meta.fields)
    
    def get_path_parameter(self):
        return build_swagger_parameter(preset='path')
    
    def get_header_parameters(self):
        if self.resource.version_name:
            return [build_swagger_parameter(
                preset = "http_accept", 
                default = self.resource.version_name,
            )]
        return []
    
    def get_form_parameters(self, method, params_type='form'):
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
                        location = params_type, 
                        name = each.name, 
                        typename = typename, 
                        description = each.field.help_text, 
                        required = each.field.required, 
                        items = items,
                        maximum = maximum, 
                        minimum = minimum, 
                        pattern = pattern,
                    )
                )
        return parameters
     
    #
    # LIST resource method
    #
    
    def get_list_parameters(self):
        parameters = self.get_form_parameters(
            self.resource.list, params_type='query')
        parameters.extend( self.get_header_parameters() )
        return parameters

    def get_list_responses(self):
        name = "%sList" % self.resource.tagname
        schema = self.get_response_schema(self.resource._meta.list_fields)
        return {
            200: {
                'description': 'Successful operation',
                'schema': {
                    'type': 'array',
                    'items': {"$ref": "#/definitions/%s"%name},
                    'schema_definition': {name: schema}
                }
            }
        }
    
    def get_list_documentation(self):
        return self.get_operation_documentation('GET', 
            parameters = self.get_list_parameters(),
            responses  = self.get_list_responses(),
        )
    
    #
    # CREATE resource method
    #
    
    def get_create_parameters(self):
        parameters = self.get_form_parameters(self.resource.create)
        parameters.extend( self.get_header_parameters() )
        return parameters
    
    def get_create_responses(self):  
        return {}  
    
    def get_create_documentation(self):
        return self.get_operation_documentation('POST',
            parameters = self.get_create_parameters(),
            responses = self.get_create_responses(),
        )
    
    #
    # DETAIL resource method
    #
    
    def get_detail_parameters(self):
        parameters = self.get_form_parameters(self.resource.detail)
        parameters.extend( self.get_header_parameters() )
        parameters.append( self.get_path_parameter() )
        return parameters
    
    def get_detail_responses(self):
        name = "%sDetail" % self.resource.tagname
        schema = self.get_response_schema(self.resource._meta.detail_fields)
        return {
            200: {
                'description': 'Successful operation',
                'schema': {"$ref": "#/definitions/%s"%name},
                'schema_definition': {name: schema}
            }
        }
        
    def get_detail_documentation(self):
        return self.get_operation_documentation('GET', 
            responses = self.get_detail_responses(),
            parameters = self.get_detail_parameters(),
        )
    
    #
    # UPDATE resource method
    #
    
    def get_update_parameters(self):
        parameters = self.get_form_parameters(self.resource.update)
        parameters.extend( self.get_header_parameters() )
        parameters.append( self.get_path_parameter() )
        return parameters

    def get_update_responses(self):
        return {}

    def get_update_documentation(self):
        return self.get_operation_documentation('PUT',
            responses = self.get_update_responses(),
            parameters = self.get_update_parameters(),
        )
    
    #
    # DETROY resource method
    #
    
    def get_destroy_parameters(self):
        parameters = self.get_form_parameters(self.resource.destroy)
        parameters.extend( self.get_header_parameters() )
        parameters.append( self.get_path_parameter() )
        return parameters

    def get_destroy_responses(self):
        return {}

    def get_destroy_documentation(self):
        return self.get_operation_documentation('DELETE',
            responses = self.get_destroy_responses(),
            parameters = self.get_destroy_parameters(),
        )
    
    #
    # EDIT resource method
    #
    
    def get_edit_parameters(self):
        parameters = self.get_form_parameters(self.resource.edit)
        parameters.extend( self.get_header_parameters() )
        parameters.append( self.get_path_parameter() )
        return parameters

    def get_edit_responses(self):
        return {}

    def get_edit_documentation(self):
        return self.get_operation_documentation('GET',
            responses = self.get_edit_responses(),
            parameters = self.get_edit_parameters(),
        )

    def get_edit_documentation(self):
        return self.get_operation_documentation('GET', 
            parameters = self.get_detail_parameters(),
        )
        
    #
    # NEW resource method
    #
    
    def get_new_parameters(self):
        parameters = self.get_form_parameters(self.resource.new)
        parameters.extend( self.get_header_parameters() )
        return parameters

    def get_new_responses(self):
        return {}

    def get_new_documentation(self):
        return self.get_operation_documentation('GET',
            responses = self.get_new_responses(),
            parameters = self.get_new_parameters(),
        )
