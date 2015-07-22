# Basic Usage


## Create the Resource

```python
from yard.resources import Resource

class Foo(Resource):

    class Meta:
        model = models.Foo

    def list(self, request):
        # GET /foo/
        ...

    def detail(self, request, pk):
        # GET /foo/:pk
        ...
```

Go deeper into the [Resource *CRUD* methods](crud.md)! and inspect the [attributes and auxiliar methods](utils/resourse_objects).


## Add to Urlpatterns

Firstly, add the `Resource` objects to an `Api` which will be responsible for generating the *urlpatterns*.

```python
from yard.api import Api

api = Api()
api.include( r'foo', Foo )
```

If you want to add the `urlpatterns` of some other *urls.py*, you need to use the `extend` method. 

```python
api.extend( r'someapp', 'path.to.someapp.urls' )
```

Finally, after including all the `Resource` objects, declare the `urlpatterns` variable in *urls.py* with the `Api` instance.

```python
urlpatterns = api.urlpatterns
```

```python    
from django.conf.urls import patterns

urlpatterns = patterns('',
    ...
    *api.urlpatterns
)
```

Find mode about the [API object](utils/api_object.md)!


## Request resource

Once added `api.urlpatterns` to the `urlpatterns`, the `Foo` resource is accessible to your HTTP client:

	http://example.com/foo/
