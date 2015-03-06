# Decorators


## validate

Check if Form is valid. If not, returns a *Bad Request* response (status 400). This decorator play a major part in the API documentation module.


```python
from yard.decorators import validate
from yard.resources import Resource

class BookResource(Resource):

    class Meta:
        model = models.Foo

    def get_extra_create_context(self, request):
        return {'foo': 'bar'}
    
    @create(SomeForm, extra=get_extra_create_context)
    def create(self, request):
        return

    @validate(SomeOtherForm)
    def update(self, request, pk):
        return
```

`validate` is able to detect if the given form is a `Form` or a `ModelForm`. In case of the latter, the decorator instantiates the form with the `instance` argument if `pk` is present in the urlpattern (corresponding to the `edit`, `update`, `destroy` and `edit` methods).


## exception_handling

Handles a given exception, returning a `HttpResponse` with a given status code if caught.

```python
from yard.decorators import exception_handling
from yard.resources import Resource

class Foo(Resource):

    @exception_handling(SomeException, response=400)
    def list(self, request):
        return
```


## resource_decorator

In case the same decorator is needed for all *CRUD* methods.

```python
from yard.resources import Resource
from yard.decorators import login_required, resource_decorator

@resource_decorator( login_required )
class Foo(Resource):

    def detail(self, request, pk):
        return
```


## Authentication & Authorization


### login_required

Check if user is authenticated. 

```python
from yard.decorators import login_required
from yard.resources import Resource

class Foo(Resource):

    class Meta:
        model = models.Foo

    @login_required()
    def list(self, request):
        return models.Foo.objects.all()
```


### permission_required

Check if user has the required permissions. 


```python
from yard.decorators import permission_required
from yard.resources import Resource

class Foo(Resource):

    class Meta:
        model = models.Foo

    @permission_required('foo.can_read')
    def list(self, request):
        return models.Foo.objects.all()
```


### key_required

To protect a specific view through key based authentication.

```python
from yard.resources import Resource
from yard.decorators import key_required

class Foo(Resource):

    class Meta:
        model = models.Foo
    
    @key_required()
    def list(self, request):
        return models.Foo.objects.all()
```

Lear more about [this decorator](apps/key_auth.md).


### Throttling

Limit each user (anonymous or authenticated) to a default maximum number of requests.

```python
from yard.resources import Resource
from yard.decorators import throttle

class Book(Resource):

    class Meta:
        model = models.Book

    @throttle()
    def list(self, request):
        ...
```

Lear more about [this decorator](apps/throttling.md).


## Adapt decorators for native Django to Yard

As simple as this:

```python
from yard.decorators import to_yard_decorator

@to_yard_decorator
def profile_required(): 
    return original_profile_required
```
