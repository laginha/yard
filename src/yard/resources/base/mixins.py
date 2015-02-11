from django.shortcuts import get_object_or_404
from yard.consts import ALL_SWAGGER_RESPONSES
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
        
    def detail_documentation(self):
        return self.path_documentation('get', 
            path_parameter = True,
            success_schema = self.path_schema(self.detail_fields),
            responses = {
                404: ALL_SWAGGER_RESPONSES[404],
            },
        )
        
    def handle_detail_method(self, method, request, fields=None, **kwargs):
        instance = kwargs.pop('pk')
        if hasattr(self, "model"):
            instance = get_object_or_404(self.model, instance)
        response = method(request, instance, **kwargs)
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
    
    def list_documentation(self):
        if self.parameters:
            parameters = [
                each.documentation for each in self.parameters.params]
        else:
            parameters = []
        return self.path_documentation('get', 
            success_schema = self.path_schema(self.list_fields),
            parameters = parameters,
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
    
    @property
    def tagname(self):
        if hasattr(self, 'model'):
            return self.model.__name__.lower()
        return 'resource'
    
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
        return 200, self.full_documentation
    
    def full_documentation(self):
        result = []
        for http_method, method_name in self.routes.iteritems():
            if http_method == 'OPTIONS':
                continue
            if hasattr(self, method_name):
                doc_method_name = "%s_documentation" %method_name
                if hasattr(self, doc_method_name):
                    json_doc = getattr(self, doc_method_name)()
                else:
                    json_doc = self.path_documentation(http_method.lower())
                if json_doc:
                    result.append( json_doc )
        return result
        
    def path_documentation(self, http, path_parameter=False, 
                        success_schema=None, **kwargs):
        parameters = kwargs.get('parameters', [])
        responses = kwargs.get('responses', DEFAULT_SWAGGER_RESPONSES)
        if success_schema:
            if 200 not in responses:
                responses[200] = ALL_SWAGGER_RESPONSES[200]
            responses[200] = {k:v for k,v in responses[200].i()}
            responses[200]['schema'] = success_schema
        if path_parameter:
            parameters.append({
                'in': 'path', 
                'name': 'pk',
                'type': 'string', 
                'requred': True,
                'description': '%s identification' %self.tagname.capitalize(),
            })
        
        verb = self.routes[http.upper()]
        return {
            http: {
                'tags': kwargs.get('tags', [self.tagname]),
                'summary': kwargs.get('summary', 
                    '%s an existing %s' %(verb.capitalize(), self.tagname)),
                'description': kwargs.get('description', ''),
                'operationId': kwargs.get('operationId', 
                    '%s%s' %(verb, self.tagname.capitalize())),
                'consumes': kwargs.get('consumes', SWAGGER_CONTENT_TYPES),
                'produces': kwargs.get('produces', SWAGGER_CONTENT_TYPES),
                'security': kwargs.get('security', []),
                'parameters': parameters,
                'responses': responses,
            }
        }
        
        def path_schema(self, fields):
            result = {}
            if not fields:
                fields = self.fields
            for name,fieldtype in fields.iteritems():
                if isinstance(fieldtype, dict):
                    result[name] = self.path_schema(fieldtype)
                else:
                    result[name] = {'type': fieldtype.__name__.lower()}
            return result
