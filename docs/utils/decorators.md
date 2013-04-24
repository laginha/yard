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

Check if user is authenticated. If not, returns a *Not Authorized* response (status 401).

```python
from yard.resources.decorators import login_required
from yard import resources

class BookResource(resources.Resource):

    @login_required
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


## validateForm

Check if a *Django's* form is valid. If not, returns a *Bad Request* response (status 400).

```python
from yard.resources.decorators import validateForm
from yard import resources

class BookResource(resources.Resource):

    @validateForm(SomeForm)
    def index(self, request, params):
        return Book.objects.filter( **params )
```


## exceptionHandling

Handles a given exception, returning a `HttpResponse` with a given status code if caught.

```python
from yard.resources.decorators import exceptionHandling
from yard import resources

class BookResource(resources.Resource):

    @exceptionHandling(SomeException, 400)
    def index(self, request, params):
        return Book.objects.filter( **params )
```
