# API Documentation

*Yard* provides a module for API documentation and discovery, based on [Swagger](http://swagger.io/). To enable this feature, in your `urls.py` do as follows:

```python
from yard.api import Api

api = Api(discover=True)
...
urlpatterns = api.urlpatterns
```

by doing so, the root of your API will return a JSON representation documenting the API, according to the [Swagger 2.0 specification](https://github.com/swagger-api/swagger-spec).

Moreover, every resource has the `OPTIONS` method impemented by default, which returns the JSON representation documenting the Resource, also according to the [Swagger 2.0 specification](https://github.com/swagger-api/swagger-spec).


## Swagger-UI

You can include the [Swagger-ui](https://github.com/swagger-api/swagger-ui) to visualize and consume your own restful services.

```python
# settings.py
INSTALLED_APPS = (
    ...
    'yard.swagger', 
    ...
)
```

```python
# urls.py
urlpatterns += patterns('',
    url(r'^doc/', include('yard.swagger.urls')),
)
```

> check this [live example](http://petstore.swagger.io/)


## Include form fields

To include `django.form.fields` in the API documentation, user the `validate` decorator. This decorator, besides checking the validity of the request according to the given form, binds the form to the method so the API Documentation module may access it and build the JSON accordingly.

```python
from yard.resources import Resource
from yard.decorators import validate

class BookResource(Resource):
    class Meta:
        model = models.Book
    
    @validate(BookCreateForm)
    def create(self, request):
        data = request.form.cleaned_data
        ...
```    

> Learn more about [*Yard* decorators](/laginha/yard/blob/develop/docs/decorators.md)!


## Customize

```python 
from yard.swagger import Documentation

class CustomDocumentation(Documentation):
    ...
```

```python 
from yard import resources

class Book(resources.Resource):
    class Meta:
        model = models.Book
        documentation = CustomDocumentation
```

To customize the `Documentation` class, there are some things you need to know:

1. `__init__` take one argument only: the resource
2. for every *CRUD* method (`list`, `detail`, `create`, `update`, `destroy`, `new` and `edit`) there are three methods, called in the following order:
    1. `get_<method>_documentation`
    2. `get_<method>_parameters`
    3. `get_<method>_responses`
