from yard.forms import QueryForm, QueryModelForm, Parameters


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

    def handle_list(self, request, kwargs):
        response = self.list(request, **kwargs)
        if hasattr(request, 'form'):
            parameters = Parameters.create(request.form)
        else:
            parameters = Parameters.create()
        return self.handle_response(
            request, response, self._meta.list_fields, parameters)
    
    def handle_create(self, request, kwargs):
        response = self.create(request, **kwargs)
        return self.handle_response(request, response, self._meta.fields)
    
