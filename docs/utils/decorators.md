# Decorators


## validate

Check if resource's parameters are valid. If not, returns a *JSON* response with the errors encountered during validation process. 

<pre>
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
</pre>


## login_required

Check if user is authenticated. If not, returns a *Not Authorized* response (status 401).

<pre>
```python
from yard.resources.decorators import login_required
from yard import resources

class BookResource(resources.Resource):

    @login_required
    def index(self, request, params):
        return Book.objects.filter( **params )
```
</pre>


## validateForm

Check if a *Django's* form is valid. If not, returns a *Bad Request* response (status 400).

<pre>
```python
from yard.resources.decorators import validateForm
from yard import resources

class BookResource(resources.Resource):

    @validateForm(SomeForm)
    def index(self, request, params):
        return Book.objects.filter( **params )
```
</pre>


## exceptionHandling

Handles a given exception, returning a `HttpResponse` with a given status code if caught.

<pre>
```python
from yard.resources.decorators import exceptionHandling
from yard import resources

class BookResource(resources.Resource):

    @exceptionHandling(SomeException, 400)
    def index(self, request, params):
        return Book.objects.filter( **params )
```
</pre>