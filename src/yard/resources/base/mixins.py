from .parameters import ResourceParameters


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
            'path': r'/(?P<pk>[0-9]+)/?$',
            'routes': cls.ELEMENT_ROUTES,
        }
        
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
    
    def handle_edit(self, request, kwargs):
        response = self.edit(request, kwargs.pop('pk'), **kwargs)
        return self.handle_response(request, response, self.fields, kwargs)


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
        return self.handle_response(request, response, self.fields, kwargs)

    
class OptionsMixin(object):
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
        return 200, {
            "List parameters": {
                'parameters':[
                    each.documentation for each in self.parameters.params
                ],
                'logic': unicode(self.parameters),
            },
        }
