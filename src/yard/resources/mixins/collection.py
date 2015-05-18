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
        if getattr(request, 'form', None):
            form = request.form
            if isinstance(form, (QueryForm, QueryModelForm)):
                parameters = form.get_validated_data()
            else:
                parameters = dict([
                    each for each in form.cleaned_data.iteritems() if each[1]
                ])
        else:
            parameters = {}
        return self.handle_response(
            request, response, self._meta.list_fields, parameters)
    
    def handle_create(self, request, kwargs):
        response = self.create(request, **kwargs)
        return self.handle_response(request, response, self._meta.fields)
    
