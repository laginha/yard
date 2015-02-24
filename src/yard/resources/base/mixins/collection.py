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
    
    def handle_create(self, request, kwargs):
        response = self.create(request, **kwargs)
        return self.handle_response(request, response, self.fields)
    
