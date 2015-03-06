from yard.swagger.functions import (
    build_swagger_operation, build_swagger_schema, build_swagger_parameter)


class OptionsMixin(object):
    
    def get_allowed_methods(self):
        allowed_methods = []
        for http_method, resource_method in self.routes.items():
             if http_method != "OPTIONS" and hasattr(self, resource_method):
                 allowed_methods.append( http_method )
        return allowed_methods
        
    def handle_options(self, request, kwargs):
        response = self.options(request, **kwargs)
        response = self.handle_response(
            request, response, self._meta.fields)
        response['Allow'] = ','.join( self.get_allowed_methods() )
        return response
    
    def options(self, request, **kwargs):
        return 200, self.get_documentation()
       
    def get_documentation(self):
        return self._meta.documentation.get_documentation()
