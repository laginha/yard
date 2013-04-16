# Resource

The `Resource` object represents the resource data you wish to provide access to. Its main purposes are:

- Organize the different *CRUD* methods into its instance methods. 
- Simplify your [responses](support.md), returning *JSON* whenever possible.
- Structure your *JSON* response, according to class attribute [*fields*](fields.md).
- Parse input according to class attribute [*Parameters*](working_with_forms/parameters.md).


## Basic Usage

### Create the Resource

```python
from yard import resources

class FooResource(resources.Resource):

    def index(self, request, params):
        return {'foo':'bar'}

    def show(self, request, book_id):
        return 404
```


#### CRUD instance methods

<table border="1">
    <tr>
        <th>Resource Method</th>
        <th>HTTP Method</th>
        <th>URL</th>
    </tr>
    <tr>
        <td>index</td>
        <td>Get</td>
        <td>/myresource/</td>
    </tr>
    <tr>
        <td>show</td>
        <td>Get</td>
        <td>/myresource/:pk/</td>
    </tr>
    <tr>
        <td>create</td>
        <td>Post</td>
        <td>/myresource/</td>
    </tr>
    <tr>
        <td>update</td>
        <td>Put</td>
        <td>/myresource/:pk/</td>
    </tr>
    <tr>
        <td>destroy</td>
        <td>Delete</td>
        <td>/myresource/:pk/</td>
    </tr>
</table>

The `option` method is implemented by default. Although it returns no content in the *HTTP* response, it list the available options for the resource in the *Allow* response header:

    ALLOW: GET, POST, DELETE

Any other method is not implemented by default, thus *Yard* returns *Not Found* whenever requested.


### Create the API

Add the `Resource` objects to an `Api` which will be responsible for generating the *urlpatterns*.

```python
from yard.api import Api

api = Api()
api.include( r'foo', FooResource )
```

If you want to add the `urlpatterns` of some other *urls.py*, you need to use the `extend` method. 

```python
api.extend( r'someapp', 'path.to.someapp.urls' )
```


### Add to Urlpatterns

After including all the `Resource` objects, declare the `urlpatterns` variable in *urls.py* with the `Api` instance.

```python
urlpatterns = api.urlpatterns
```

```python    
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    ...
    *api.urlpatterns
)
```


### Request resource

Once added `api.urlpatterns` to the `urlpatterns`, the `FooResource` is accessible to your HTTP client:

	http://example.com/foo/


### Create the API

Add the `Resource` objects to an `Api` which will be responsible for generating the *urlpatterns*.

```python
from yard.api import Api

api = Api()
api.include( r'foo', FooResource )
```

If you want to add the `urlpatterns` of some other *urls.py*, you need to use the `extend` method. 

```python
api.extend( r'someapp', 'path.to.someapp.urls' )
```


### Add to Urlpatterns

After including all the `Resource` objects, declare the `urlpatterns` variable in *urls.py* with the `Api` instance.

```python
urlpatterns = api.urlpatterns
```

```python    
from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    ...
    *api.urlpatterns
)
```


### Request resource

Once added `api.urlpatterns` to the `urlpatterns`, the `FooResource` is accessible to your HTTP client:

	http://example.com/foo/

