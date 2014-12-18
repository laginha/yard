from yard.forms import Form
from yard.resources.utils.parameters import ResourceParameters


class DetailMixin(object):
    DETAIL_ROUTES = {
        'GET':'show', 
        'PUT':'update', 
        'POST':'update', 
        'DELETE': 'destroy',
        'OPTIONS': 'options', 
    }
    
    @classmethod
    def as_detail_view(cls, api):
        return {
            'name': 'detail',
            'path': r'/(?P<pk>[0-9]+)/?$',
            'view': cls(api, cls.DETAIL_ROUTES,
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
        view = cls(api, cls.COLLECTION_ROUTES,
            index_fields = getattr(cls, "index_fields", None),
        )
        view.parameters = view.get_parameters()
        return {
            'name': 'list',
            'path': r'/?$',
            'view': view
        }
    
    def get_parameters(self):
        parameters = Form( self.Parameters ) if hasattr(self, "Parameters") else None
        if not parameters:
            self.get_resource_parameters = lambda r,p: ResourceParameters( p )
        return parameters

    def handle_index(self, request, **kwargs):
        parameters = self.get_resource_parameters( request, kwargs )
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
            'view': cls(api, cls.EDIT_ROUTES)
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
            'view': cls(api, cls.NEW_ROUTES)
        }
        
    def handle_new(self, request, **kwargs):
        response = self.new(request, **kwargs)
        return self.handle_response(request, response, self.fields, kwargs)
