# Decorators


## validate

Check if resource's parameters are valid. If not, returns a *JSON* response with the errors encountered during validation process. 

```python
from yard.resources.decorators import validate
from yard import resources, forms

class BookResource(resources.Resource):
    class Parameters:
        ...

    @validate
    def index(self, request, params):
        return Book.objects.filter( **params )
```


## login_required

Check if user is authenticated. 

Uses the *django's* `login_required` decorator thus it accepts the same arguments plus an extra one:

- `redirect`: determines whether it should redirect to the login url or return a *Not Authorized* response (status 401), if the user is not authenticated. (defaults to `False`)

```python
from yard.resources.decorators import login_required
from yard import resources

class BookResource(resources.Resource):

    @login_required()
    def index(self, request, params):
        return Book.objects.filter( **params )
```


## permission_required

Check if user has the required permissions. 

Uses the *django's* `permission_required` decorator thus it accepts the same arguments plus an extra one:

- `redirect`: determines whether it should redirect to the login url or return a *Not Authorized* response (status 401), if the user is not authenticated. (defaults to `False`)

```python
from yard.resources.decorators import permission_required
from yard import resources

class BookResource(resources.Resource):

    @permission_required('books.can_read')
    def index(self, request, params):
        return Book.objects.filter( **params )
```


## key_required

To protect a specific view through key based authentication.

```python
from yard import resources
from yard.apps.keyauth.decorators import key_required

class FooResource(resources.Resource):

    @key_required
    def show(self, request, book_id):
        return "bar"
```

Don't forget to add `yard.apps.keyauth` to `INSTALLED_APPS` and `yard.apps.keyauth.backends.KeyAuthBackend` to `AUTHENTICATION_BACKENDS` in your settings.


## validate_form

Check if a *Django's* form is valid. If not, returns a *Bad Request* response (status 400).

```python
from yard.resources.decorators import validateForm
from yard import resources

class BookResource(resources.Resource):

    def get_extra_context(self, request):
        return {'instance': request.user}

    @validate_form(SomeForm, extra=get_extra_context)
    def index(self, request, params):
        return Book.objects.filter( **params )
```


## exception_handling

Handles a given exception, returning a `HttpResponse` with a given status code if caught.

```python
from yard.resources.decorators import exceptionHandling
from yard import resources

class BookResource(resources.Resource):

    @exception_handling(SomeException, response=400)
    def index(self, request, params):
        return Book.objects.filter( **params )
```


## resource_decorator

In case the same decorator is needed for all *HTTP* response methods (*index*, *show*, *create*, *update*, *destroy*).

```python
from yard import resources
from yard.resources.decorators import login_required, resource_decorator

@resource_decorator( login_required )
class FooResource(resources.Resource):

    def show(self, request, book_id):
        return "bar"
```
