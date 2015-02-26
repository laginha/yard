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
        return self.handle_response(request, response, self._meta.fields)

