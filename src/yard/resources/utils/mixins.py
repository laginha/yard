from yard.forms import Form
from yard.resources.utils.parameters import ResourceParameters
from yard.resources.utils.preprocessor import ResourcePreprocessor


class DetailMixin(object):
    DETAIL_ROUTES = {
        'GET':'show', 
        'PUT':'update',
        'PATCH': 'update',
        'POST':'update', 
        'DELETE': 'destroy',
        'OPTIONS': 'options', 
    }
    
    @classmethod
    def as_detail_view(cls, api):
        return {
            'name': 'detail',
            'path': r'/(?P<pk>[0-9]+)/?$',
            'view': ResourcePreprocessor(
                api = api, 
                resource_class = cls,
                routes = cls.DETAIL_ROUTES,
                show_fields = getattr(cls, "show_fields", None),
            )
        }
    
    def handle_detail(self, method, request, fields=None, **kwargs):
        response = method(request, kwargs.pop('pk'), **kwargs)
        return self.handle_response(request, response, fields or self.fields, kwargs)
    
    def handle_show(self, request, **kwargs):
        return self.handle_detail(
            request = request,
            method  = self.show, 
            fields  = self.show_fields, 
            **kwargs
        )
    
    def handle_update(self, request, **kwargs):
        return self.handle_detail(
            request = request,
            method  = self.update, 
            **kwargs
        )
    
    def handle_destroy(self, request, **kwargs):
        return self.handle_detail(
            request = request,
            method  = self.destroy, 
            **kwargs
        )
    

class ListMixin(object):
    COLLECTION_ROUTES = {
        'GET':'index', 
        'POST':'create',
        'OPTIONS': 'options'
    }
    
    @classmethod
    def as_list_view(cls, api):
        return {
            'name': 'list',
            'path': r'/?$',
            'view': ResourcePreprocessor(
                api = api, 
                resource_class = cls,
                routes = cls.COLLECTION_ROUTES,
                index_fields = getattr(cls, "index_fields", None),
            ),
        }

    def get_resource_parameters(self, request, **kwargs):
        '''
        Gets parameters from resource request
        '''
        resource_params = ResourceParameters( kwargs )
        if not self.parameters:
            return resource_params
        for i in self.parameters.get( request ):
            resource_params.update( i )
        return resource_params

    def handle_index(self, request, **kwargs):
        parameters = self.get_resource_parameters( request, **kwargs )
        response = self.index(request, parameters)
        return self.handle_response(request, response, self.index_fields, parameters)
    
    def handle_create(self, request, **kwargs):
        response = self.create(request, **kwargs)
        return self.handle_response(request, response, self.fields, kwargs)
    

class EditMixin(object):
    EDIT_ROUTES = {
        'GET': 'edit', 
    }
    
    @classmethod
    def as_edit_view(cls, api):
        return {
            'name': 'edit',
            'path': r'/(?P<pk>[0-9]+)/edit/?$',
            'view': ResourcePreprocessor(
                api = api, 
                resource_class = cls,
                routes = cls.EDIT_ROUTES,
            )
        }

    def handle_edit(self, request, **kwargs):
        response = self.edit(request, kwargs.pop('pk'), **kwargs)
        return self.handle_response(request, response, self.fields, kwargs)


class NewMixin(object):
    NEW_ROUTES = {
        'GET': 'new', 
    }
    
    @classmethod
    def as_new_view(cls, api):
        return {
            'name': 'new',
            'path': r'/new/?$',
            'view': ResourcePreprocessor(
                api = api, 
                resource_class = cls,
                routes = cls.NEW_ROUTES,
            )
        }
        
    def handle_new(self, request, **kwargs):
        response = self.new(request, **kwargs)
        return self.handle_response(request, response, self.fields, kwargs)


class OptionsMixin(object):
    
    def get_allowed_methods(self):
        return [k for k,v in self.routes.items() if k!="OPTIONS" and hasattr(self, v)]
    
    def handle_options(self, request, **kwargs):
        response = self.options(request, **kwargs)
        response = self.handle_response(request, response, self.fields, kwargs)
        response['Allow'] = ','.join( self.get_allowed_methods() )
        return response
    
    def options(self, request, **kwargs):
        return 200, {
            "Index parameters": {
                'parameters':[
                    each.documentation for each in self.parameters.params
                ],
                'logic': unicode(self.parameters),
            },
        }
