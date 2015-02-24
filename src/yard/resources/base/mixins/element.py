from yard.swagger.functions import build_swagger_parameter


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
    
    def handle_detail(self, request, kwargs):
        response = self.detail(request, kwargs.pop('pk'), **kwargs)
        return self.handle_response(request, response, self.detail_fields)
    
    def handle_update(self, request, kwargs):
        response = self.update(request, kwargs.pop('pk'), **kwargs)
        return self.handle_response(request, response, self.fields)

    def handle_destroy(self, request, kwargs):
        response = self.destroy(request, kwargs.pop('pk'), **kwargs)
        return self.handle_response(request, response, self.fields)
    
